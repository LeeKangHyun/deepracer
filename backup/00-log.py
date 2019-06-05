import json
import time

CODE_NAME = 'center'

g_episode = 0
g_progress = float(0)
g_total = float(0)
g_start = float(0)
g_time = float(0)


def get_episode(progress):
    global g_episode
    global g_progress
    global g_total
    global g_start
    global g_time

    # reset
    if g_progress > progress:
        g_episode += 1
        g_total = float(0)
        g_start = time.time()

    g_time = time.time() - g_start

    # prev progress
    g_progress = progress

    return g_episode


def reward_function(params):
    global g_total
    global g_time

    progress = params['progress']

    reward = 0.001

    # episode
    episode = get_episode(progress)

    g_total += reward

    # log
    params['log_key'] = '{}'.format(CODE_NAME)
    params['episode'] = episode
    params['reward'] = reward
    params['total'] = g_total
    params['time'] = g_time
    print(json.dumps(params))

    return float(reward)
