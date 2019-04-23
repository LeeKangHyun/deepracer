import json
import math

CODE_NAME = 'left'

MAX_SPEED = 2
MIN_SPEED = MAX_SPEED * 0.7

g_episode = 0
g_total = 0
g_prev = 0
g_diff = 0


def get_episode(progress):
    global g_episode
    global g_total
    global g_prev
    global g_diff

    if g_prev > progress:
        g_episode += 1
        g_total = 0
        g_diff = 0
    else:
        if progress == 100:
            g_diff = 0.5
        else:
            g_diff = progress - g_prev

    g_prev = progress

    return g_episode


def reward_function(params):
    global g_total
    global g_diff

    all_wheels_on_track = params['all_wheels_on_track']
    progress = params['progress']

    speed = params['speed']

    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    is_left_of_center = params['is_left_of_center']
    is_reversed = params['is_reversed']

    reward = 0.001

    # episode
    episode = get_episode(progress)

    if all_wheels_on_track == True:
        # speed
        if speed > MIN_SPEED:
            # center
            distance_rate = distance_from_center / track_width

            # reverse
            if is_reversed:
                if is_left_of_center:
                    is_left_of_center = False
                else:
                    is_left_of_center = True

            # left
            if is_left_of_center:
                if distance_rate <= 0.1:
                    reward = 1.0 + g_diff
            #     elif distance_rate <= 0.5:
            #         reward = 0.5
            # else:
            #     if distance_rate <= 0.3:
            #         reward = 0.5

    g_total += reward

    # log
    params['log_key'] = '{}-{}'.format(CODE_NAME, MAX_SPEED)
    params['episode'] = episode
    params['reward'] = reward
    params['total'] = g_total
    print(json.dumps(params))

    return float(reward)
