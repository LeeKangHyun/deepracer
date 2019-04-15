
def reward_function(params):
    import json
    import math

    MAX_SPEED = 5
    MIN_SPEED = MAX_SPEED * 0.8

    MAX_STEER = 15

    MAX_ANGLE = 10

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

    x = params['x']
    y = params['y']
    speed = params['speed']
    heading = params['heading']
    steering = abs(params['steering_angle'])
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    closest_waypoints = params['closest_waypoints']
    waypoints = params['waypoints']
    is_left_of_center = params['is_left_of_center']

    reward = 0.001

    # center
    distance_rate = distance_from_center / track_width

    # if distance_rate < 0.1:
    #     reward = 1.0
    # elif distance_rate < 0.2:
    #     reward = 0.5
    # elif distance_rate < 0.4:
    #     reward = 0.1

    if distance_rate < 0.5:
        reward = 1.0

    # speed
    if speed > MIN_SPEED:
        reward *= 1.5

    # steering
    if steering > MAX_STEER:
        reward *= 0.75

    # angle
    coor1 = waypoints[closest_waypoints[0]]
    coor2 = waypoints[closest_waypoints[1]]
    angle = math.atan2((coor2[1] - coor1[1]), (coor2[0] - coor1[0]))
    yaw = math.radians(heading)
    allow = math.radians(MAX_ANGLE)
    in_range = is_range(yaw, angle, allow)

    if in_range:
        reward *= 1.3

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
