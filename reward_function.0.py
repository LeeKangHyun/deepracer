
def reward_function(params):
    import json

    track_width = params['track_width']
    distance_from_center = params['distance_from_center']

    reward = 0.001

    distance_rate = distance_from_center / track_width

    if distance_rate <= 0.1:
        reward = 1.0
    elif distance_rate <= 0.2:
        reward = 0.5
    elif distance_rate <= 0.4:
        reward = 0.1

    params['log_key'] = 'MATDORI_STEP0'
    print(json.dumps(params))

    return float(reward)
