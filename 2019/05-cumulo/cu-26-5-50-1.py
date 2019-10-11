import json
import math
import time

NAME = "cu-26-5-50-1"

BASE_REWARD = 10.0

MAX_CENTER = 0.25

MAX_STEER = 30.0
MIN_STEER = 10.0
LEN_STEER = 2

MAX_SPEED = 8.0
MIN_SPEED = 3.0

g_episode = 0
g_progress = float(0)
g_total = float(0)
g_start = float(0)
g_steer = []
g_param = []


def get_episode(steps, progress):
    global g_episode
    global g_progress
    global g_param

    # reset
    if steps == 0:
        g_episode += 1
        diff_progress = 0.00001

        if g_episode > 1:
            g_param["diff_progress"] = g_param["progress"]
            g_param["progress"] = -1
            print(json.dumps(g_param))
    else:
        diff_progress = progress - g_progress

    # prev
    g_progress = progress

    return g_episode, diff_progress


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
    global g_start
    global g_steer
    global g_param

    steps = params["steps"]
    progress = params["progress"]

    steering = params["steering_angle"]
    speed = params["speed"]

    # episode
    episode, diff_progress = get_episode(steps, progress)

    # reset
    if steps == 0:
        g_total = float(0)
        g_start = time.time()
        del g_steer[:]

    # lap time
    lap_time = time.time() - g_start

    # distance
    distance = params["distance_from_center"]
    track_width = params["track_width"]
    track_half = track_width / 2.0

    # diff steering
    diff_steer = get_diff_steering(steering)

    # abs steering
    abs_steer = abs(steering)

    # reward
    reward = BASE_REWARD
    reward *= (track_half - (distance * 0.5)) / track_half
    reward *= ((MAX_STEER * 2.0) - (diff_steer * 0.5)) / (MAX_STEER * 2.0)
    # reward *= (MAX_STEER - (abs_steer * 0.5)) / MAX_STEER
    reward *= speed / MAX_SPEED

    if reward <= 0:
        reward = 0.00001

    # total reward
    g_total += reward

    # log
    params["name"] = NAME
    params["episode"] = episode
    params["diff_progress"] = diff_progress
    params["diff_steer"] = diff_steer
    params["abs_steer"] = abs_steer
    params["reward"] = reward
    params["total"] = g_total
    params["time"] = lap_time
    print(json.dumps(params))

    g_param = params

    return float(reward)
