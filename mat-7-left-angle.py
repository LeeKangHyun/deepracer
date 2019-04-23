import json
import math

CODE_NAME = 'left-angle'

MAX_SPEED = 2
MIN_SPEED = MAX_SPEED * 0.7

MAX_ANGLE = 5

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


def reward_function(params):
    all_wheels_on_track = params['all_wheels_on_track']
    progress = params['progress']

    speed = params['speed']

    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    is_left_of_center = params['is_left_of_center']
    is_reversed = params['is_reversed']

    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    reward = 0.001

    # episode
    episode, total = get_episode(progress)

    # angle
    coor1 = waypoints[closest_waypoints[0]]
    coor2 = waypoints[closest_waypoints[1]]
    guide = math.atan2((coor2[1] - coor1[1]), (coor2[0] - coor1[0]))
    yaw = math.radians(heading)
    allow = math.radians(MAX_ANGLE)
    diff = diff_angle(yaw, guide)

    if all_wheels_on_track == True:
        # speed
        if speed > MIN_SPEED and diff < allow:
            # center rate
            distance_score = 1.0 - (distance_from_center / (track_width / 2))
            angle_score = 1.0 - (diff / allow)

            # reverse
            if is_reversed:
                if is_left_of_center:
                    is_left_of_center = False
                else:
                    is_left_of_center = True

            # left and angle
            if is_left_of_center:
                reward = distance_score * angle_score

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
