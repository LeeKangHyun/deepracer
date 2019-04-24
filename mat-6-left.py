import json
import math

CODE_NAME = 'left'

g_progress = 0
g_episode = 0
g_speed = 0
g_total = 0
g_bonus = 0
g_steer = []


def get_episode(progress, speed):
    global g_progress
    global g_episode
    global g_speed
    global g_total
    global g_bonus

    if g_progress > progress:
        g_episode += 1
        g_total = 0
        g_bonus = 0
        del g_steer[:]
    else:
        if progress == 100:
            g_bonus = 0.5
        else:
            g_bonus = progress - g_progress

    g_progress = progress

    if g_speed < speed:
        g_speed = speed

    return g_episode


def reward_function(params):
    global g_total
    global g_bonus

    all_wheels_on_track = params['all_wheels_on_track']
    progress = params['progress']

    speed = params['speed']

    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    is_left_of_center = params['is_left_of_center']
    is_reversed = params['is_reversed']

    reward = 0.001

    # episode
    episode = get_episode(progress, speed)

    if all_wheels_on_track == True:
        # speed
        min_speed = g_speed * 0.7

        if speed > min_speed:
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
                    reward = 1.0 + g_bonus
            #     elif distance_rate <= 0.5:
            #         reward = 0.5
            # else:
            #     if distance_rate <= 0.3:
            #         reward = 0.5

    g_total += reward

    # log
    params['log_key'] = CODE_NAME
    params['episode'] = episode
    params['reward'] = reward
    params['total'] = g_total
    print(json.dumps(params))

    return float(reward)
