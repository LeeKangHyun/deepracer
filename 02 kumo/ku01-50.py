import json
import math
import time

NAME = 'ku01-50-b'
ACTION = '30 / 7 / 5 / 1'
HYPER = '256 / 0.999 / 40'

SIGHT = 5

MAX_CENTER = 0.25

MAX_ANGLE = 10

MAX_STEER = 10
LEN_STEER = 2

MAX_STEPS = 100

BASE_REWARD = 1.2

g_episode = 0
g_progress = float(0)
g_steps = float(0)
g_steer = []
g_total = float(0)
g_start = float(0)
g_time = float(0)
g_param = []


def get_episode(progress, steps):
    global g_episode
    global g_progress
    global g_steps
    global g_steer
    global g_total
    global g_start
    global g_time
    global g_param

    diff_progress = progress - g_progress

    # reset
    if g_progress > progress:
        print('- episode reset - {} - {} - {} - {} - {}'.format(NAME, g_episode,
                                                                g_time, g_steps, g_progress))
        g_episode += 1
        g_total = float(0)
        g_start = time.time()
        del g_steer[:]

        if g_episode > 1:
            g_param['diff_progress'] = g_param['progress']
            g_param['progress'] = -1
            print(json.dumps(g_param))

    g_time = time.time() - g_start

    # completed
    if g_progress < progress and progress == 100:
        print('- episode completed - {} - {} - {} - {} - {}'.format(NAME, g_episode,
                                                                    g_time, steps, progress))

    # prev
    g_progress = progress
    g_steps = steps

    return g_episode, diff_progress


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
    global g_total
    global g_time
    global g_param

    steps = params['steps']
    progress = params['progress']

    # track_width = params['track_width']
    # distance_from_center = params['distance_from_center']
    all_wheels_on_track = params['all_wheels_on_track']

    heading = params['heading']
    steering = params['steering_angle']

    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    prev_waypoint = waypoints[closest_waypoints[0]]
    next_waypoint = waypoints[closest_waypoints[1]]

    # default
    reward = 0.00001

    # episode
    episode, diff_progress = get_episode(progress, steps)

    # distance
    distance = params['distance_from_center']

    # diff angle
    diff_angle = get_diff_angle(
        prev_waypoint, next_waypoint, heading, steering)

    # diff steering
    diff_steer = get_diff_steering(steering)
    abs_steer = abs(steering)

    # reward
    if all_wheels_on_track and distance < MAX_CENTER:
        # center bonus
        reward += (BASE_REWARD - (distance / MAX_CENTER))

        if distance < (MAX_CENTER * 0.3):
            reward *= 1.5

        # # angle bonus
        # if diff_angle <= MAX_ANGLE:
        #     reward += (BASE_REWARD - (diff_angle / MAX_ANGLE))

        # steer bonus
        if diff_steer <= MAX_STEER:
            reward += (BASE_REWARD - (diff_steer / MAX_STEER))

        # # steer panelity
        # if abs_steer > MAX_STEER:
        #     reward *= 0.5

        # progress bonus
        if diff_progress > 1:
            reward += diff_progress

    # total reward
    g_total += reward

    # log
    params['name'] = NAME
    params['params'] = ACTION
    params['episode'] = episode
    params['closest'] = closest_waypoints[1]
    params['distance'] = distance
    # params['destination'] = destination
    params['diff_progress'] = diff_progress
    params['diff_angle'] = diff_angle
    params['diff_steer'] = diff_steer
    params['abs_steer'] = abs_steer
    params['reward'] = reward
    params['total'] = g_total
    params['time'] = g_time
    print(json.dumps(params))

    g_param = params

    return float(reward)
