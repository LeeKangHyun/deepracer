import json
import math
import time

NAME = 'ku02'
ACTION = '27 / 7 / 5 / 1'
HYPER = '256 / 0.999 / 40'

SIGHT = 2

MAX_CENTER = 0.3

MAX_ANGLE = 10

MAX_STEER = 10
LEN_STEER = 2

MAX_STEPS = 100

BASE_REWARD = 1.2

g_episode = 0
g_progress = float(0)
g_steps = float(0)
g_waypoints = []
g_steer = []
g_total = float(0)
g_start = float(0)
g_time = float(0)


def get_episode(progress, steps):
    global g_episode
    global g_progress
    global g_steps
    global g_waypoints
    global g_steer
    global g_total
    global g_start
    global g_time

    diff_progress = progress - g_progress

    # reset
    if diff_progress < 0:
        print('- episode reset - {} - {} - {} - {} - {}'.format(NAME, g_episode,
                                                                g_time, g_steps, g_progress))
        g_episode += 1
        g_total = float(0)
        g_start = time.time()
        del g_steer[:]

    g_time = time.time() - g_start

    # completed
    if g_progress < progress and progress == 100:
        print('- episode completed - {} - {} - {} - {} - {}'.format(NAME, g_episode,
                                                                    g_time, steps, progress))

    # waypoints
    if len(g_waypoints) < 1:
        g_waypoints = get_waypoints()

    # prev
    g_progress = progress
    g_steps = steps

    return g_episode, diff_progress


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
    global g_total
    global g_time

    steps = params['steps']
    progress = params['progress']

    # track_width = params['track_width']
    # distance_from_center = params['distance_from_center']
    all_wheels_on_track = params['all_wheels_on_track']

    heading = params['heading']
    steering = params['steering_angle']

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
    episode, diff_progress = get_episode(progress, steps)

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
    params['closest'] = closest
    params['distance'] = distance
    params['destination'] = destination
    params['diff_progress'] = diff_progress
    params['diff_angle'] = diff_angle
    params['diff_steer'] = diff_steer
    params['abs_steer'] = abs_steer
    params['reward'] = reward
    params['total'] = g_total
    params['time'] = g_time
    print(json.dumps(params))

    return float(reward)


def get_waypoints():
    waypoints = []

    waypoints.append([3.24253, 4.10780])
    waypoints.append([3.06037, 4.22897])
    waypoints.append([2.80425, 4.30897])
    waypoints.append([2.52618, 4.35897])
    waypoints.append([2.30384, 4.38397])
    waypoints.append([2.11037, 4.39097])
    waypoints.append([1.92745, 4.35897])
    waypoints.append([1.75964, 4.32897])
    waypoints.append([1.59397, 4.26718])
    waypoints.append([1.43618, 4.15203])
    waypoints.append([1.29309, 4.02619])
    waypoints.append([1.15681, 3.88941])
    waypoints.append([1.03704, 3.74519])
    waypoints.append([0.93231, 3.57949])
    waypoints.append([0.85261, 3.40403])
    waypoints.append([0.79536, 3.21902])
    waypoints.append([0.76481, 3.03004])
    waypoints.append([0.76010, 2.83607])
    waypoints.append([0.77578, 2.64199])
    waypoints.append([0.80888, 2.45050])
    waypoints.append([0.85673, 2.26419])
    waypoints.append([0.91495, 2.07703])
    waypoints.append([0.97778, 1.89746])
    waypoints.append([1.05408, 1.72426])
    waypoints.append([1.14750, 1.55301])
    waypoints.append([1.25108, 1.39219])
    waypoints.append([1.37082, 1.24724])
    waypoints.append([1.51734, 1.11247])
    waypoints.append([1.68072, 0.99970])
    waypoints.append([1.84879, 0.91840])
    waypoints.append([2.03233, 0.86200])
    waypoints.append([2.21960, 0.82270])
    waypoints.append([2.41457, 0.79061])
    waypoints.append([2.59895, 0.76538])
    waypoints.append([2.78642, 0.74258])
    waypoints.append([2.97693, 0.72094])
    waypoints.append([3.16903, 0.69833])
    waypoints.append([3.35579, 0.67174])
    waypoints.append([3.54579, 0.64725])
    waypoints.append([3.73317, 0.62576])
    waypoints.append([3.92495, 0.60421])
    waypoints.append([4.11422, 0.58649])
    waypoints.append([4.30373, 0.57120])
    waypoints.append([4.53554, 0.55453])
    waypoints.append([4.72440, 0.53453])
    waypoints.append([4.91888, 0.50453])
    waypoints.append([5.10440, 0.50453])
    waypoints.append([5.29896, 0.50453])
    waypoints.append([5.49131, 0.50453])
    waypoints.append([5.68114, 0.52316])
    waypoints.append([5.87219, 0.56770])
    waypoints.append([6.05910, 0.62581])
    waypoints.append([6.23843, 0.69953])
    waypoints.append([6.40818, 0.78845])
    waypoints.append([6.56030, 0.89962])
    waypoints.append([6.69361, 1.03565])
    waypoints.append([6.80115, 1.19084])
    waypoints.append([6.88037, 1.35855])
    waypoints.append([6.93335, 1.54818])
    waypoints.append([6.95654, 1.73871])
    waypoints.append([6.94899, 1.93395])
    waypoints.append([6.90892, 2.12847])
    waypoints.append([6.83860, 2.31170])
    waypoints.append([6.74054, 2.48041])
    waypoints.append([6.61898, 2.62930])
    waypoints.append([6.47635, 2.75640])
    waypoints.append([6.29897, 2.79087])
    waypoints.append([6.13194, 2.82396])
    waypoints.append([5.94359, 2.85845])
    waypoints.append([5.75543, 2.88454])
    waypoints.append([5.56220, 2.90642])
    waypoints.append([5.36546, 2.92524])
    waypoints.append([5.17176, 2.94149])
    waypoints.append([4.98141, 2.96338])
    waypoints.append([4.79314, 2.99787])
    waypoints.append([4.58109, 3.05386])
    waypoints.append([4.35882, 3.17600])
    waypoints.append([4.18542, 3.26852])
    waypoints.append([4.02032, 3.37148])
    waypoints.append([3.86941, 3.48725])
    waypoints.append([3.73015, 3.61918])
    waypoints.append([3.60174, 3.76221])
    waypoints.append([3.46093, 3.94082])

    return waypoints
