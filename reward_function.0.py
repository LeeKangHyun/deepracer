# reward_function 0

def reward_function(params):
    import json
    import math

    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    closest_waypoints = params['closest_waypoints']
    waypoints = params['waypoints']

    reward = 0.001

    distance_rate = distance_from_center / track_width

    if distance_rate <= 0.1:
        reward = 1.0
    elif distance_rate <= 0.2:
        reward = 0.5
    elif distance_rate <= 0.4:
        reward = 0.1

    coor1 = waypoints[closest_waypoints[0]]
    coor2 = waypoints[closest_waypoints[1]]
    suggest = math.atan2((coor2[1] - coor1[1]), (coor2[0] - coor1[0]))

    params['log_key'] = 'MATDORI_0'
    params['suggest'] = suggest
    print(json.dumps(params))

    return float(reward)
