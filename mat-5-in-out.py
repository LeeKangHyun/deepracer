
def reward_function(params):
    import json
    import math

    MAX_SPEED = 5
    MIN_SPEED = MAX_SPEED * 0.8

    x = params['x']
    y = params['y']
    speed = params['speed']
    track_width = params['track_width']
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    is_left_of_center = params['is_left_of_center']

    reward = 0.001

    if all_wheels_on_track:
        # center
        distance_rate = distance_from_center / track_width

        if distance_rate < 0.5:
            reward = 1.0

        # speed
        if speed > MIN_SPEED:
            reward *= 1.5

        # out-in-out
        if is_left_of_center:
            if x > 6.1 or x < 2.0 or y > 4.0:
                reward *= 1.5
        else:
            if x > 4.0 and x < 5.0 and y > 2.0:
                reward *= 1.5

    # log
    # params['log_key'] = 'mat-{}-{}'.format(MAX_SPEED, MAX_STEER)
    # params['reward'] = reward
    # print(json.dumps(params))

    return float(reward)
