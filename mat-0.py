
def reward_function(params):
    import json
    import math

    LOG_ENABLED = True

    CHK_SPEED = True
    CHK_STEER = True
    CHK_ANGLE = False

    MAX_SPEED = 5
    MIN_SPEED = MAX_SPEED * 0.5

    MAX_STEER = 15

    MAX_ANGLE = 15

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

    reward = 0.001

    speed = params['speed']
    heading = params['heading']
    steering = abs(params['steering_angle'])
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    closest_waypoints = params['closest_waypoints']
    waypoints = params['waypoints']

    # center
    distance_rate = distance_from_center / track_width

    if distance_rate <= 0.1:
        reward = 1.0
    elif distance_rate <= 0.2:
        reward = 0.5
    elif distance_rate <= 0.4:
        reward = 0.1

    # speed
    if CHK_SPEED and speed > MIN_SPEED:
        reward *= 1.5

    # steering
    if CHK_STEER and steering > MAX_STEER:
        reward *= 0.75

    # angle
    coor1 = waypoints[closest_waypoints[0]]
    coor2 = waypoints[closest_waypoints[1]]
    angle = math.atan2((coor2[1] - coor1[1]), (coor2[0] - coor1[0]))
    yaw = math.radians(heading)
    allow = math.radians(MAX_ANGLE)
    in_range = is_range(yaw, angle, allow)

    if CHK_ANGLE and in_range:
        reward *= 1.3

    # log
    if LOG_ENABLED:
        log_key = 'mat-{}'.format(MAX_SPEED)

        if CHK_STEER:
            log_key += '-s{}'.format(MAX_STEER)

        if CHK_ANGLE:
            log_key += '-a{}'.format(MAX_ANGLE)

        params['log_key'] = log_key
        params['yaw'] = yaw
        params['angle'] = angle
        params['in_range'] = in_range
        params['reward'] = reward
        print(json.dumps(params))

    return float(reward)
