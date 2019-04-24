import json
import math

CODE_NAME = 'smooth'

MAX_ANGLE = math.radians(5)

MAX_STEER = 15
LEN_STEER = 2

g_progress = 0
g_episode = 0
g_speed = 0
g_total = 0
g_bonus = 0
g_steer = []


def get_episode(progress, speed):
    global g_progress
    global g_episode
    global g_speed
    global g_total
    global g_bonus

    # reset
    if g_progress > progress:
        g_episode += 1
        g_total = 0
        g_bonus = 0
        del g_steer[:]
    else:
        # bonus
        if progress == 100:
            g_bonus = 0.5
        else:
            g_bonus = progress - g_progress

    # max speed
    if g_speed < speed:
        g_speed = speed

    # prev progress
    g_progress = progress

    return g_episode


def get_diff_angle(coor1, coor2, heading):
    # guide
    angle = math.atan2((coor2[1] - coor1[1]), (coor2[0] - coor1[0]))

    # car yaw
    yaw = math.radians(heading)

    diff = (yaw - angle) % (2.0 * math.pi)

    if diff >= math.pi:
        diff -= 2.0 * math.pi

    return abs(diff)


def get_diff_steering(steering):
    global g_steer

    prev = -100
    diff = 0

    # steering list
    g_steer.append(steering)
    if len(g_steer) > LEN_STEER:
        del g_steer[0]

    # steering diff
    for v in g_steer:
        if prev > -100:
            diff += abs(prev - v)
        prev = v

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
    prev_waypoint = waypoints[closest_waypoints[0]]
    next_waypoint = waypoints[closest_waypoints[1]]
    heading = params['heading']

    reward = 0.001

    # episode
    episode = get_episode(progress, speed)

    # diff angle
    diff_angle = get_diff_angle(prev_waypoint, next_waypoint, heading)

    # diff steering
    diff_steer = get_diff_steering(steering_angle)

    if all_wheels_on_track == True:
        # speed
        min_speed = g_speed * 0.7

        # speed and steer and angle
        if speed >= min_speed and diff_steer <= MAX_STEER and diff_angle <= MAX_ANGLE:
            # score
            distance_score = 1.1 - (distance_from_center / (track_width / 2))
            angle_score = 1.1 - (diff_angle / MAX_ANGLE)

            reward = (distance_score * angle_score) + g_bonus

    g_total += reward

    # log
    params['log_key'] = CODE_NAME
    params['episode'] = episode
    params['diff_angle'] = diff_angle
    params['diff_steer'] = diff_steer
    params['reward'] = reward
    params['total'] = g_total
    print(json.dumps(params))

    return float(reward)
