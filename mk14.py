import json
import math
import time

NAME = 'mk14-1'
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
    waypoints.append([5.80056, 4.20592])
    waypoints.append([5.71788, 4.25945])
    waypoints.append([5.60014, 4.33185])
    waypoints.append([5.44112, 4.42374])
    waypoints.append([5.25022, 4.52512])
    waypoints.append([5.07247, 4.60549])
    waypoints.append([4.87113, 4.67052])
    waypoints.append([4.68704, 4.70278])
    waypoints.append([4.47370, 4.70609])
    waypoints.append([4.27182, 4.68231])
    waypoints.append([4.06676, 4.64390])
    waypoints.append([3.88510, 4.60331])
    waypoints.append([3.67510, 4.56089])
    waypoints.append([3.48196, 4.52948])
    waypoints.append([3.28509, 4.51463])
    waypoints.append([3.08470, 4.51676])
    waypoints.append([2.85882, 4.53308])
    waypoints.append([2.66182, 4.55523])
    waypoints.append([2.46391, 4.57311])
    waypoints.append([2.26272, 4.57534])
    waypoints.append([2.08379, 4.56530])
    waypoints.append([1.87131, 4.53756])
    waypoints.append([1.64066, 4.48410])
    waypoints.append([1.45554, 4.41828])
    waypoints.append([1.27246, 4.32055])
    waypoints.append([1.13742, 4.21873])
    waypoints.append([0.99240, 4.07849])
    waypoints.append([0.85845, 3.90694])
    waypoints.append([0.76525, 3.74440])
    waypoints.append([0.67568, 3.54631])
    waypoints.append([0.61690, 3.36986])
    waypoints.append([0.57503, 3.17243])
    waypoints.append([0.54990, 2.98636])
    waypoints.append([0.52768, 2.78566])
    waypoints.append([0.51035, 2.58666])
    waypoints.append([0.49850, 2.39754])
    waypoints.append([0.49362, 2.19227])
    waypoints.append([0.49608, 2.00691])
    waypoints.append([0.51131, 1.79590])
    waypoints.append([0.54931, 1.59524])
    waypoints.append([0.60869, 1.42396])
    waypoints.append([0.69260, 1.25175])
    waypoints.append([0.79544, 1.09611])
    waypoints.append([0.92386, 0.95211])
    waypoints.append([1.05769, 0.83806])
    waypoints.append([1.23077, 0.73854])
    waypoints.append([1.40250, 0.67875])
    waypoints.append([1.60878, 0.64981])
    waypoints.append([1.78728, 0.66263])
    waypoints.append([1.97927, 0.70772])
    waypoints.append([2.16748, 0.76414])
    waypoints.append([2.36749, 0.82297])
    waypoints.append([2.55731, 0.87352])
    waypoints.append([2.74960, 0.91945])
    waypoints.append([2.91863, 0.95564])
    waypoints.append([3.10641, 0.98902])
    waypoints.append([3.30189, 1.01478])
    waypoints.append([3.52701, 1.03366])
    waypoints.append([3.71984, 1.04066])
    waypoints.append([3.92300, 1.03989])
    waypoints.append([4.12234, 1.02447])
    waypoints.append([4.33021, 0.98992])
    waypoints.append([4.50628, 0.95779])
    waypoints.append([4.70035, 0.92307])
    waypoints.append([4.89445, 0.88504])
    waypoints.append([5.08514, 0.84249])
    waypoints.append([5.30547, 0.79120])
    waypoints.append([5.48697, 0.75140])
    waypoints.append([5.66798, 0.72631])
    waypoints.append([5.86719, 0.72406])
    waypoints.append([6.08100, 0.75941])
    waypoints.append([6.25880, 0.82330])
    waypoints.append([6.42096, 0.91701])
    waypoints.append([6.56818, 1.03562])
    waypoints.append([6.69822, 1.16609])
    waypoints.append([6.84153, 1.32464])
    waypoints.append([6.96163, 1.46242])
    waypoints.append([7.07850, 1.62076])
    waypoints.append([7.17600, 1.79976])
    waypoints.append([7.24462, 1.98666])
    waypoints.append([7.28768, 2.18190])
    waypoints.append([7.30473, 2.37430])
    waypoints.append([7.29916, 2.56507])
    waypoints.append([7.27381, 2.73916])
    waypoints.append([7.21643, 2.93575])
    waypoints.append([7.13376, 3.10269])
    waypoints.append([7.01264, 3.26970])
    waypoints.append([6.87532, 3.41216])
    waypoints.append([6.72086, 3.54170])
    waypoints.append([6.54573, 3.67138])
    waypoints.append([6.39780, 3.77423])
    waypoints.append([6.22779, 3.88490])
    waypoints.append([6.04722, 4.00412])
    waypoints.append([5.91426, 4.12353])
    return waypoints
