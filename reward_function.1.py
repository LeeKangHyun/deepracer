# reward_function 1

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

    distance_rate = distance_from_center / track_width

    coor1 = waypoints[closest_waypoints[0]]
    coor2 = waypoints[closest_waypoints[1]]
    suggest = math.atan2((coor2[1] - coor1[1]), (coor2[0] - coor1[0]))
    yaw = math.radians(heading)
    allow = math.radians(15)
    in_range = is_range(yaw, suggest, allow)

    reward = 0.001

    if distance_rate <= 0.1:
        reward = 1.0

        # if in_range:
        #     reward += 0.3
        # else:
        #     reward -= 0.2

    elif distance_rate <= 0.2:
        reward = 0.5
    elif distance_rate <= 0.4:
        reward = 0.1

    params['log_key'] = 'MATDORI_STEP1'
    params['yaw'] = yaw
    params['suggest'] = suggest
    params['in_range'] = in_range
    params['reward'] = reward
    print(json.dumps(params))

    return float(reward)
