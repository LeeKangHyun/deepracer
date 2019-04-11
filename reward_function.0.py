# reward_function 0

def reward_function(params):
    import json
    import math

    def is_range(yaw, suggest, allow):
        in_range = False
        if suggest > (math.pi - allow) or suggest < (math.pi * -1) + allow:
            if yaw <= math.pi and yaw >= (suggest - allow):
                in_range = True
            elif yaw >= (math.pi * -1) and yaw <= (suggest + allow):
                in_range = True
        else:
            if yaw >= (suggest - allow) and yaw <= (suggest + allow):
                in_range = True
        return in_range

    heading = params['heading']
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
    is_range = is_range(heading, suggest, math.radians(30))

    params['log_key'] = 'MATDORI_LOG'
    params['suggest'] = suggest
    params['is_range'] = is_range
    print(json.dumps(params))

    return float(reward)
