import json
import math

CODE_NAME = 'in-out'

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

    all_wheels_on_track = params['all_wheels_on_track']
    progress = params['progress']

    speed = params['speed']

    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    is_left_of_center = params['is_left_of_center']
    is_reversed = params['is_reversed']

    x = params['x']
    y = params['y']

    reward = 0.001

    # episode
    episode = get_episode(progress, speed)

    if all_wheels_on_track == True:
        # center
        distance_rate = distance_from_center / track_width

        if distance_rate < 0.5:
            # speed
            min_speed = g_speed * 7

            if speed > min_speed:
                # reverse
                if is_reversed:
                    if is_left_of_center:
                        is_left_of_center = False
                    else:
                        is_left_of_center = True

                # out-in-out
                if is_left_of_center:
                    if x > 6.5:
                        reward = 1
                    elif y > 3.5:
                        reward = 1
                    elif x < 2.5 and y < 1.5:
                        reward = 1
                else:
                    if x > 3.5 and x < 5.5 and y > 3.5:
                        reward = 1
                    elif x < 2.5 and y > 2.0 and y < 3.0:
                        reward = 1

    g_total += reward

    # log
    params['log_key'] = CODE_NAME
    params['episode'] = episode
    params['reward'] = reward
    params['total'] = g_total
    print(json.dumps(params))

    return float(reward)
