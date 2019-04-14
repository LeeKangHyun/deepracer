
def reward_function(params):
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']

    distance_rate = distance_from_center / track_width

    reward = 0.001

    if distance_rate <= 0.1:
        reward = 1.0
    elif distance_rate <= 0.2:
        reward = 0.5
    elif distance_rate <= 0.4:
        reward = 0.1

    return float(reward)
