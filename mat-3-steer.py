
def reward_function(params):
    import json
    import math

    MAX_SPEED = 5
    MIN_SPEED = MAX_SPEED * 0.8

    MAX_STEER = 15

    reward = 0.001

    speed = params['speed']
    steering = abs(params['steering_angle'])
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']

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

    # steering
    if steering > MAX_STEER:
        reward *= 0.75

    # log
    params['log_key'] = 'mat-{}-{}'.format(MAX_SPEED, MAX_STEER)
    params['reward'] = reward
    print(json.dumps(params))

    return float(reward)
