import json
import math
import time

NAME = "em02-50-f"
ACTION = "24 / 5 / 5.0 / 1"
HYPER = "256 / 0.00003 / 40"

MIN_SIGHT = 2
MAX_SIGHT = 4

MIN_ANGLE = 6.0

MAX_SPEED = 5.0
MIN_SPEED = 3.0

MAX_STEER = 20.0
MIN_STEER = 13.0

MIN_PROGRESS = 0.6

g_episode = 0
g_progress = float(0)
g_total = float(0)
g_start = float(0)
g_param = []


def get_episode(steps, progress):
    global g_episode
    global g_progress
    global g_total
    global g_start
    global g_param

    # reset
    if steps == 0:
        g_episode += 1
        g_total = float(0)
        g_start = time.time()
        diff_progress = 0.00001

        if g_episode > 1:
            g_param["diff_progress"] = g_param["progress"]
            g_param["progress"] = -1
            print(json.dumps(g_param))
    else:
        diff_progress = progress - g_progress

    # prev
    g_progress = progress

    # lap time
    lap_time = time.time() - g_start

    return g_episode, diff_progress, lap_time


def get_angel(coor1, coor2):
    return math.atan2((coor2[1] - coor1[1]), (coor2[0] - coor1[0]))


def get_diff_angle(coor1, coor2, coor3):
    angle1 = get_angel(coor1, coor2)
    angle2 = get_angel(coor1, coor3)

    diff = (angle2 - angle1) % (2.0 * math.pi)

    if diff >= math.pi:
        diff -= 2.0 * math.pi

    return math.degrees(diff)


def reward_function(params):
    global g_total
    global g_param

    steps = params["steps"]
    progress = params["progress"]

    # track_width = params['track_width']
    # distance_from_center = params['distance_from_center']
    # all_wheels_on_track = params['all_wheels_on_track']

    speed = params["speed"]
    steering = params["steering_angle"]
    # heading = params['heading']

    waypoints = params["waypoints"]
    closest_waypoints = params["closest_waypoints"]
    next0 = waypoints[closest_waypoints[1]]
    next1 = waypoints[(closest_waypoints[1] + MIN_SIGHT) % len(waypoints)]
    next2 = waypoints[(closest_waypoints[1] + MAX_SIGHT) % len(waypoints)]

    # default
    reward = 0.00001

    # episode
    episode, diff_progress, lap_time = get_episode(steps, progress)

    # distance
    distance = params["distance_from_center"]

    # diff angle
    diff_angle = get_diff_angle(next0, next1, next2)

    # direction
    direction = -1

    # reward
    if speed > MIN_SPEED:
        reward = 1.0

        # # progress bonus
        # if diff_progress > MIN_PROGRESS:
        #     reward *= 2.0

        # speed bonus
        if speed > MAX_SPEED and abs(steering) < MIN_STEER:
            direction = 0
            reward *= 2.0

        # angle bonus
        if abs(diff_angle) <= MIN_ANGLE and abs(steering) < MIN_STEER:
            direction = 1
            reward *= 1.0

        elif diff_angle > MIN_ANGLE and steering >= 0:
            direction = 2
            reward *= 1.0

        elif diff_angle < (MIN_ANGLE * -1) and steering <= 0:
            direction = 3
            reward *= 1.0

        else:
            reward *= 0.1

    # total reward
    g_total += reward

    # log
    params["name"] = NAME
    params["params"] = ACTION
    params["episode"] = episode
    params["distance"] = distance
    params["diff_progress"] = diff_progress
    params["diff_angle"] = diff_angle
    params["direction"] = direction
    params["reward"] = reward
    params["total"] = g_total
    params["time"] = lap_time
    print(json.dumps(params))

    g_param = params

    return float(reward)
