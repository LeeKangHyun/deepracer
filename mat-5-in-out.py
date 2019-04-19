import json
import math

MAX_SPEED = 5
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
    progress = params['progress']
    episode = get_episode(progress)

    x = params['x']
    y = params['y']
    speed = params['speed']
    track_width = params['track_width']
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    is_left_of_center = params['is_left_of_center']
    is_reversed = params['is_reversed']

    reward = 0.001

    if all_wheels_on_track == False:
        return reward

    # center
    distance_rate = distance_from_center / track_width

    if distance_rate < 0.5:
        reward = 1.0

    # speed
    if speed >= MIN_SPEED:
        # reverse
        if is_reversed:
            if is_left_of_center:
                is_left_of_center = False
            else:
                is_left_of_center = True

        # out-in-out
        if is_left_of_center:
            if x > 6.5:
                reward *= 1.5
            elif y > 3.5:
                reward *= 1.5
            elif x < 2.5 and y < 1.5:
                reward *= 1.5
        else:
            if x > 3.5 and x < 5.5 and y > 3.5:
                reward *= 1.5
            elif x < 2.5 and y > 2.0 and y < 3.0:
                reward *= 1.5

    # log
    params['log_key'] = 'mat-in-out-{}'.format(MAX_SPEED)
    params['episode'] = episode
    params['reward'] = reward
    print(json.dumps(params))

    return float(reward)
