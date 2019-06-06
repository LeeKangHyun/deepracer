import json
import math
import time

NAME = 're02-c'
ACTION = '30 / 7 / 3 / 1'
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

    waypoints.append([4.05040, 3.46011])
    waypoints.append([3.91680, 3.54621])
    waypoints.append([3.77500, 3.65268])
    waypoints.append([3.62537, 3.76549])
    waypoints.append([3.46936, 3.87414])
    waypoints.append([3.30377, 3.97037])
    waypoints.append([3.13596, 4.06680])
    waypoints.append([2.96436, 4.15603])
    waypoints.append([2.79017, 4.23394])
    waypoints.append([2.60535, 4.30952])
    waypoints.append([2.42090, 4.37588])
    waypoints.append([2.23250, 4.42310])
    waypoints.append([2.03887, 4.44734])
    waypoints.append([1.84735, 4.44545])
    waypoints.append([1.65920, 4.41613])
    waypoints.append([1.47665, 4.35791])
    waypoints.append([1.30673, 4.27046])
    waypoints.append([1.15420, 4.15500])
    waypoints.append([1.03144, 4.02343])
    waypoints.append([0.92930, 3.86575])
    waypoints.append([0.85771, 3.69489])
    waypoints.append([0.81702, 3.51776])
    waypoints.append([0.80607, 3.33400])
    waypoints.append([0.82629, 3.14357])
    waypoints.append([0.87155, 2.96368])
    waypoints.append([0.92262, 2.77979])
    waypoints.append([0.97058, 2.58932])
    waypoints.append([1.00736, 2.40285])
    waypoints.append([1.05145, 2.21942])
    waypoints.append([1.11176, 2.03351])
    waypoints.append([1.18355, 1.85331])
    waypoints.append([1.26750, 1.67823])
    waypoints.append([1.36311, 1.50920])
    waypoints.append([1.47409, 1.34860])
    waypoints.append([1.60660, 1.20706])
    waypoints.append([1.75582, 1.09144])
    waypoints.append([1.92335, 1.00218])
    waypoints.append([2.09753, 0.94558])
    waypoints.append([2.27547, 0.91451])
    waypoints.append([2.46721, 0.89861])
    waypoints.append([2.65437, 0.88898])
    waypoints.append([2.84723, 0.87977])
    waypoints.append([3.04496, 0.87720])
    waypoints.append([3.23391, 0.88128])
    waypoints.append([3.43017, 0.88549])
    waypoints.append([3.62490, 0.89055])
    waypoints.append([3.81978, 0.89309])
    waypoints.append([4.00881, 0.88268])
    waypoints.append([4.19814, 0.85321])
    waypoints.append([4.38886, 0.80465])
    waypoints.append([4.57179, 0.74895])
    waypoints.append([4.75122, 0.69544])
    waypoints.append([4.93970, 0.64800])
    waypoints.append([5.13319, 0.61416])
    waypoints.append([5.32176, 0.57911])
    waypoints.append([5.51408, 0.53799])
    waypoints.append([5.70395, 0.51237])
    waypoints.append([5.90451, 0.51206])
    waypoints.append([6.09214, 0.54103])
    waypoints.append([6.27644, 0.60056])
    waypoints.append([6.44085, 0.68469])
    waypoints.append([6.58880, 0.79277])
    waypoints.append([6.71906, 0.92397])
    waypoints.append([6.82822, 1.07579])
    waypoints.append([6.91173, 1.24222])
    waypoints.append([6.96710, 1.41692])
    waypoints.append([6.99480, 1.60014])
    waypoints.append([6.99595, 1.79260])
    waypoints.append([6.96538, 1.97839])
    waypoints.append([6.90121, 2.15825])
    waypoints.append([6.80868, 2.31850])
    waypoints.append([6.69190, 2.45838])
    waypoints.append([6.55330, 2.57631])
    waypoints.append([6.39397, 2.67275])
    waypoints.append([6.21596, 2.74343])
    waypoints.append([6.03452, 2.78281])
    waypoints.append([5.83725, 2.80635])
    waypoints.append([5.64676, 2.82937])
    waypoints.append([5.45966, 2.85430])
    waypoints.append([5.27022, 2.88641])
    waypoints.append([5.07150, 2.93355])
    waypoints.append([4.89000, 2.99874])
    waypoints.append([4.71539, 3.07954])
    waypoints.append([4.54636, 3.16580])
    waypoints.append([4.37609, 3.25796])
    waypoints.append([4.21475, 3.35582])

    return waypoints
