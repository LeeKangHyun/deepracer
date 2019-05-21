import json
import math
import time

NAME = 'mk19'
ACTION = '18 / 7 / 5 / 1'

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
    res = 0
    index = 0
    # waypoints = get_waypoints()
    min_distance = float('inf')
    for row in waypoints:
        distance = math.sqrt(
            (row[0] - x) * (row[0] - x) + (row[1] - y) * (row[1] - y))
        if distance < min_distance:
            min_distance = distance
            res = index
        index = index + 1
    return res


def get_distance(coor1, coor2):
    return math.sqrt((coor1[0] - coor2[0]) * (coor1[0] - coor2[0]) + (coor1[1] - coor2[1]) * (coor1[1] - coor2[1]))


def get_next_point(waypoints, coor, closest, distance):
    idx = closest + distance

    if idx > len(waypoints):
        idx = idx - len(waypoints)

    return waypoints[idx]


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
    destination = get_next_point(g_waypoints, location, closest, SIGHT)

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
    # mk17-3779 : 12.08786
    waypoints = []
    waypoints.append([4.51924, 0.94947])
    waypoints.append([4.72065, 0.96947])
    waypoints.append([4.90346, 0.92127])
    waypoints.append([5.09590, 0.87284])
    waypoints.append([5.28353, 0.82819])
    waypoints.append([5.47253, 0.79156])
    waypoints.append([5.68686, 0.77315])
    waypoints.append([5.88856, 0.78262])
    waypoints.append([6.09699, 0.82496])
    waypoints.append([6.29590, 0.90720])
    waypoints.append([6.46692, 1.01641])
    waypoints.append([6.62835, 1.15746])
    waypoints.append([6.75403, 1.29477])
    waypoints.append([6.88200, 1.45740])
    waypoints.append([6.98948, 1.62523])
    waypoints.append([7.07103, 1.79671])
    waypoints.append([7.13119, 2.00030])
    waypoints.append([7.15550, 2.19367])
    waypoints.append([7.15643, 2.38786])
    waypoints.append([7.12878, 2.59147])
    waypoints.append([7.07524, 2.78715])
    waypoints.append([7.00045, 2.97919])
    waypoints.append([6.90218, 3.15394])
    waypoints.append([6.77540, 3.31139])
    waypoints.append([6.64178, 3.43569])
    waypoints.append([6.47508, 3.56477])
    waypoints.append([6.30582, 3.67831])
    waypoints.append([6.13413, 3.77637])
    waypoints.append([5.96340, 3.86716])
    waypoints.append([5.78205, 3.96641])
    waypoints.append([5.61543, 4.05799])
    waypoints.append([5.43259, 4.15718])
    waypoints.append([5.23785, 4.25960])
    waypoints.append([5.07677, 4.33170])
    waypoints.append([4.87590, 4.40682])
    waypoints.append([4.68310, 4.47165])
    waypoints.append([4.48896, 4.52680])
    waypoints.append([4.30277, 4.56763])
    waypoints.append([4.10523, 4.59094])
    waypoints.append([3.90130, 4.59932])
    waypoints.append([3.71634, 4.58888])
    waypoints.append([3.50672, 4.56152])
    waypoints.append([3.30471, 4.53151])
    waypoints.append([3.10150, 4.50439])
    waypoints.append([2.91107, 4.48990])
    waypoints.append([2.69634, 4.48267])
    waypoints.append([2.47776, 4.47581])
    waypoints.append([2.26069, 4.47213])
    waypoints.append([2.07700, 4.46525])
    waypoints.append([1.88598, 4.45176])
    waypoints.append([1.67958, 4.42629])
    waypoints.append([1.48419, 4.37681])
    waypoints.append([1.30926, 4.31491])
    waypoints.append([1.12989, 4.23253])
    waypoints.append([0.94550, 4.12106])
    waypoints.append([0.79534, 3.99662])
    waypoints.append([0.65952, 3.83548])
    waypoints.append([0.55705, 3.65934])
    waypoints.append([0.48697, 3.48136])
    waypoints.append([0.43413, 3.27279])
    waypoints.append([0.40536, 3.09771])
    waypoints.append([0.39255, 2.90650])
    waypoints.append([0.40225, 2.70544])
    waypoints.append([0.43090, 2.49140])
    waypoints.append([0.46823, 2.29583])
    waypoints.append([0.51556, 2.11258])
    waypoints.append([0.58271, 1.91844])
    waypoints.append([0.67401, 1.71830])
    waypoints.append([0.76385, 1.55065])
    waypoints.append([0.87489, 1.37185])
    waypoints.append([1.01093, 1.19337])
    waypoints.append([1.15897, 1.05361])
    waypoints.append([1.32798, 0.94359])
    waypoints.append([1.50068, 0.86500])
    waypoints.append([1.70609, 0.80742])
    waypoints.append([1.93302, 0.78272])
    waypoints.append([2.12585, 0.78219])
    waypoints.append([2.32548, 0.80541])
    waypoints.append([2.52337, 0.84509])
    waypoints.append([2.74230, 0.89078])
    waypoints.append([2.93506, 0.92652])
    waypoints.append([3.16310, 0.95202])
    waypoints.append([3.36451, 0.95181])
    waypoints.append([3.57010, 0.92998])
    waypoints.append([3.74748, 0.92998])
    waypoints.append([3.95386, 0.92998])
    waypoints.append([4.14270, 0.92998])
    waypoints.append([4.34740, 0.92998])
    return waypoints
