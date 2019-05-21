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
    # mk15-1-2369 : 12.16402
    waypoints = []
    waypoints.append([2.97767, 4.60312])
    waypoints.append([2.83500, 4.58851])
    waypoints.append([2.66094, 4.57260])
    waypoints.append([2.46208, 4.56710])
    waypoints.append([2.25843, 4.55949])
    waypoints.append([2.04656, 4.53518])
    waypoints.append([1.86197, 4.49741])
    waypoints.append([1.65763, 4.43898])
    waypoints.append([1.47362, 4.36323])
    waypoints.append([1.30242, 4.27484])
    waypoints.append([1.14376, 4.17479])
    waypoints.append([0.99419, 4.05242])
    waypoints.append([0.85656, 3.89948])
    waypoints.append([0.74485, 3.73091])
    waypoints.append([0.64358, 3.53244])
    waypoints.append([0.57034, 3.34704])
    waypoints.append([0.51308, 3.15598])
    waypoints.append([0.46532, 2.94197])
    waypoints.append([0.43333, 2.74226])
    waypoints.append([0.41638, 2.52570])
    waypoints.append([0.42563, 2.32478])
    waypoints.append([0.46146, 2.13845])
    waypoints.append([0.52090, 1.94914])
    waypoints.append([0.60346, 1.76409])
    waypoints.append([0.70449, 1.59493])
    waypoints.append([0.82129, 1.43344])
    waypoints.append([0.95664, 1.26238])
    waypoints.append([1.09239, 1.12337])
    waypoints.append([1.25194, 1.00036])
    waypoints.append([1.44051, 0.90402])
    waypoints.append([1.62061, 0.84361])
    waypoints.append([1.80650, 0.80211])
    waypoints.append([2.02136, 0.77786])
    waypoints.append([2.22682, 0.76111])
    waypoints.append([2.41779, 0.75221])
    waypoints.append([2.61961, 0.75762])
    waypoints.append([2.82694, 0.78585])
    waypoints.append([3.03243, 0.82510])
    waypoints.append([3.20695, 0.85804])
    waypoints.append([3.41163, 0.89586])
    waypoints.append([3.60304, 0.92329])
    waypoints.append([3.80263, 0.93734])
    waypoints.append([3.99534, 0.94002])
    waypoints.append([4.19338, 0.93429])
    waypoints.append([4.40900, 0.91709])
    waypoints.append([4.61544, 0.89042])
    waypoints.append([4.82158, 0.85327])
    waypoints.append([5.01442, 0.81365])
    waypoints.append([5.21810, 0.76902])
    waypoints.append([5.41240, 0.72787])
    waypoints.append([5.61212, 0.69931])
    waypoints.append([5.80460, 0.69438])
    waypoints.append([6.01191, 0.71756])
    waypoints.append([6.21355, 0.76809])
    waypoints.append([6.39822, 0.84018])
    waypoints.append([6.57703, 0.94534])
    waypoints.append([6.71872, 1.06589])
    waypoints.append([6.85173, 1.21851])
    waypoints.append([6.95664, 1.37827])
    waypoints.append([7.04170, 1.55430])
    waypoints.append([7.10990, 1.73572])
    waypoints.append([7.15855, 1.92585])
    waypoints.append([7.18413, 2.13412])
    waypoints.append([7.18829, 2.32991])
    waypoints.append([7.17169, 2.55817])
    waypoints.append([7.13450, 2.73437])
    waypoints.append([7.05646, 2.94256])
    waypoints.append([6.96940, 3.10120])
    waypoints.append([6.84163, 3.27394])
    waypoints.append([6.68996, 3.42234])
    waypoints.append([6.54860, 3.52935])
    waypoints.append([6.38136, 3.63435])
    waypoints.append([6.20633, 3.73457])
    waypoints.append([6.01762, 3.83760])
    waypoints.append([5.83286, 3.93763])
    waypoints.append([5.65950, 4.02998])
    waypoints.append([5.48149, 4.12280])
    waypoints.append([5.29630, 4.21497])
    waypoints.append([5.10121, 4.29623])
    waypoints.append([4.92588, 4.35193])
    waypoints.append([4.71549, 4.40021])
    waypoints.append([4.52263, 4.43506])
    waypoints.append([4.32630, 4.46820])
    waypoints.append([4.13270, 4.49703])
    waypoints.append([3.93026, 4.52514])
    waypoints.append([3.72861, 4.55347])
    waypoints.append([3.51931, 4.58120])
    waypoints.append([3.32636, 4.60595])
    waypoints.append([3.12311, 4.60487])
    return waypoints
