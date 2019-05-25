import json
import math
import time

NAME = 'mk20-a'
ACTION = '18 / 7 / 5 / 1'
HYPER = '128 / 0.99 / 40'

SIGHT = 1

MAX_CENTER = 0.3

MAX_ANGLE = 10

MAX_STEER = 10
LEN_STEER = 2

MAX_STEPS = 100

BASE_REWARD = 1.2

g_episode = 0
g_progress = float(0)
g_completed = False
g_waypoints = []
g_steer = []
g_total = float(0)
g_start = float(0)
g_time = float(0)


def get_episode(progress, steps):
    global g_episode
    global g_progress
    global g_completed
    global g_waypoints
    global g_steer
    global g_total
    global g_start
    global g_time

    # reset
    if g_progress > progress:
        g_episode += 1
        g_total = float(0)
        g_start = time.time()
        del g_steer[:]

    g_time = time.time() - g_start

    # completed
    if g_progress < progress and progress == 100:
        g_completed = True
        print('- episode completed - {} - {} - {} - {} - {}'.format(NAME, g_episode,
                                                                    g_time, steps, g_total))
    else:
        g_completed = False

    # waypoints
    if len(g_waypoints) < 1:
        g_waypoints = get_waypoints()

    # prev progress
    g_progress = progress

    return g_episode


def get_closest_waypoint(waypoints, x, y):
    closest = 0
    index = 0
    min_distance = float('inf')
    for row in waypoints:
        distance = math.sqrt(
            (row[0] - x) * (row[0] - x) + (row[1] - y) * (row[1] - y))
        if distance < min_distance:
            min_distance = distance
            closest = index
        index += 1
    return closest


def get_distance(coor1, coor2):
    return math.sqrt((coor1[0] - coor2[0]) * (coor1[0] - coor2[0]) + (coor1[1] - coor2[1]) * (coor1[1] - coor2[1]))


def get_destination(waypoints, closest, sight):
    index = closest + sight

    if index >= len(waypoints):
        index = index - len(waypoints)

    return waypoints[index]


def get_diff_angle(coor1, coor2, heading, steering):
    # guide
    angle = math.atan2((coor2[1] - coor1[1]), (coor2[0] - coor1[0]))

    # car yaw
    # yaw = math.radians(heading)
    yaw = math.radians(heading + steering)

    diff = (yaw - angle) % (2.0 * math.pi)

    if diff >= math.pi:
        diff -= 2.0 * math.pi

    return math.degrees(abs(diff))


def get_diff_steering(steering):
    global g_steer

    prev = -100
    diff = 0

    # steering list
    g_steer.append(steering)
    if len(g_steer) > LEN_STEER:
        del g_steer[0]

    # steering diff
    for v in g_steer:
        if prev > -100:
            diff += abs(prev - v)
        prev = v

    diff = diff / (LEN_STEER - 1)

    return diff


def reward_function(params):
    global g_waypoints
    global g_total
    global g_time

    steps = params['steps']
    progress = params['progress']

    # track_width = params['track_width']
    # distance_from_center = params['distance_from_center']

    heading = params['heading']
    steering = params['steering_angle']

    x = params['x']
    y = params['y']
    location = [x, y]

    # waypoints = params['waypoints']
    # closest_waypoints = params['closest_waypoints']
    # prev_waypoint = waypoints[closest_waypoints[0]]
    # next_waypoint = waypoints[closest_waypoints[1]]

    # default
    reward = 0.001

    # episode
    episode = get_episode(progress, steps)

    # closest waypoint
    closest = get_closest_waypoint(g_waypoints, x, y)

    # distance
    distance = get_distance(g_waypoints[closest], location)

    # center bonus
    if distance < MAX_CENTER:
        reward += (BASE_REWARD - (distance / MAX_CENTER))

    # point
    destination = get_destination(g_waypoints, closest, SIGHT)

    # diff angle
    diff_angle = get_diff_angle(location, destination, heading, steering)

    # if diff_angle <= MAX_ANGLE:
    #     reward += (BASE_REWARD - (diff_angle / MAX_ANGLE))

    # diff steering
    diff_steer = get_diff_steering(steering)

    if diff_steer <= MAX_STEER:
        reward += (BASE_REWARD - (diff_steer / MAX_STEER))

    # total reward
    g_total += reward

    # log
    params['name'] = NAME
    params['params'] = ACTION
    params['episode'] = episode
    params['distance'] = distance
    params['destination'] = destination
    params['diff_angle'] = diff_angle
    params['diff_steer'] = diff_steer
    params['reward'] = reward
    params['total'] = g_total
    params['time'] = g_time
    print(json.dumps(params))

    return float(reward)


def get_waypoints():
    # mk19-1412 : 12.16402
    waypoints = []
    waypoints.append([0.51976, 3.59240])
    waypoints.append([0.44372, 3.45534])
    waypoints.append([0.38050, 3.28612])
    waypoints.append([0.33838, 3.08892])
    waypoints.append([0.32505, 2.89342])
    waypoints.append([0.33563, 2.68632])
    waypoints.append([0.35619, 2.49087])
    waypoints.append([0.38760, 2.29594])
    waypoints.append([0.43796, 2.09730])
    waypoints.append([0.49466, 1.92181])
    waypoints.append([0.56486, 1.74624])
    waypoints.append([0.65760, 1.56096])
    waypoints.append([0.75744, 1.39378])
    waypoints.append([0.88405, 1.23598])
    waypoints.append([1.03562, 1.09688])
    waypoints.append([1.19241, 0.99302])
    waypoints.append([1.37817, 0.90455])
    waypoints.append([1.59288, 0.83653])
    waypoints.append([1.81621, 0.80096])
    waypoints.append([2.02494, 0.80101])
    waypoints.append([2.22880, 0.83007])
    waypoints.append([2.43859, 0.88339])
    waypoints.append([2.63488, 0.94528])
    waypoints.append([2.83718, 1.00644])
    waypoints.append([3.03110, 1.05237])
    waypoints.append([3.22733, 1.07636])
    waypoints.append([3.44688, 1.08119])
    waypoints.append([3.62727, 1.07877])
    waypoints.append([3.85800, 1.06984])
    waypoints.append([4.03715, 1.05417])
    waypoints.append([4.24876, 1.02736])
    waypoints.append([4.44853, 0.99159])
    waypoints.append([4.64180, 0.95061])
    waypoints.append([4.83186, 0.90362])
    waypoints.append([5.03354, 0.84922])
    waypoints.append([5.22682, 0.80719])
    waypoints.append([5.42702, 0.77694])
    waypoints.append([5.63253, 0.76242])
    waypoints.append([5.81468, 0.76698])
    waypoints.append([6.00421, 0.79684])
    waypoints.append([6.21150, 0.86169])
    waypoints.append([6.39241, 0.93913])
    waypoints.append([6.55439, 1.03044])
    waypoints.append([6.71640, 1.15830])
    waypoints.append([6.85737, 1.31298])
    waypoints.append([6.96359, 1.46928])
    waypoints.append([7.05109, 1.64680])
    waypoints.append([7.11022, 1.83114])
    waypoints.append([7.14820, 2.04317])
    waypoints.append([7.15300, 2.24659])
    waypoints.append([7.13260, 2.44288])
    waypoints.append([7.08660, 2.63245])
    waypoints.append([7.01619, 2.81061])
    waypoints.append([6.91815, 2.97972])
    waypoints.append([6.78792, 3.14420])
    waypoints.append([6.65047, 3.28856])
    waypoints.append([6.51123, 3.41846])
    waypoints.append([6.35561, 3.54498])
    waypoints.append([6.19596, 3.65995])
    waypoints.append([6.02427, 3.77584])
    waypoints.append([5.83880, 3.89783])
    waypoints.append([5.67771, 3.99936])
    waypoints.append([5.51008, 4.09791])
    waypoints.append([5.32982, 4.19280])
    waypoints.append([5.14226, 4.27476])
    waypoints.append([4.96698, 4.33270])
    waypoints.append([4.76049, 4.37437])
    waypoints.append([4.54242, 4.39937])
    waypoints.append([4.34803, 4.41284])
    waypoints.append([4.14324, 4.42437])
    waypoints.append([3.94441, 4.42752])
    waypoints.append([3.75683, 4.42169])
    waypoints.append([3.54250, 4.41625])
    waypoints.append([3.34360, 4.41211])
    waypoints.append([3.14585, 4.40282])
    waypoints.append([2.93094, 4.38382])
    waypoints.append([2.74903, 4.36142])
    waypoints.append([2.55182, 4.33412])
    waypoints.append([2.36487, 4.31050])
    waypoints.append([2.17474, 4.28660])
    waypoints.append([1.97038, 4.25613])
    waypoints.append([1.76547, 4.21876])
    waypoints.append([1.57797, 4.17749])
    waypoints.append([1.38774, 4.12790])
    waypoints.append([1.18190, 4.05923])
    waypoints.append([0.98385, 3.96397])
    waypoints.append([0.81619, 3.85111])
    waypoints.append([0.67272, 3.72771])
    return waypoints
