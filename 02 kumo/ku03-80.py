import json
import math
import time

NAME = 'ku03-80-k'
ACTION = '24 / 5 / 8.0 / 2'
HYPER = '256 / 0.00001 / 40'

SIGHT = 6

MAX_CENTER = 0.25

MAX_STEER = 21.0
MIN_STEER = 13.0
LEN_STEER = 2

MAX_SPEED = 6.0
MIN_SPEED = 3.0

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


def get_rules(index):
    # 0 : any direction
    # 1 : straight
    # 2 : left
    # 3 : right

    # rules = [
    #     1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  # 0
    #     1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    #     1, 1, 1, 1, 1, 2, 2, 2, 2, 2,
    #     2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    #     0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
    #     1, 1, 1, 1, 1, 1, 0, 0, 0, 0,  # 50
    #     0, 0, 2, 2, 2, 2, 2, 2, 2, 2,
    #     2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    #     2, 2, 0, 0, 0, 0, 0, 3, 3, 3,
    #     3, 3, 3, 3, 3, 3, 3, 3, 0, 0,
    #     0, 0, 0, 1, 1, 1, 1, 1, 1, 1,  # 100
    #     1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    #     1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    #     2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    #     2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    #     2, 2, 2, 2, 2, 2, 2, 2, 2, 2,  # 150
    #     2, 1, 1, 1, 1, 1, 1, 1, 1, 1
    # ]

    rules = [
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  # 0
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
        1, 1, 1, 0, 0, 0, 0, 0, 0, 0,  # 50
        0, 0, 0, 0, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 0, 0, 0, 0, 0, 0, 3,
        3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 100
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 1, 1, 1, 1, 1, 1,  # 150
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1
    ]

    return rules[index]


def reward_function(params):
    global g_waypoints
    global g_steer
    global g_total
    global g_start
    global g_param

    steps = params['steps']
    progress = params['progress']

    # track_width = params['track_width']
    # distance_from_center = params['distance_from_center']
    all_wheels_on_track = params['all_wheels_on_track']

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
    if all_wheels_on_track == True and speed > MIN_SPEED:
        reward = 1.0

        # # center bonus (0.25)
        # reward += (BASE_REWARD - (distance / MAX_CENTER))

        # # center bonus (0.25)
        # if distance < (MAX_CENTER * 0.3):
        #     reward *= 2.0

        # direction
        direction = get_rules(closest_waypoint)

        # 0 : any direction
        # 1 : straight
        # 2 : left
        # 3 : right

        # direction bonus (13)
        if (direction == 0) or (direction == 1 and abs_steer < MIN_STEER):
            reward *= 2.0

        elif (direction == 2 and steering >= 0) or (direction == 3 and steering <= 0):
            reward *= 2.0

        else:
            reward *= 0.1

        # speed bonus (6 / 21 / 13)
        if speed > MAX_SPEED and abs_steer < MAX_STEER:
            reward *= 2.0

        elif speed < MAX_SPEED and abs_steer > MIN_STEER:
            reward *= 2.0

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

    waypoints.append([8.51685, 1.65381])
    waypoints.append([8.46102, 1.84977])
    waypoints.append([8.39127, 2.01960])
    waypoints.append([8.30220, 2.20453])
    waypoints.append([8.19190, 2.37790])
    waypoints.append([8.06004, 2.50976])
    waypoints.append([7.89001, 2.61612])
    waypoints.append([7.69220, 2.67968])
    waypoints.append([7.45872, 2.68688])
    waypoints.append([7.22943, 2.62205])
    waypoints.append([7.08140, 2.53250])
    waypoints.append([6.95981, 2.41857])
    waypoints.append([6.86888, 2.29604])
    waypoints.append([6.79362, 2.13857])
    waypoints.append([6.73628, 1.96152])
    waypoints.append([6.71062, 1.75014])
    waypoints.append([6.70768, 1.57855])
    waypoints.append([6.71368, 1.37816])
    waypoints.append([6.71268, 1.18927])
    waypoints.append([6.69323, 0.97714])
    waypoints.append([6.64926, 0.79322])
    waypoints.append([6.57685, 0.61381])
    waypoints.append([6.47996, 0.44661])
    waypoints.append([6.34808, 0.29739])
    waypoints.append([6.18600, 0.17519])
    waypoints.append([6.03157, 0.09495])
    waypoints.append([5.84050, 0.03699])
    waypoints.append([5.62317, 0.01521])
    waypoints.append([5.42850, 0.00039])
    waypoints.append([5.24510, -0.05430])
    waypoints.append([5.03642, -0.10228])
    waypoints.append([4.85453, -0.14785])
    waypoints.append([4.61256, -0.16505])
    waypoints.append([4.44811, -0.18738])
    waypoints.append([4.25193, -0.22479])
    waypoints.append([4.06226, -0.26491])
    waypoints.append([3.86265, -0.29859])
    waypoints.append([3.68098, -0.33573])
    waypoints.append([3.47630, -0.38582])
    waypoints.append([3.28779, -0.42659])
    waypoints.append([3.09522, -0.44894])
    waypoints.append([2.89116, -0.46536])
    waypoints.append([2.69049, -0.48369])
    waypoints.append([2.50392, -0.51696])
    waypoints.append([2.32340, -0.57730])
    waypoints.append([2.13678, -0.66928])
    waypoints.append([1.98814, -0.77299])
    waypoints.append([1.86212, -0.90648])
    waypoints.append([1.76616, -1.06877])
    waypoints.append([1.71448, -1.23444])
    waypoints.append([1.70327, -1.41931])
    waypoints.append([1.72842, -1.59148])
    waypoints.append([1.79483, -1.76396])
    waypoints.append([1.90732, -1.92728])
    waypoints.append([2.03042, -2.04123])
    waypoints.append([2.19551, -2.14840])
    waypoints.append([2.38263, -2.23446])
    waypoints.append([2.54182, -2.27767])
    waypoints.append([2.73724, -2.31226])
    waypoints.append([2.92976, -2.33376])
    waypoints.append([3.13366, -2.36602])
    waypoints.append([3.32862, -2.40486])
    waypoints.append([3.52120, -2.44150])
    waypoints.append([3.71702, -2.47803])
    waypoints.append([3.91604, -2.51307])
    waypoints.append([4.11689, -2.52634])
    waypoints.append([4.30780, -2.52634])
    waypoints.append([4.51630, -2.52634])
    waypoints.append([4.71269, -2.52634])
    waypoints.append([4.89472, -2.52634])
    waypoints.append([5.09584, -2.52634])
    waypoints.append([5.27265, -2.52634])
    waypoints.append([5.47805, -2.52634])
    waypoints.append([5.67761, -2.52634])
    waypoints.append([5.87236, -2.52634])
    waypoints.append([6.07290, -2.52634])
    waypoints.append([6.26141, -2.52634])
    waypoints.append([6.45218, -2.52634])
    waypoints.append([6.65395, -2.52634])
    waypoints.append([6.82439, -2.52634])
    waypoints.append([7.03490, -2.49619])
    waypoints.append([7.22811, -2.46092])
    waypoints.append([7.41695, -2.41489])
    waypoints.append([7.61947, -2.34145])
    waypoints.append([7.77546, -2.25100])
    waypoints.append([7.92330, -2.11961])
    waypoints.append([8.02525, -1.98735])
    waypoints.append([8.12050, -1.80974])
    waypoints.append([8.19437, -1.62215])
    waypoints.append([8.25753, -1.41836])
    waypoints.append([8.32083, -1.21958])
    waypoints.append([8.37074, -1.02482])
    waypoints.append([8.40994, -0.79019])
    waypoints.append([8.42611, -0.62178])
    waypoints.append([8.44250, -0.42346])
    waypoints.append([8.46015, -0.23377])
    waypoints.append([8.49220, -0.02123])
    waypoints.append([8.51875, 0.17349])
    waypoints.append([8.53185, 0.33367])
    waypoints.append([8.56185, 0.53351])
    waypoints.append([8.56185, 0.72296])
    waypoints.append([8.56185, 0.93002])
    waypoints.append([8.56185, 1.12089])
    waypoints.append([8.55185, 1.31937])
    waypoints.append([8.53185, 1.50000])

    return waypoints
