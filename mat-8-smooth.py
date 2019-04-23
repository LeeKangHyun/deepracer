import json
import math

CODE_NAME = 'smooth'

MAX_SPEED = 2
MIN_SPEED = MAX_SPEED * 0.7

MAX_ANGLE = 5

MAX_STEER = 30

g_episode = 0
g_total = 0
g_prev = 0
g_bonus = 0
g_steering = []


def get_episode(progress):
    global g_episode
    global g_total
    global g_prev
    global g_bonus
    global g_steering

    # reset
    if g_prev > progress:
        g_episode += 1
        g_total = 0
        g_bonus = 0
        g_steering = []
    else:
        # bonus
        if progress == 100:
            g_bonus = 0.5
        else:
            g_bonus = progress - g_prev

    # prev progress
    g_prev = progress

    return g_episode


def diff_angle(yaw, angle):
    diff = (yaw - angle) % (2.0 * math.pi)

    if diff >= math.pi:
        diff -= 2.0 * math.pi

    return abs(diff)


def diff_steering(steering):
    global g_steering

    prev = 0
    diff = 0

    # steering list
    g_steering.append(steering)
    if len(g_steering) > 10:
        g_steering.remove(0)

    # steering diff
    for steering in g_steering:
        diff += abs(prev - steering)
        prev = steering

    return diff


def reward_function(params):
    global g_total
    global g_bonus

    all_wheels_on_track = params['all_wheels_on_track']
    progress = params['progress']

    speed = params['speed']

    track_width = params['track_width']
    distance_from_center = params['distance_from_center']

    steering_angle = params['steering_angle']

    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    reward = 0.001

    # episode
    episode = get_episode(progress)

    # diff steering
    steer = diff_steering(steering_angle)

    # diff angle
    coor1 = waypoints[closest_waypoints[0]]
    coor2 = waypoints[closest_waypoints[1]]
    angle = math.atan2((coor2[1] - coor1[1]), (coor2[0] - coor1[0]))
    yaw = math.radians(heading)
    allow = math.radians(MAX_ANGLE)
    diff = diff_angle(yaw, angle)

    if all_wheels_on_track == True:
        # speed and steer and angle
        if speed >= MIN_SPEED and steer <= MAX_STEER and diff <= allow:
            # score
            distance_score = 1.0 - (distance_from_center / (track_width / 2))
            angle_score = 1.0 - (diff / allow)

            reward = (distance_score * angle_score) + g_bonus

    g_total += reward

    # log
    params['log_key'] = '{}-{}-{}'.format(CODE_NAME, MAX_SPEED, MAX_ANGLE)
    params['episode'] = episode
    params['angle'] = angle
    params['yaw'] = yaw
    params['diff'] = diff
    params['steer'] = steer
    params['reward'] = reward
    params['total'] = g_total
    print(json.dumps(params))

    return float(reward)
