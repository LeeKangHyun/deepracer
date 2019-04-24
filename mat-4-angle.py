import json
import math

CODE_NAME = 'angle'

MAX_SPEED = 2
MIN_SPEED = MAX_SPEED * 0.7

MAX_ANGLE = math.radians(5)

g_episode = 0
g_total = 0
g_prev = 0
g_bonus = 0


def get_episode(progress):
    global g_episode
    global g_total
    global g_prev
    global g_bonus

    if g_prev > progress:
        g_episode += 1
        g_total = 0
        g_bonus = 0
    else:
        if progress == 100:
            g_bonus = 0.5
        else:
            g_bonus = progress - g_prev

    g_prev = progress

    return g_episode


def diff_angle(yaw, angle):
    diff = (yaw - angle) % (2.0 * math.pi)

    if diff >= math.pi:
        diff -= 2.0 * math.pi

    return abs(diff)


def reward_function(params):
    global g_total
    global g_bonus

    all_wheels_on_track = params['all_wheels_on_track']
    progress = params['progress']

    speed = params['speed']

    track_width = params['track_width']
    distance_from_center = params['distance_from_center']

    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    reward = 0.001

    # episode
    episode = get_episode(progress)

    # angle
    coor1 = waypoints[closest_waypoints[0]]
    coor2 = waypoints[closest_waypoints[1]]
    angle = math.atan2((coor2[1] - coor1[1]), (coor2[0] - coor1[0]))
    yaw = math.radians(heading)
    diff = diff_angle(yaw, angle)

    if all_wheels_on_track == True:
        # speed
        if speed >= MIN_SPEED and diff <= MAX_ANGLE:
            # score
            distance_score = 1.1 - (distance_from_center / (track_width / 2))
            angle_score = 1.1 - (diff / MAX_ANGLE)

            reward = (distance_score * angle_score) + g_bonus

    g_total += reward

    # log
    params['log_key'] = '{}-{}-{}'.format(CODE_NAME, MAX_SPEED, MAX_ANGLE)
    params['episode'] = episode
    params['angle'] = angle
    params['yaw'] = yaw
    params['diff'] = diff
    params['reward'] = reward
    params['total'] = g_total
    print(json.dumps(params))

    return float(reward)
