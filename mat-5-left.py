import json
import math

CODE_NAME = 'left'

MAX_SPEED = 2
MIN_SPEED = MAX_SPEED * 0.8

g_episode = 0
g_prev = 0

def get_episode(progress):
    global g_episode
    global g_prev

    if g_episode == 0 or g_prev > progress:
        g_episode += 1

    g_prev = progress

    return g_episode

def reward_function(params):
    speed = params['speed']
    track_width = params['track_width']
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    is_left_of_center = params['is_left_of_center']
    is_reversed = params['is_reversed']
    progress = params['progress']

    reward = 0.001

    # episode
    episode = get_episode(progress)

    if all_wheels_on_track == True:
        # center
        distance_rate = distance_from_center / track_width

        if distance_rate < 0.5:
            # speed
            if speed >= MIN_SPEED:
                # reverse
                if is_reversed:
                    if is_left_of_center:
                        is_left_of_center = False
                    else:
                        is_left_of_center = True

                # left
                if is_left_of_center:
                    reward = 1

    # log
    params['log_key'] = '{}-{}'.format(CODE_NAME, MAX_SPEED)
    params['episode'] = episode
    params['reward'] = reward
    print(json.dumps(params))

    return float(reward)
