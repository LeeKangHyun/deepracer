import json
import math
import time

NAME = 're02-80-m'
ACTION = '22 / 5 / 8.0 / 2'
HYPER = '256 / 0.00003 / 40'

MIN_SIGHT = 3
MAX_SIGHT = 6

MAX_SPEED = 6.0
MIN_SPEED = 3.0

MIN_ANGLE = 5.0

MAX_STEER = 20.0
MIN_STEER = 13.0

MIN_PROGRESS = 0.75

g_episode = 0
g_progress = float(0)
g_total = float(0)
g_start = float(0)
g_param = []


def get_episode(steps, progress):
    global g_episode
    global g_progress
    global g_total
    global g_start
    global g_param

    # reset
    if steps == 0:
        g_episode += 1
        g_total = float(0)
        g_start = time.time()

        if g_episode > 1:
            g_param['diff_progress'] = g_param['progress']
            g_param['progress'] = -1
            print(json.dumps(g_param))

        diff_progress = 0.00001
    else:
        diff_progress = progress - g_progress

    # prev
    g_progress = progress

    # lap time
    lap_time = time.time() - g_start

    return g_episode, diff_progress, lap_time


def get_rules(index):
    # 0 : any direction [33,34]
    # 1 : straight
    # 2 : left [10,22] [40,42] [50,52] [60,67]
    # 3 : right

    rules = [
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  # 0
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 1, 1, 1, 1, 1, 1, 1,  # 20
        1, 1, 1, 0, 0, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 2, 2, 2,  # 40
        2, 2, 2, 2, 2, 1, 1, 1, 1, 1,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 1,  # 60
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1
    ]

    return rules[index]


def reward_function(params):
    global g_total
    global g_param

    steps = params['steps']
    progress = params['progress']

    # track_width = params['track_width']
    # distance_from_center = params['distance_from_center']
    # all_wheels_on_track = params['all_wheels_on_track']

    speed = params['speed']
    steering = params['steering_angle']
    # heading = params['heading']

    # waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    # next0 = waypoints[closest_waypoints[1]]
    # next1 = waypoints[(closest_waypoints[1] + MIN_SIGHT) % len(waypoints)]
    # next2 = waypoints[(closest_waypoints[1] + MAX_SIGHT) % len(waypoints)]

    closest_waypoint = closest_waypoints[1]

    # default
    reward = 0.00001

    # episode
    episode, diff_progress, lap_time = get_episode(steps, progress)

    # distance
    distance = params['distance_from_center']

    # diff steering
    abs_steer = abs(steering)

    # direction
    direction = get_rules(closest_waypoint)

    # reward
    if speed > MIN_SPEED:
        reward = 1.0

        # progress bonus
        if diff_progress > MIN_PROGRESS:
            reward *= 2.0

        # bonus
        if speed > MAX_SPEED and abs_steer < MAX_STEER:
            reward *= 3.0
        elif (direction == 0 and abs_steer < MAX_STEER):
            reward *= 1.0
        elif (direction == 1 and abs_steer < 1):
            reward *= 1.0
        elif (direction == 2 and steering >= 0) or (direction == 3 and steering <= 0):
            reward *= 1.0
        else:
            reward *= 0.1

    # total reward
    g_total += reward

    # log
    params['name'] = NAME
    params['params'] = ACTION
    params['episode'] = episode
    params['distance'] = distance
    params['diff_progress'] = diff_progress
    params['direction'] = direction
    params['reward'] = reward
    params['total'] = g_total
    params['time'] = lap_time
    print(json.dumps(params))

    g_param = params

    return float(reward)
