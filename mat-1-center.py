
def reward_function(params):
    import json
    import math

    reward = 0.001

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

    # log
    params['log_key'] = 'mat-0'
    params['reward'] = reward
    print(json.dumps(params))

    return float(reward)