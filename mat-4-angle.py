import json
import math

CODE_NAME = 'angle'

MAX_SPEED = 2
MIN_SPEED = MAX_SPEED * 0.7

MAX_ANGLE = 10

g_episode = 0
g_total = 0
g_prev = 0


def get_episode(progress):
    global g_episode
    global g_total
    global g_prev

    if g_episode == 0 or g_prev > progress:
        g_episode += 1
        g_total = 0

    g_prev = progress

    return g_episode, g_total


def diff_angle(yaw, guide):
    diff = (yaw - guide) % (2.0 * math.pi)

    if diff >= math.pi:
        diff -= 2.0 * math.pi

    return abs(diff)


def is_range(yaw, guide, allow):
    if diff_angle(yaw, guide) <= allow:
        return True
    return False


def reward_function(params):
    speed = params['speed']
    track_width = params['track_width']
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    heading = params['heading']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    progress = params['progress']

    reward = 0.001

    # episode
    episode, total = get_episode(progress)

    # angle
    coor1 = waypoints[closest_waypoints[0]]
    coor2 = waypoints[closest_waypoints[1]]
    guide = math.atan2((coor2[1] - coor1[1]), (coor2[0] - coor1[0]))
    yaw = math.radians(heading)
    diff = diff_angle(yaw, guide)

    if all_wheels_on_track == True:
        # speed
        if speed > MIN_SPEED:
            # score
            distance_score = 1.2 - (distance_from_center / (track_width / 2))
            angle_score = 2.0 - (diff * 10)

            reward = distance_score * angle_score

            if reward < 0.01:
                reward = 0.01

    total += reward

    # log
    params['log_key'] = '{}-{}-{}'.format(CODE_NAME, MAX_SPEED, MAX_ANGLE)
    params['episode'] = episode
    params['yaw'] = yaw
    params['guide'] = guide
    params['diff'] = diff
    params['reward'] = reward
    params['total'] = total
    print(json.dumps(params))

    return float(reward)
