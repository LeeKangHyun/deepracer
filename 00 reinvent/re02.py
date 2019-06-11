import json
import math
import time

NAME = 're02-5'
ACTION = '30 / 7 / 5 / 1'
HYPER = '256 / 0.999 / 40'

SIGHT = 1

MAX_CENTER = 0.3

MAX_ANGLE = 10

MAX_STEER = 10
LEN_STEER = 2

MAX_SPEED = 5

BASE_REWARD = 1.2

g_episode = 0
g_max_steps = 500
g_progress = float(0)
g_waypoints = []
g_steer = []
g_total = float(0)
g_start = float(0)


def get_episode(steps, progress):
    global g_episode
    global g_max_steps
    global g_progress

    # reset
    if steps == 0:
        g_episode += 1
        diff_progress = 0.00001
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

    index = closest + sight

    if index >= len(g_waypoints):
        index = index - len(g_waypoints)

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

    steps = params['steps']
    progress = params['progress']

    # track_width = params['track_width']
    # distance_from_center = params['distance_from_center']
    all_wheels_on_track = params['all_wheels_on_track']

    heading = params['heading']
    steering = params['steering_angle']
    # speed = params['speed']

    x = params['x']
    y = params['y']
    location = [x, y]

    # waypoints = params['waypoints']
    # closest_waypoints = params['closest_waypoints']
    # prev_waypoint = waypoints[closest_waypoints[0]]
    # next_waypoint = waypoints[closest_waypoints[1]]

    # default
    reward = 0.00001

    # episode
    episode, max_steps, diff_progress = get_episode(steps, progress)

    # reset
    if steps == 0:
        del g_steer[:]
        g_total = float(0)
        g_start = time.time()

    # lap rime
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
    if all_wheels_on_track and distance < MAX_CENTER:
        # center bonus
        reward += (BASE_REWARD - (distance / MAX_CENTER))

        if distance < (MAX_CENTER * 0.3):
            reward *= 1.5

        # # time bonus
        # if lap_time > 0:
        #     reward += (progress / lap_time * 10)

        # # speed bonus
        # if speed > 0:
        #     reward += (speed / MAX_SPEED)

        # # angle bonus
        # if diff_angle <= MAX_ANGLE:
        #     reward += (BASE_REWARD - (diff_angle / MAX_ANGLE))

        # # steer bonus
        # if diff_steer <= MAX_STEER:
        #     reward += (BASE_REWARD - (diff_steer / MAX_STEER))

        # # steer panelity
        # if abs_steer > MAX_STEER:
        #     reward *= 0.5

        # progress bonus
        if diff_steps > 0 and steps <= max_steps:
            reward += (diff_steps * 2)

        # progress bonus
        if diff_progress > 0 and steps <= max_steps:
            reward += (diff_progress * 2)

    # total reward
    g_total += reward

    # log
    params['name'] = NAME
    params['params'] = ACTION
    params['episode'] = episode
    params['closest'] = closest
    params['distance'] = distance
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

    return float(reward)


def get_waypoints():
    waypoints = []
    # re01-5
    waypoints.append([5.43638, 2.78755])
    waypoints.append([5.23127, 2.87217])
    waypoints.append([5.05186, 2.96391])
    waypoints.append([4.86540, 3.06448])
    waypoints.append([4.67951, 3.16473])
    waypoints.append([4.50179, 3.26559])
    waypoints.append([4.32895, 3.37909])
    waypoints.append([4.15319, 3.49836])
    waypoints.append([3.97832, 3.61676])
    waypoints.append([3.80203, 3.73292])
    waypoints.append([3.61786, 3.84176])
    waypoints.append([3.43467, 3.94329])
    waypoints.append([3.24966, 4.04535])
    waypoints.append([3.05691, 4.15042])
    waypoints.append([2.86847, 4.24460])
    waypoints.append([2.67530, 4.32777])
    waypoints.append([2.48104, 4.39300])
    waypoints.append([2.28451, 4.42936])
    waypoints.append([2.07978, 4.43869])
    waypoints.append([1.88056, 4.41171])
    waypoints.append([1.69313, 4.35565])
    waypoints.append([1.50739, 4.27086])
    waypoints.append([1.34753, 4.15846])
    waypoints.append([1.21114, 4.01601])
    waypoints.append([1.10104, 3.84779])
    waypoints.append([1.01915, 3.66130])
    waypoints.append([0.97010, 3.47089])
    waypoints.append([0.94418, 3.26779])
    waypoints.append([0.94847, 3.07007])
    waypoints.append([0.98019, 2.87041])
    waypoints.append([1.02432, 2.67065])
    waypoints.append([1.07700, 2.46704])
    waypoints.append([1.12928, 2.26244])
    waypoints.append([1.18031, 2.05918])
    waypoints.append([1.23216, 1.85279])
    waypoints.append([1.29145, 1.64719])
    waypoints.append([1.36971, 1.45292])
    waypoints.append([1.46716, 1.27048])
    waypoints.append([1.58194, 1.10122])
    waypoints.append([1.72198, 0.95440])
    waypoints.append([1.88439, 0.82990])
    waypoints.append([2.05718, 0.73226])
    waypoints.append([2.24235, 0.65948])
    waypoints.append([2.44506, 0.62713])
    waypoints.append([2.64360, 0.62713])
    waypoints.append([2.84994, 0.62713])
    waypoints.append([3.05867, 0.62713])
    waypoints.append([3.26479, 0.62713])
    waypoints.append([3.46990, 0.62713])
    waypoints.append([3.68135, 0.62713])
    waypoints.append([3.88978, 0.62713])
    waypoints.append([4.09455, 0.62713])
    waypoints.append([4.30165, 0.62713])
    waypoints.append([4.50681, 0.62713])
    waypoints.append([4.71168, 0.62713])
    waypoints.append([4.91660, 0.62713])
    waypoints.append([5.11920, 0.62713])
    waypoints.append([5.32138, 0.62713])
    waypoints.append([5.52080, 0.62713])
    waypoints.append([5.72394, 0.62713])
    waypoints.append([5.93302, 0.62713])
    waypoints.append([6.13864, 0.62713])
    waypoints.append([6.33390, 0.65860])
    waypoints.append([6.51916, 0.72767])
    waypoints.append([6.68570, 0.83263])
    waypoints.append([6.82745, 0.97075])
    waypoints.append([6.93587, 1.13408])
    waypoints.append([7.00750, 1.31626])
    waypoints.append([7.03980, 1.51233])
    waypoints.append([7.02791, 1.72316])
    waypoints.append([6.97677, 1.90737])
    waypoints.append([6.88395, 2.08670])
    waypoints.append([6.76019, 2.23858])
    waypoints.append([6.60831, 2.36283])
    waypoints.append([6.43455, 2.45536])
    waypoints.append([6.24154, 2.52972])
    waypoints.append([6.04822, 2.59499])
    waypoints.append([5.84790, 2.65178])
    waypoints.append([5.64647, 2.70959])

    return waypoints
