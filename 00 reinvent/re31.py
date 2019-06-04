import json
import math
import time

NAME = 're31-f'
ACTION = '24 / 7 / 5 / 1'
HYPER = '128 / 0.999 / 40'

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

    # mk11
    waypoints.append([1.97500, 4.27896])
    waypoints.append([1.79196, 4.25956])
    waypoints.append([1.61161, 4.24012])
    waypoints.append([1.43498, 4.16430])
    waypoints.append([1.26477, 4.07530])
    waypoints.append([1.10850, 3.96560])
    waypoints.append([0.96614, 3.83165])
    waypoints.append([0.85026, 3.68416])
    waypoints.append([0.76020, 3.52505])
    waypoints.append([0.69550, 3.35139])
    waypoints.append([0.66074, 3.17008])
    waypoints.append([0.65276, 2.97429])
    waypoints.append([0.67368, 2.78445])
    waypoints.append([0.71788, 2.60179])
    waypoints.append([0.77247, 2.41587])
    waypoints.append([0.83500, 2.23600])
    waypoints.append([0.90661, 2.05838])
    waypoints.append([0.99304, 1.88435])
    waypoints.append([1.08552, 1.72005])
    waypoints.append([1.18540, 1.55611])
    waypoints.append([1.30083, 1.40013])
    waypoints.append([1.43371, 1.26287])
    waypoints.append([1.58256, 1.14650])
    waypoints.append([1.76119, 1.04567])
    waypoints.append([1.94688, 0.97342])
    waypoints.append([2.13245, 0.91109])
    waypoints.append([2.31756, 0.85339])
    waypoints.append([2.50641, 0.79858])
    waypoints.append([2.69250, 0.74643])
    waypoints.append([2.88327, 0.69396])
    waypoints.append([3.06550, 0.64981])
    waypoints.append([3.25216, 0.61233])
    waypoints.append([3.44136, 0.58139])
    waypoints.append([3.63288, 0.57106])
    waypoints.append([3.82728, 0.57888])
    waypoints.append([4.01471, 0.59193])
    waypoints.append([4.21044, 0.60042])
    waypoints.append([4.40570, 0.61894])
    waypoints.append([4.59599, 0.62658])
    waypoints.append([4.79019, 0.63504])
    waypoints.append([4.98027, 0.64228])
    waypoints.append([5.17036, 0.66761])
    waypoints.append([5.36040, 0.69138])
    waypoints.append([5.56267, 0.69848])
    waypoints.append([5.75080, 0.71288])
    waypoints.append([5.94780, 0.73880])
    waypoints.append([6.13484, 0.79131])
    waypoints.append([6.38950, 0.88263])
    waypoints.append([6.57956, 1.00143])
    waypoints.append([6.73160, 1.14001])
    waypoints.append([6.82449, 1.29136])
    waypoints.append([6.89050, 1.45509])
    waypoints.append([6.96050, 1.63586])
    waypoints.append([6.96940, 1.81988])
    waypoints.append([6.96940, 2.01092])
    waypoints.append([6.92940, 2.22405])
    waypoints.append([6.85704, 2.37795])
    waypoints.append([6.71508, 2.53316])
    waypoints.append([6.54343, 2.60913])
    waypoints.append([6.36056, 2.66915])
    waypoints.append([6.17232, 2.70209])
    waypoints.append([5.97423, 2.74905])
    waypoints.append([5.78277, 2.79622])
    waypoints.append([5.58993, 2.83565])
    waypoints.append([5.39603, 2.87128])
    waypoints.append([5.20890, 2.90078])
    waypoints.append([5.03020, 2.94299])
    waypoints.append([4.85411, 2.99457])
    waypoints.append([4.68989, 3.03562])
    waypoints.append([4.52982, 3.09673])
    waypoints.append([4.36345, 3.19547])
    waypoints.append([4.18732, 3.26890])
    waypoints.append([4.02660, 3.36166])
    waypoints.append([3.86905, 3.47019])
    waypoints.append([3.71589, 3.59122])
    waypoints.append([3.56276, 3.70954])
    waypoints.append([3.40770, 3.81997])
    waypoints.append([3.24910, 3.92490])
    waypoints.append([3.08332, 4.01892])
    waypoints.append([2.91224, 4.10444])
    waypoints.append([2.73308, 4.16461])
    waypoints.append([2.54475, 4.20234])
    waypoints.append([2.34918, 4.23512])
    waypoints.append([2.15661, 4.26222])

    return waypoints
