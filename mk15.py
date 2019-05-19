import json
import math
import time

NAME = 'mk15-1'
ACTION = '18 / 7 / 5 / 1 / 0.5 / 10'

SIGHT = 0.3

MAX_ANGLE = 10

BASE_REWARD = 1.2

g_episode = 0
g_progress = float(0)
g_completed = False
g_waypoints = []
g_total = float(0)
g_start = float(0)
g_time = float(0)


def get_episode(progress, steps):
    global g_episode
    global g_progress
    global g_completed
    global g_waypoints
    global g_total
    global g_start
    global g_time

    # reset
    if g_progress > progress:
        g_episode += 1
        g_total = float(0)
        g_start = time.time()

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
    idx = closest
    dest = []

    while True:
        dest = waypoints[idx]

        dist = get_distance(coor, dest)
        if dist >= distance:
            break

        idx += 1
        if idx >= len(waypoints):
            idx = idx - len(waypoints)

    return dest


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

    # point
    destination = get_next_point(g_waypoints, location, closest, SIGHT)

    # diff angle
    diff_angle = get_diff_angle(location, destination, heading, steering)

    if diff_angle <= MAX_ANGLE:
        # angle
        reward += (BASE_REWARD - (diff_angle / MAX_ANGLE))

    # center bonus
    # reward += (BASE_REWARD - (distance_from_center / (track_width / 2)))
    reward += (BASE_REWARD - distance)

    g_total += reward

    # log
    params['name'] = NAME
    params['params'] = ACTION
    params['episode'] = episode
    params['distance'] = distance
    params['diff_angle'] = diff_angle
    params['destination'] = destination
    params['reward'] = reward
    params['total'] = g_total
    params['time'] = g_time
    print(json.dumps(params))

    return float(reward)


def get_waypoints():
    waypoints = []
    waypoints.append([5.66370, 4.29320])
    waypoints.append([5.53341, 4.35786])
    waypoints.append([5.35650, 4.42695])
    waypoints.append([5.16926, 4.48315])
    waypoints.append([4.97112, 4.52565])
    waypoints.append([4.77482, 4.54958])
    waypoints.append([4.57910, 4.56087])
    waypoints.append([4.39365, 4.56691])
    waypoints.append([4.20165, 4.57305])
    waypoints.append([4.00245, 4.58743])
    waypoints.append([3.79770, 4.61511])
    waypoints.append([3.60778, 4.64489])
    waypoints.append([3.40183, 4.67561])
    waypoints.append([3.20580, 4.70093])
    waypoints.append([3.01651, 4.71522])
    waypoints.append([2.81311, 4.71595])
    waypoints.append([2.61158, 4.70619])
    waypoints.append([2.42432, 4.68780])
    waypoints.append([2.22611, 4.65887])
    waypoints.append([2.03404, 4.61637])
    waypoints.append([1.84679, 4.55488])
    waypoints.append([1.64895, 4.47532])
    waypoints.append([1.46716, 4.39147])
    waypoints.append([1.28876, 4.29275])
    waypoints.append([1.14495, 4.19316])
    waypoints.append([0.99031, 4.05429])
    waypoints.append([0.86619, 3.90409])
    waypoints.append([0.77007, 3.73985])
    waypoints.append([0.68701, 3.52540])
    waypoints.append([0.63643, 3.33200])
    waypoints.append([0.59735, 3.14455])
    waypoints.append([0.56141, 2.95634])
    waypoints.append([0.52543, 2.76059])
    waypoints.append([0.49512, 2.57089])
    waypoints.append([0.47259, 2.39474])
    waypoints.append([0.45875, 2.20228])
    waypoints.append([0.46353, 2.02609])
    waypoints.append([0.48789, 1.82579])
    waypoints.append([0.52698, 1.62208])
    waypoints.append([0.58616, 1.42517])
    waypoints.append([0.66485, 1.24861])
    waypoints.append([0.76334, 1.09617])
    waypoints.append([0.89440, 0.94619])
    waypoints.append([1.03833, 0.82718])
    waypoints.append([1.20525, 0.72778])
    waypoints.append([1.37982, 0.65849])
    waypoints.append([1.58337, 0.60898])
    waypoints.append([1.78563, 0.58608])
    waypoints.append([1.97716, 0.59113])
    waypoints.append([2.15591, 0.61301])
    waypoints.append([2.35033, 0.64308])
    waypoints.append([2.55772, 0.66978])
    waypoints.append([2.75327, 0.69324])
    waypoints.append([2.94569, 0.71728])
    waypoints.append([3.14328, 0.74424])
    waypoints.append([3.34301, 0.76620])
    waypoints.append([3.53064, 0.78011])
    waypoints.append([3.72870, 0.78690])
    waypoints.append([3.92769, 0.79757])
    waypoints.append([4.10814, 0.80674])
    waypoints.append([4.32686, 0.80006])
    waypoints.append([4.51405, 0.78515])
    waypoints.append([4.73070, 0.76881])
    waypoints.append([4.93341, 0.75296])
    waypoints.append([5.11925, 0.73692])
    waypoints.append([5.31583, 0.72079])
    waypoints.append([5.53285, 0.70845])
    waypoints.append([5.72438, 0.71307])
    waypoints.append([5.92754, 0.74350])
    waypoints.append([6.11187, 0.80221])
    waypoints.append([6.28906, 0.89405])
    waypoints.append([6.44431, 1.01030])
    waypoints.append([6.57958, 1.15076])
    waypoints.append([6.69389, 1.30934])
    waypoints.append([6.79380, 1.46801])
    waypoints.append([6.89770, 1.65620])
    waypoints.append([6.97850, 1.83453])
    waypoints.append([7.04654, 2.01746])
    waypoints.append([7.09502, 2.19834])
    waypoints.append([7.12712, 2.38214])
    waypoints.append([7.13876, 2.60543])
    waypoints.append([7.10999, 2.81123])
    waypoints.append([7.04533, 3.00089])
    waypoints.append([6.95404, 3.17670])
    waypoints.append([6.85349, 3.32962])
    waypoints.append([6.72245, 3.49556])
    waypoints.append([6.58755, 3.63237])
    waypoints.append([6.43677, 3.76242])
    waypoints.append([6.28354, 3.87947])
    waypoints.append([6.11897, 3.99522])
    waypoints.append([5.95282, 4.10550])
    waypoints.append([5.78273, 4.20628])
    return waypoints
