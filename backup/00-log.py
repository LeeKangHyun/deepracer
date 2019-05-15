import json

CODE_NAME = 'center'

g_episode = 0
g_progress = float(0)
g_total = float(0)


def get_episode(progress):
    global g_episode
    global g_progress
    global g_total

    # reset
    if g_progress > progress:
        g_episode += 1
        g_total = float(0)

    # prev progress
    g_progress = progress

    return g_episode


def reward_function(params):
    global g_total

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
    print(json.dumps(params))

    return float(reward)
