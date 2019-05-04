import json
import math

CODE_NAME = 'london'

SIGHT = 0.5

BASE_REWARD = 1.2

MAX_ANGLE = 5
RAD_ANGLE = math.radians(MAX_ANGLE)

MAX_STEER = 5
LEN_STEER = 5

MAX_STEPS = 200

g_episode = 0
g_progress = float(0)
g_completed = False
g_max_speed = float(0)
g_total = float(0)
g_steer = []


def get_episode(progress, speed):
    global g_episode
    global g_progress
    global g_completed
    global g_max_speed
    global g_total
    global g_steer

    # reset
    if g_progress > progress:
        g_episode += 1
        g_total = float(0)
        del g_steer[:]

    # completed
    if g_progress < progress and progress == 100:
        g_completed = True
    else:
        g_completed = False

    # speed
    if g_max_speed < speed:
        g_max_speed = speed

    # prev progress
    g_progress = progress

    return g_episode, g_completed


def get_distance(coor1, coor2):
    return math.sqrt((coor1[0] - coor2[0]) * (coor1[0] - coor2[0]) + (coor1[1] - coor2[1]) * (coor1[1] - coor2[1]))


def get_next_point(waypoints, this_point, closest, distance):
    next_index = closest
    next_point = []

    while True:
        next_point = waypoints[next_index]

        dist = get_distance(this_point, next_point)
        if dist >= distance:
            break

        next_index += 1
        if next_index >= len(waypoints):
            next_index = next_index - len(waypoints)

    return next_point


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

    diff = diff / (LEN_STEER - 1)

    return diff


def reward_function(params):
    global g_max_speed
    global g_total

    steps = params['steps']
    progress = params['progress']

    all_wheels_on_track = params['all_wheels_on_track']

    speed = params['speed']

    track_width = params['track_width']
    distance_from_center = params['distance_from_center']

    heading = params['heading']
    steering = params['steering_angle']

    x = params['x']
    y = params['y']

    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    # prev_waypoint = waypoints[closest_waypoints[0]]
    # next_waypoint = waypoints[closest_waypoints[1]]

    # default
    reward = 0.001

    # episode
    episode, completed = get_episode(progress, speed)

    # point
    this_point = [x, y]
    next_point = get_next_point(
        waypoints, this_point, closest_waypoints[1], SIGHT)

    # diff angle
    diff_angle = get_diff_angle(
        this_point, next_point, heading, steering)

    # diff steering
    diff_steer = get_diff_steering(steering)

    if all_wheels_on_track == True:
        # complete bonus
        if completed == True and steps < MAX_STEPS:
            # reward += (MAX_STEPS - steps)
            reward += (steps / MAX_STEPS)

        if diff_angle <= RAD_ANGLE and diff_steer <= MAX_STEER:
            # diff angle
            reward += (BASE_REWARD - (diff_angle / RAD_ANGLE))

            # diff steering
            reward += (BASE_REWARD - (diff_steer / MAX_STEER))

            # center
            reward += (BASE_REWARD - (distance_from_center / (track_width / 2)))

            # speed bonus
            if g_max_speed > 0:
                reward += (speed / g_max_speed)

            # steps bonus
            if steps > 0:
                reward += (progress / steps)

    g_total += reward

    # log
    params['log_key'] = CODE_NAME
    params['episode'] = episode
    params['diff_angle'] = diff_angle
    params['diff_steer'] = diff_steer
    params['next_point'] = next_point
    params['reward'] = reward
    params['total'] = g_total
    print(json.dumps(params))

    return float(reward)
