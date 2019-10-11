import json
import math

CODE_NAME = "steering"

MAX_STEER = 15

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


def reward_function(params):
    global g_total
    global g_min_speed

    all_wheels_on_track = params["all_wheels_on_track"]
    progress = params["progress"]

    speed = params["speed"]

    track_width = params["track_width"]
    distance_from_center = params["distance_from_center"]

    steering = abs(params["steering_angle"])

    # episode
    episode = get_episode(progress)

    # reward
    reward = 0.001

    if all_wheels_on_track == True:
        # center
        distance_rate = distance_from_center / track_width

        if distance_rate <= 0.1:
            reward = 1.0
        elif distance_rate <= 0.2:
            reward = 0.5
        elif distance_rate <= 0.4:
            reward = 0.1

        # bonus
        bonus = reward * 0.5

        # speed
        if speed >= g_min_speed:
            reward += bonus

        # steering
        if steering < MAX_STEER:
            reward += bonus

    g_total += reward

    # log
    params["log_key"] = "{}-{}".format(CODE_NAME, MAX_STEER)
    params["log_key"] = CODE_NAME
    params["episode"] = episode
    params["reward"] = reward
    params["total"] = g_total
    print(json.dumps(params))

    return float(reward)
