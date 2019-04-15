
def reward_function(params):
    import json
    import math

    MAX_SPEED = 5
    MIN_SPEED = MAX_SPEED * 0.8

    speed = params['speed']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']

    reward = 0.001

    # center
    distance_rate = distance_from_center / track_width

    if distance_rate <= 0.1:
        reward = 1.0
    elif distance_rate <= 0.2:
        reward = 0.5
    elif distance_rate <= 0.4:
        reward = 0.1

    # speed
    if speed > MIN_SPEED:
        reward *= 1.5

    # log
    # params['log_key'] = 'mat-{}'.format(MAX_SPEED)
    # params['reward'] = reward
    # print(json.dumps(params))

    return float(reward)
