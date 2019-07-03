import json
import math
import time

NAME = 're03-80-c-gen2-b'
ACTION = '24 / 5 / 8.0 / 2'
HYPER = '256 / 0.00003 / 40'

SIGHT = 2

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
g_waypoints = []
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


def get_closest_waypoint(location):
    global g_waypoints

    # 모든 waypoint 와의 거리 배열
    dist_list = []
    for waypoint in g_waypoints:
        dist_list.append(get_distance(waypoint, location))

    index = 0
    closest = 0
    min_dist = float('inf')

    # 가장 가까운 waypoint
    for dist in dist_list:
        if dist < min_dist:
            min_dist = dist
            closest = index
        index += 1

    # 가장 가까운 waypoint 하나 전
    prev_index = closest - 1
    if prev_index < 0:
        prev_index = len(g_waypoints) - 1

    dist1 = dist_list[prev_index]
    dist2 = get_distance(g_waypoints[prev_index], g_waypoints[closest])

    # 차량 바로 앞의 waypoint
    if dist1 > dist2:
        closest = closest + 1
        if closest >= len(g_waypoints):
            closest = closest - len(g_waypoints)

    # 차량 바로 뒤의 waypoint
    closest2 = closest - 1
    if closest2 < 0:
        closest2 = len(g_waypoints) - 1

    # 3개 점의 거리
    dist1 = dist_list[closest]
    dist2 = dist_list[closest2]
    dist3 = get_distance(g_waypoints[closest], g_waypoints[closest2])

    # 삼각형의 높이 구하기 (가장 가까운 거리)
    x = ((dist1 * dist1) - (dist2 * dist2) + (dist3 * dist3)) / (dist3 * 2)
    h = math.sqrt((dist1 * dist1) - (x * x))

    return closest, h


def get_distance(coor1, coor2):
    return math.sqrt((coor1[0] - coor2[0]) * (coor1[0] - coor2[0]) + (coor1[1] - coor2[1]) * (coor1[1] - coor2[1]))


def get_destination(closest, sight):
    global g_waypoints

    index = (closest + sight) % len(g_waypoints)

    return g_waypoints[index]


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
    global g_waypoints
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

    x = params['x']
    y = params['y']
    location = [x, y]

    # waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    # prev_waypoint = waypoints[closest_waypoints[0]]
    # next_waypoint = waypoints[closest_waypoints[1]]
    # next_waypoint = waypoints[(closest_waypoints[1] + SIGHT) % len(waypoints)]

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

    # waypoints
    if len(g_waypoints) < 1:
        g_waypoints = get_waypoints()

    # closest waypoint
    closest, distance = get_closest_waypoint(location)

    # point
    destination = get_destination(closest, SIGHT)

    # diff angle
    diff_angle = get_diff_angle(
        g_waypoints[closest], destination, heading, steering)

    # diff steering
    diff_steer = get_diff_steering(steering)
    abs_steer = abs(steering)

    if steps > 0:
        diff_steps = progress / steps
    else:
        diff_steps = 0

    # reward
    if distance_from_center < MAX_CENTER and speed > MIN_SPEED:
        # center bonus
        # reward += (BASE_REWARD - (distance / MAX_CENTER))
        reward = 1.0

        if distance < (MAX_CENTER * 0.3):
            reward *= 2.0

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

        # progress bonus
        if diff_progress > 0.7:
            reward += 1.0

        # speed bonus
        if speed > MAX_SPEED:
            reward *= 2.0
        elif closest_waypoint >= 11 and closest_waypoint <= 24:
            reward *= 1.0
        elif closest_waypoint >= 41 and closest_waypoint <= 42:
            reward *= 1.0
        elif closest_waypoint >= 51 and closest_waypoint <= 52:
            reward *= 1.0
        elif closest_waypoint >= 62 and closest_waypoint <= 67:
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
    params['closest'] = closest
    params['distance'] = distance
    params['max_steps'] = max_steps
    params['destination'] = destination
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


def get_waypoints():
    waypoints = []
    # re02-5-5
    waypoints.append([5.43071, 2.80230])
    waypoints.append([5.16804, 2.84078])
    waypoints.append([4.96455, 2.90833])
    waypoints.append([4.77464, 2.99941])
    waypoints.append([4.57747, 3.10608])
    waypoints.append([4.38708, 3.21749])
    waypoints.append([4.21180, 3.33754])
    waypoints.append([4.03489, 3.46878])
    waypoints.append([3.85774, 3.59565])
    waypoints.append([3.67189, 3.72081])
    waypoints.append([3.48923, 3.83945])
    waypoints.append([3.30132, 3.95916])
    waypoints.append([3.12407, 4.07969])
    waypoints.append([2.93798, 4.20203])
    waypoints.append([2.74186, 4.31141])
    waypoints.append([2.54641, 4.40900])
    waypoints.append([2.35025, 4.48177])
    waypoints.append([2.14150, 4.52780])
    waypoints.append([1.93272, 4.53286])
    waypoints.append([1.73383, 4.49599])
    waypoints.append([1.53868, 4.41331])
    waypoints.append([1.37071, 4.29213])
    waypoints.append([1.23665, 4.14057])
    waypoints.append([1.11794, 3.96425])
    waypoints.append([1.02298, 3.77300])
    waypoints.append([0.95876, 3.56911])
    waypoints.append([0.92171, 3.36056])
    waypoints.append([0.89507, 3.14507])
    waypoints.append([0.87280, 2.92892])
    waypoints.append([0.86328, 2.70969])
    waypoints.append([0.86657, 2.49030])
    waypoints.append([0.89457, 2.27760])
    waypoints.append([0.94408, 2.06711])
    waypoints.append([1.02285, 1.86996])
    waypoints.append([1.12619, 1.68837])
    waypoints.append([1.25077, 1.50615])
    waypoints.append([1.39130, 1.32522])
    waypoints.append([1.52681, 1.16213])
    waypoints.append([1.68763, 1.01690])
    waypoints.append([1.86037, 0.89273])
    waypoints.append([2.03473, 0.78986])
    waypoints.append([2.24205, 0.69781])
    waypoints.append([2.44374, 0.63929])
    waypoints.append([2.66634, 0.59569])
    waypoints.append([2.87307, 0.58032])
    waypoints.append([3.09022, 0.57641])
    waypoints.append([3.30573, 0.57641])
    waypoints.append([3.52530, 0.57641])
    waypoints.append([3.74238, 0.57641])
    waypoints.append([3.95890, 0.57641])
    waypoints.append([4.17035, 0.57641])
    waypoints.append([4.38774, 0.57641])
    waypoints.append([4.60328, 0.57641])
    waypoints.append([4.82003, 0.57641])
    waypoints.append([5.03520, 0.57641])
    waypoints.append([5.25278, 0.57641])
    waypoints.append([5.46939, 0.57641])
    waypoints.append([5.68860, 0.56684])
    waypoints.append([5.90438, 0.59667])
    waypoints.append([6.11413, 0.64439])
    waypoints.append([6.32120, 0.70992])
    waypoints.append([6.51308, 0.80790])
    waypoints.append([6.67325, 0.93156])
    waypoints.append([6.81082, 1.08905])
    waypoints.append([6.91320, 1.26909])
    waypoints.append([6.97702, 1.46944])
    waypoints.append([6.99673, 1.67736])
    waypoints.append([6.97358, 1.87856])
    waypoints.append([6.90588, 2.08201])
    waypoints.append([6.80610, 2.25426])
    waypoints.append([6.66276, 2.41444])
    waypoints.append([6.49690, 2.53522])
    waypoints.append([6.30789, 2.62892])
    waypoints.append([6.11167, 2.69020])
    waypoints.append([5.90114, 2.72931])
    waypoints.append([5.68849, 2.74923])

    return waypoints
