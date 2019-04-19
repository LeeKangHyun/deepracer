import json
import math

CODE_NAME = 'speed'

MAX_SPEED = 2
MIN_SPEED = MAX_SPEED * 0.8

g_episode = 0
g_total = 0
g_prev = 0


def get_episode(progress):
    global g_episode
    global g_total
    global g_prev

    if g_episode == 0 or g_prev > progress:
        g_episode += 1
        g_total = 0

    g_prev = progress

    return g_episode, g_total


def reward_function(params):
    speed = params['speed']
    track_width = params['track_width']
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    progress = params['progress']

    reward = 0.001

    # episode
    episode, total = get_episode(progress)

    if all_wheels_on_track == True:
        # center
        distance_rate = distance_from_center / track_width

        if distance_rate <= 0.1:
            reward = 1.0
        elif distance_rate <= 0.2:
            reward = 0.5
        elif distance_rate <= 0.4:
            reward = 0.1

        # speed
        if speed >= MIN_SPEED:
            reward *= 1.5

    total += reward

    # log
    params['log_key'] = '{}-{}'.format(CODE_NAME, MAX_SPEED)
    params['episode'] = episode
    params['reward'] = reward
    params['total'] = total
    print(json.dumps(params))

    return float(reward)
