import json
import math
import time

NAME = 'mk11'
PARAM = '21 / 5 / 4.5 / 1'

SIGHT = 0.6

BASE_REWARD = 1.2

MAX_ANGLE = 5

MAX_STEER = 15
LEN_STEER = 3

MAX_STEPS = 200

g_episode = 0
g_progress = float(0)
g_completed = False
g_total = float(0)
g_steer = []
g_start = 0


def get_episode(progress):
    global g_episode
    global g_progress
    global g_completed
    global g_total
    global g_steer
    global g_start

    # reset
    if g_progress > progress:
        g_episode += 1
        g_total = float(0)
        g_start = time.time()
        del g_steer[:]

    # completed
    if g_progress < progress and progress == 100:
        g_completed = True
        seconds = time.time() - g_start
        print('--- completed --- {} seconds ---'.format(seconds))
    else:
        g_completed = False

    # prev progress
    g_progress = progress

    return g_episode


def get_distance(coor1, coor2):
    return math.sqrt((coor1[0] - coor2[0]) * (coor1[0] - coor2[0]) + (coor1[1] - coor2[1]) * (coor1[1] - coor2[1]))


def get_next_point(waypoints, this_point, closest, distance):
    next_index = closest
    next_point = []

    while True:
        next_point = waypoints[next_index]

        dist = get_distance(this_point, next_point)
        if dist >= distance:
            break

        next_index += 1
        if next_index >= len(waypoints):
            next_index = next_index - len(waypoints)

    return next_point


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
    global g_total

    progress = params['progress']

    track_width = params['track_width']
    distance_from_center = params['distance_from_center']

    heading = params['heading']
    steering = params['steering_angle']

    x = params['x']
    y = params['y']

    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    # prev_waypoint = waypoints[closest_waypoints[0]]
    # next_waypoint = waypoints[closest_waypoints[1]]

    # default
    reward = 0.001

    # episode
    episode = get_episode(progress)

    # point
    this_point = [x, y]
    next_point = get_next_point(
        waypoints, this_point, closest_waypoints[1], SIGHT)

    # diff angle
    diff_angle = get_diff_angle(
        this_point, next_point, heading, steering)

    # diff steering
    diff_steer = get_diff_steering(steering)

    if diff_angle <= MAX_ANGLE and diff_steer <= MAX_STEER:
        # angle
        reward += (BASE_REWARD - (diff_angle / MAX_ANGLE))

        # steering
        reward += (BASE_REWARD - (diff_steer / MAX_STEER))

        # center bonus
        reward += (BASE_REWARD - (distance_from_center / (track_width / 2)))

    g_total += reward

    # log
    params['name'] = NAME
    params['params'] = PARAM
    params['episode'] = episode
    params['diff_angle'] = diff_angle
    params['diff_steer'] = diff_steer
    params['next_point'] = next_point
    params['reward'] = reward
    params['total'] = g_total
    print(json.dumps(params))

    return float(reward)