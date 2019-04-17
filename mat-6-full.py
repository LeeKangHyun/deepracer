
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
    steering = abs(params['steering_angle'])
    track_width = params['track_width']
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    heading = params['heading']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    is_left_of_center = params['is_left_of_center']
    is_reversed = params['is_reversed']

    reward = 0.001

    if all_wheels_on_track:
        # center
        distance_rate = distance_from_center / track_width

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

        # reverse
        if is_reversed:
            if is_left_of_center:
                is_left_of_center = False
            else:
                is_left_of_center = True

        # out-in-out
        if is_left_of_center:
            if x > 6.5:
                reward *= 1.5
            elif y > 3.5:
                reward *= 1.5
            elif x < 2.5 and y < 1.5:
                reward *= 1.5
        else:
            if x > 3.5 and x < 5.5 and y > 3.5:
                reward *= 1.5
            elif x < 2.5 and y > 2.0 and y < 3.0:
                reward *= 1.5

    # log
    # params['log_key'] = 'mat-{}-{}'.format(MAX_SPEED, MAX_STEER)
    # params['reward'] = reward
    # print(json.dumps(params))

    return float(reward)
