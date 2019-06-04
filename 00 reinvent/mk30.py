import json
import math
import time

NAME = 'mk30-f'
ACTION = '18 / 7 / 5 / 1'
HYPER = '512 / 0.999 / 40'

SIGHT = 1

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

    if distance < MAX_CENTER:
        # center bonus
        reward += (BASE_REWARD - (distance / MAX_CENTER)) * 2

        # angle bonus
        if diff_angle <= MAX_ANGLE:
            reward += (BASE_REWARD - (diff_angle / MAX_ANGLE))

        # # steer bonus
        # if diff_steer <= MAX_STEER:
        #     reward += (BASE_REWARD - (diff_steer / MAX_STEER))

        # # progress bonus
        # if diff_progress > 1:
        #     reward += diff_progress

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
    params['reward'] = reward
    params['total'] = g_total
    params['time'] = g_time
    print(json.dumps(params))

    return float(reward)


def get_waypoints():
    waypoints = []

    # re11 : 13.89231
    waypoints.append([6.55431, 2.74437])
    waypoints.append([6.40536, 2.77149])
    waypoints.append([6.28100, 2.79411])
    waypoints.append([6.13500, 2.80435])
    waypoints.append([5.98250, 2.80790])
    waypoints.append([5.82778, 2.81186])
    waypoints.append([5.67529, 2.81878])
    waypoints.append([5.51936, 2.82989])
    waypoints.append([5.36509, 2.84597])
    waypoints.append([5.20990, 2.87237])
    waypoints.append([5.05897, 2.90557])
    waypoints.append([4.91032, 2.94398])
    waypoints.append([4.76643, 2.99096])
    waypoints.append([4.62528, 3.04961])
    waypoints.append([4.48936, 3.11745])
    waypoints.append([4.36077, 3.19971])
    waypoints.append([4.23983, 3.29632])
    waypoints.append([4.12682, 3.40541])
    waypoints.append([4.01926, 3.52476])
    waypoints.append([3.91881, 3.63991])
    waypoints.append([3.81614, 3.75384])
    waypoints.append([3.70513, 3.86216])
    waypoints.append([3.58988, 3.96208])
    waypoints.append([3.47000, 4.05710])
    waypoints.append([3.34126, 4.13924])
    waypoints.append([3.20319, 4.21064])
    waypoints.append([3.06255, 4.26940])
    waypoints.append([2.91745, 4.31395])
    waypoints.append([2.76772, 4.34875])
    waypoints.append([2.61387, 4.37665])
    waypoints.append([2.45639, 4.39507])
    waypoints.append([2.30006, 4.40642])
    waypoints.append([2.15070, 4.40803])
    waypoints.append([1.99910, 4.39320])
    waypoints.append([1.85037, 4.36513])
    waypoints.append([1.70198, 4.32403])
    waypoints.append([1.56265, 4.26756])
    waypoints.append([1.42581, 4.19456])
    waypoints.append([1.29282, 4.10563])
    waypoints.append([1.17370, 4.00137])
    waypoints.append([1.07217, 3.88184])
    waypoints.append([0.98526, 3.74915])
    waypoints.append([0.91419, 3.60940])
    waypoints.append([0.85940, 3.46447])
    waypoints.append([0.81968, 3.31036])
    waypoints.append([0.79731, 3.15712])
    waypoints.append([0.79081, 3.00520])
    waypoints.append([0.79978, 2.84918])
    waypoints.append([0.82160, 2.69291])
    waypoints.append([0.84810, 2.54074])
    waypoints.append([0.87664, 2.38957])
    waypoints.append([0.91036, 2.23583])
    waypoints.append([0.94935, 2.08751])
    waypoints.append([0.99918, 1.94274])
    waypoints.append([1.06433, 1.80187])
    waypoints.append([1.13882, 1.67143])
    waypoints.append([1.22215, 1.54269])
    waypoints.append([1.31188, 1.41843])
    waypoints.append([1.41730, 1.30134])
    waypoints.append([1.53341, 1.19897])
    waypoints.append([1.66107, 1.11198])
    waypoints.append([1.79956, 1.03832])
    waypoints.append([1.94046, 0.98285])
    waypoints.append([2.09564, 0.94247])
    waypoints.append([2.25022, 0.91394])
    waypoints.append([2.40057, 0.89116])
    waypoints.append([2.55484, 0.87229])
    waypoints.append([2.70756, 0.85993])
    waypoints.append([2.85780, 0.85154])
    waypoints.append([3.01207, 0.83862])
    waypoints.append([3.16458, 0.81565])
    waypoints.append([3.31630, 0.78392])
    waypoints.append([3.46896, 0.75078])
    waypoints.append([3.61907, 0.71746])
    waypoints.append([3.77524, 0.67888])
    waypoints.append([3.92655, 0.63921])
    waypoints.append([4.07794, 0.60076])
    waypoints.append([4.22594, 0.56572])
    waypoints.append([4.37857, 0.53853])
    waypoints.append([4.53220, 0.52039])
    waypoints.append([4.68291, 0.50469])
    waypoints.append([4.83727, 0.49064])
    waypoints.append([4.99028, 0.47788])
    waypoints.append([5.14339, 0.46564])
    waypoints.append([5.29550, 0.45428])
    waypoints.append([5.45099, 0.44288])
    waypoints.append([5.60350, 0.43703])
    waypoints.append([5.75543, 0.44327])
    waypoints.append([5.91138, 0.46543])
    waypoints.append([6.06121, 0.50508])
    waypoints.append([6.20377, 0.55902])
    waypoints.append([6.33930, 0.62722])
    waypoints.append([6.47002, 0.71093])
    waypoints.append([6.59269, 0.80277])
    waypoints.append([6.71198, 0.90453])
    waypoints.append([6.82726, 1.01621])
    waypoints.append([6.92731, 1.13617])
    waypoints.append([7.01068, 1.26432])
    waypoints.append([7.08138, 1.40267])
    waypoints.append([7.13829, 1.54566])
    waypoints.append([7.18103, 1.69481])
    waypoints.append([7.20559, 1.84697])
    waypoints.append([7.20893, 2.00128])
    waypoints.append([7.19046, 2.15574])
    waypoints.append([7.15426, 2.30438])
    waypoints.append([7.05932, 2.44780])
    waypoints.append([6.93903, 2.55755])
    waypoints.append([6.74297, 2.68606])

    return waypoints
