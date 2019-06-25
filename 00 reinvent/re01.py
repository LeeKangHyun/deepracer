import json
import math
import time

NAME = 're01-80-i'
ACTION = '24 / 5 / 8.0 / 2'
HYPER = '256 / 0.00003 / 40'

SIGHT = 6

MAX_CENTER = 0.25

MAX_ANGLE = 10

MAX_STEER = 10
LEN_STEER = 2

MAX_SPEED = 5
MIN_SPEED = 3

BASE_REWARD = 1.2

g_episode = 0
g_max_steps = 500
g_progress = float(0)
g_steer = []
g_total = float(0)
g_start = float(0)
g_param = []


def get_episode(steps, progress):
    global g_episode
    global g_max_steps
    global g_progress
    global g_param

    # reset
    if steps == 0:
        g_episode += 1
        diff_progress = 0.00001

        if g_episode > 1:
            g_param['diff_progress'] = g_param['progress']
            g_param['progress'] = -1
            print(json.dumps(g_param))
    else:
        diff_progress = progress - g_progress

    # prev
    g_progress = progress

    if progress == 100 and steps < g_max_steps:
        g_max_steps = steps

    return g_episode, g_max_steps, diff_progress


def get_distance(coor1, coor2):
    return math.sqrt((coor1[0] - coor2[0]) * (coor1[0] - coor2[0]) + (coor1[1] - coor2[1]) * (coor1[1] - coor2[1]))


def get_diff_angle(coor1, coor2, heading, steering):
    # guide
    angle = math.atan2((coor2[1] - coor1[1]), (coor2[0] - coor1[0]))

    # car yaw
    # yaw = math.radians(heading)
    yaw = math.radians(heading + steering)

    diff = (yaw - angle) % (2.0 * math.pi)

    if diff >= math.pi:
        diff -= 2.0 * math.pi

    return math.degrees(abs(diff))


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
    global g_steer
    global g_total
    global g_start
    global g_param

    steps = params['steps']
    progress = params['progress']

    # track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    # all_wheels_on_track = params['all_wheels_on_track']

    heading = params['heading']
    steering = params['steering_angle']
    speed = params['speed']

    # x = params['x']
    # y = params['y']

    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    prev_waypoint = waypoints[closest_waypoints[0]]
    # next_waypoint = waypoints[closest_waypoints[1]]
    next_waypoint = waypoints[(closest_waypoints[1] + SIGHT) % len(waypoints)]

    closest_waypoint = closest_waypoints[1]

    # default
    reward = 0.00001

    # episode
    episode, max_steps, diff_progress = get_episode(steps, progress)

    # reset
    if steps == 0:
        del g_steer[:]
        g_total = float(0)
        g_start = time.time()

    # lap time
    lap_time = time.time() - g_start

    # distance
    distance = params['distance_from_center']

    # diff angle
    diff_angle = get_diff_angle(
        prev_waypoint, next_waypoint, heading, steering)

    # diff steering
    diff_steer = get_diff_steering(steering)
    abs_steer = abs(steering)

    if steps > 0:
        diff_steps = progress / steps
    else:
        diff_steps = 0

    # reward
    if distance_from_center < MAX_CENTER and speed > MIN_SPEED:
        reward = 1.0

        # # center bonus
        # reward += (BASE_REWARD - (distance / MAX_CENTER))

        # if distance < (MAX_CENTER * 0.3):
        #     reward *= 2.0

        # # angle bonus
        # if diff_angle <= MAX_ANGLE:
        #     reward += (BASE_REWARD - (diff_angle / MAX_ANGLE))

        # # steer bonus
        # if diff_steer <= MAX_STEER:
        #     reward += (BASE_REWARD - (diff_steer / MAX_STEER))

        # # progress bonus
        # if diff_steps > 0 and steps <= max_steps:
        #     reward += (diff_steps * 2)

        # # progress bonus
        # if diff_progress > 0 and steps <= max_steps:
        #     reward += (diff_progress * 2)

        # # progress bonus
        # if diff_progress > (90 / max_steps):
        #     reward += 1.0

        # speed bonus
        if speed > MAX_SPEED:
            reward *= 2.0

        # steer bonus
        if closest_waypoint >= 10 and closest_waypoint <= 24 and steering >= 0:  # left
            reward *= 1.0
        elif closest_waypoint >= 33 and closest_waypoint <= 34 and steering <= 0:  # right
            reward *= 1.0
        elif closest_waypoint >= 40 and closest_waypoint <= 42 and steering >= 0:  # left
            reward *= 1.0
        elif closest_waypoint >= 50 and closest_waypoint <= 52 and steering >= 0:  # left
            reward *= 1.0
        elif closest_waypoint >= 60 and closest_waypoint <= 67 and steering >= 0:  # left
            reward *= 1.0
        elif abs_steer <= MAX_STEER:
            reward *= 1.0
        else:
            reward *= 0.1

        # # speed bonus
        # if speed > MAX_SPEED:
        #     reward *= 2.0
        # elif x > 6.5:
        #     reward *= 1.0
        # elif x < 1.1 and y > 3.8:
        #     reward *= 1.0
        # elif x < 1.5 and y < 1.2:
        #     reward *= 1.0
        # else:
        #     reward *= 0.1

        # # steer panelity
        # if abs_steer > MAX_STEER:
        #     reward *= 0.5

        # # steps panelity
        # if steps > max_steps:
        #     reward *= 0.5

    # total reward
    g_total += reward

    # log
    params['name'] = NAME
    params['params'] = ACTION
    params['episode'] = episode
    params['closest'] = closest_waypoint
    params['distance'] = distance
    params['max_steps'] = max_steps
    params['diff_progress'] = diff_progress
    params['diff_angle'] = diff_angle
    params['diff_steer'] = diff_steer
    params['diff_steps'] = diff_steps
    params['abs_steer'] = abs_steer
    params['reward'] = reward
    params['total'] = g_total
    params['time'] = lap_time
    print(json.dumps(params))

    g_param = params

    return float(reward)
