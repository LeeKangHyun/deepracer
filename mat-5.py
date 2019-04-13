# mat-5


def reward_function(params):
    import json
    import math

    MAX_SPEED = 5
    MIN_SPEED = MAX_SPEED * 0.5
    CHK_SPEED = True

    MAX_ANGLE = 10
    CHK_ANGLE = True

    def is_range(yaw, angle, allow):
        in_range = False
        if angle > (math.pi - allow) or angle < (math.pi * -1) + allow:
            if yaw <= math.pi and yaw >= (angle - allow):
                in_range = True
            elif yaw >= (math.pi * -1) and yaw <= (angle + allow):
                in_range = True
        else:
            if yaw >= (angle - allow) and yaw <= (angle + allow):
                in_range = True
        return in_range

    speed = params['speed']
    heading = params['heading']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    closest_waypoints = params['closest_waypoints']
    waypoints = params['waypoints']

    distance_rate = distance_from_center / track_width

    coor1 = waypoints[closest_waypoints[0]]
    coor2 = waypoints[closest_waypoints[1]]
    angle = math.atan2((coor2[1] - coor1[1]), (coor2[0] - coor1[0]))
    yaw = math.radians(heading)
    allow = math.radians(MAX_ANGLE)
    in_range = is_range(yaw, angle, allow)

    reward = 0.001

    if distance_rate <= 0.1:
        reward = 1.0
    elif distance_rate <= 0.2:
        reward = 0.5
    elif distance_rate <= 0.4:
        reward = 0.1

    if CHK_ANGLE and in_range:
        reward *= 1.2

    if CHK_SPEED and speed < MIN_SPEED:
        reward *= 0.8

    params['log_key'] = 'mat-{}-{}'.format(MAX_SPEED, MAX_ANGLE)
    params['yaw'] = yaw
    params['angle'] = angle
    params['in_range'] = in_range
    params['reward'] = reward
    print(json.dumps(params))

    return float(reward)
