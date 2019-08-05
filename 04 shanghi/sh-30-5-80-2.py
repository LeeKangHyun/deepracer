import json
import math
import time

NAME = 'sh-30-5-80-2'

BASE_REWARD = 10.0

MAX_CENTER = 0.25

MAX_STEER = 30.0
MIN_STEER = 10.0

MAX_SPEED = 8.0
MIN_SPEED = 3.0

g_episode = 0
g_progress = float(0)
g_total = float(0)
g_start = float(0)
g_param = []


def get_episode(steps, progress):
    global g_episode
    global g_progress
    global g_param

    # reset
    if steps == 0:
        g_episode += 1
        diff_progress = 0.00001

        if g_episode > 1:
            g_param['diff_progress'] = g_param['progress']
            g_param['progress'] = -1
            print(json.dumps(g_param))
    else:
        diff_progress = progress - g_progress

    # prev
    g_progress = progress

    return g_episode, diff_progress


def reward_function(params):
    global g_total
    global g_start
    global g_param

    steps = params['steps']
    progress = params['progress']

    steering = params['steering_angle']
    speed = params['speed']

    # episode
    episode, diff_progress = get_episode(steps, progress)

    # reset
    if steps == 0:
        g_total = float(0)
        g_start = time.time()

    # lap time
    lap_time = time.time() - g_start

    # distance
    distance = params['distance_from_center']
    track_width = params['track_width']
    track_half = track_width / 2.0

    # abs steering
    abs_steer = abs(steering)

    # reward
    reward = BASE_REWARD
    reward *= (track_width - distance) / track_half
    reward *= (MAX_STEER - abs_steer) / MAX_STEER
    reward *= speed / MAX_SPEED

    if reward < 0:
        reward = 0.00001

    # total reward
    g_total += reward

    # log
    params['name'] = NAME
    params['episode'] = episode
    params['diff_progress'] = diff_progress
    params['abs_steer'] = abs_steer
    params['reward'] = reward
    params['total'] = g_total
    params['time'] = lap_time
    print(json.dumps(params))

    g_param = params

    return float(reward)
