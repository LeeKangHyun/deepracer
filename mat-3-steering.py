import json
import math

CODE_NAME = 'steering'

MAX_SPEED = 2
MIN_SPEED = MAX_SPEED * 0.7

MAX_STEER = 15

g_episode = 0
g_total = 0
g_prev = 0


def get_episode(progress):
    global g_episode
    global g_total
    global g_prev

    if g_prev > progress:
        g_episode += 1
        g_total = 0

    g_prev = progress

    return g_episode


def reward_function(params):
    global g_total

    all_wheels_on_track = params['all_wheels_on_track']
    progress = params['progress']

    speed = params['speed']

    track_width = params['track_width']
    distance_from_center = params['distance_from_center']

    steering = abs(params['steering_angle'])

    reward = 0.001

    # episode
    episode = get_episode(progress)

    if all_wheels_on_track == True:
        # center
        distance_rate = distance_from_center / track_width

        if distance_rate <= 0.1:
            reward = 1.0
        elif distance_rate <= 0.2:
            reward = 0.5
        elif distance_rate <= 0.4:
            reward = 0.1

        # speed and steering
        if speed > MIN_SPEED and steering < MAX_STEER:
            reward *= 1.5

    g_total += reward

    # log
    params['log_key'] = '{}-{}-{}'.format(CODE_NAME, MAX_SPEED, MAX_STEER)
    params['episode'] = episode
    params['reward'] = reward
    params['total'] = g_total
    print(json.dumps(params))

    return float(reward)
