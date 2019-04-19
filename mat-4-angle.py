import json
import math

CODE_NAME = 'angle'

MAX_SPEED = 2
MIN_SPEED = MAX_SPEED * 0.5

MAX_ANGLE = 10

g_episode = 0
g_total = 0
g_prev = 0


def get_episode(progress):
    global g_episode
    global g_total
    global g_prev

    if g_episode == 0 or g_prev > progress:
        g_episode += 1
        g_total = 0

    g_prev = progress

    return g_episode, g_total


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


def reward_function(params):
    speed = params['speed']
    track_width = params['track_width']
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    heading = params['heading']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    progress = params['progress']

    reward = 0.001

    # episode
    episode, total = get_episode(progress)

    # angle
    coor1 = waypoints[closest_waypoints[0]]
    coor2 = waypoints[closest_waypoints[1]]
    angle = math.atan2((coor2[1] - coor1[1]), (coor2[0] - coor1[0]))
    yaw = math.radians(heading)
    allow = math.radians(MAX_ANGLE)
    in_range = is_range(yaw, angle, allow)

    if all_wheels_on_track == True:
        # center
        distance_rate = distance_from_center / track_width

        if distance_rate <= 0.1:
            reward = 1.0
        elif distance_rate <= 0.2:
            reward = 0.5
        elif distance_rate <= 0.4:
            reward = 0.1

        # speed and angle
        if speed > MIN_SPEED and in_range:
            reward *= 2

    total += reward

    # log
    params['log_key'] = '{}-{}-{}'.format(CODE_NAME, MAX_SPEED, MAX_ANGLE)
    params['episode'] = episode
    params['yaw'] = yaw
    params['angle'] = angle
    params['in_range'] = in_range
    params['reward'] = reward
    params['total'] = total
    print(json.dumps(params))

    return float(reward)
