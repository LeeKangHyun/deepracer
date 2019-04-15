
def reward_function(params):
    import json
    import math

    MAX_SPEED = 3
    MIN_SPEED = MAX_SPEED * 0.5

    MAX_STEER = 15

    reward = 0.001

    x = params['x']
    y = params['y']
    speed = params['speed']
    steering = abs(params['steering_angle'])
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    is_left_of_center = params['is_left_of_center']

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

    # out-in-out
    if is_left_of_center:
        if x > 6.0 or x < 2.0 or y > 4.0:
            reward *= 1.5
    else:
        if x > 4.0 and x < 5.0 and y > 2.0:
            reward *= 1.5

    # log
    params['log_key'] = 'mat-{}-{}'.format(MAX_SPEED, MAX_STEER)
    params['reward'] = reward
    print(json.dumps(params))

    return float(reward)
