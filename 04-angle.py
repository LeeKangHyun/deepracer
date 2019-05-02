import json
import math

CODE_NAME = 'angle'

MAX_ANGLE = 5
RAD_ANGLE = math.radians(MAX_ANGLE)

g_episode = 0
g_progress = float(0)
g_max_speed = float(0)
g_min_speed = float(0)
g_total = float(0)
g_steer = []


def get_episode(progress, speed):
    global g_episode
    global g_progress
    global g_max_speed
    global g_min_speed
    global g_total

    # reset
    if g_progress > progress:
        g_episode += 1
        g_total = float(0)
        del g_steer[:]

    # speed
    if g_max_speed < speed:
        g_max_speed = speed
        g_min_speed = speed * 0.7

    # prev progress
    g_progress = progress

    return g_episode


def get_diff_angle(coor1, coor2, heading, steering):
    # guide
    angle = math.atan2((coor2[1] - coor1[1]), (coor2[0] - coor1[0]))

    # car yaw
    # yaw = math.radians(heading)
    yaw = math.radians(heading + steering)

    diff = (yaw - angle) % (2.0 * math.pi)

    if diff >= math.pi:
        diff -= 2.0 * math.pi

    return abs(diff)


def reward_function(params):
    global g_total
    global g_min_speed

    all_wheels_on_track = params['all_wheels_on_track']
    progress = params['progress']

    speed = params['speed']

    track_width = params['track_width']
    distance_from_center = params['distance_from_center']

    heading = params['heading']
    steering = params['steering_angle']

    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    prev_waypoint = waypoints[closest_waypoints[0]]
    next_waypoint = waypoints[closest_waypoints[1]]

    reward = 0.001

    # episode
    episode = get_episode(progress, speed)

    # diff angle
    diff_angle = get_diff_angle(
        prev_waypoint, next_waypoint, heading, steering)

    if all_wheels_on_track == True:
        # distance
        reward = 1.2 - (distance_from_center / (track_width / 2))

        # bonus
        bonus = reward * 0.5

        # speed
        if speed >= g_min_speed:
            reward += bonus

        # diff angle
        if diff_angle <= RAD_ANGLE:
            reward += bonus

    g_total += reward

    # log
    params['log_key'] = '{}-{}'.format(CODE_NAME, MAX_ANGLE)
    params['episode'] = episode
    params['diff_angle'] = diff_angle
    params['reward'] = reward
    params['total'] = g_total
    print(json.dumps(params))

    return float(reward)
