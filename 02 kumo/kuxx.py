import json
import math
import time

NAME = 'kuxx-r'
ACTION = '30 / 7 / 5 / 1'
HYPER = '256 / 0.999 / 40'

g_episode = 0
g_progress = float(0)
g_steps = float(0)
g_total = float(0)
g_start = float(0)
g_time = float(0)


def get_episode(progress, steps):
    global g_episode
    global g_progress
    global g_steps
    global g_total
    global g_start
    global g_time

    diff_progress = progress - g_progress

    # reset
    if diff_progress < 0:
        print('- episode reset - {} - {} - {} - {} - {}'.format(NAME, g_episode,
                                                                g_time, g_steps, g_progress))
        g_episode += 1
        g_total = float(0)
        g_start = time.time()

    g_time = time.time() - g_start

    # completed
    if g_progress < progress and progress == 100:
        print('- episode completed - {} - {} - {} - {} - {}'.format(NAME, g_episode,
                                                                    g_time, steps, progress))

    # prev
    g_progress = progress
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
    episode, diff_progress = get_episode(progress, steps)

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
