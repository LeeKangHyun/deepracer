
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

        # in
        if is_left_of_center:
            reward *= 1.5

    # log
    params['log_key'] = 'mat-in-out-{}'.format(MAX_SPEED)
    params['reward'] = reward
    print(json.dumps(params))

    return float(reward)
