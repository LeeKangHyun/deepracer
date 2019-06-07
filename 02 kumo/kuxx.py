import json
import math
import time

NAME = 'kuxx-r'
ACTION = '30 / 7 / 5 / 1'
HYPER = '256 / 0.999 / 40'

g_episode = 0
g_steps = float(0)
g_progress = float(0)
g_steer = []
g_total = float(0)
g_start = float(0)
g_time = float(0)


def get_episode(steps, progress):
    global g_episode
    global g_steps
    global g_progress
    global g_steer
    global g_total
    global g_start
    global g_time

    # reset
    if steps == 0:
        g_episode += 1
        diff_progress = 0.00001
        g_total = float(0)
        g_start = time.time()
        del g_steer[:]
    else:
        diff_progress = progress - g_progress

    # lab time
    g_time = time.time() - g_start

    # prev
    g_progress = progress

    # min steps
    if progress == 100 and g_steps > steps:
        g_steps = steps

    return g_episode, diff_progress


def reward_function(params):
    global g_total
    global g_time

    steps = params['steps']
    progress = params['progress']

    steering = params['steering_angle']

    # default
    reward = 0.00001

    # episode
    episode, diff_progress = get_episode(steps, progress)

    if steering < -25:
        reward += 10

    # total reward
    g_total += reward

    # log
    params['name'] = NAME
    params['params'] = ACTION
    params['episode'] = episode
    params['diff_progress'] = diff_progress
    params['reward'] = reward
    params['total'] = g_total
    params['time'] = g_time
    print(json.dumps(params))

    return float(reward)
