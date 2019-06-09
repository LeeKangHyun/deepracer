import json
import math
import time

NAME = 're03-5'
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

    waypoints.append([5.60974, 2.76938])
    waypoints.append([5.52253, 2.78053])
    waypoints.append([5.39071, 2.80230])
    waypoints.append([5.30819, 2.81771])
    waypoints.append([5.21804, 2.84078])
    waypoints.append([5.11397, 2.87109])
    waypoints.append([5.01455, 2.90833])
    waypoints.append([4.91962, 2.95134])
    waypoints.append([4.82464, 2.99941])
    waypoints.append([4.72650, 3.05116])
    waypoints.append([4.62747, 3.10608])
    waypoints.append([4.53315, 3.16004])
    waypoints.append([4.43708, 3.21749])
    waypoints.append([4.34972, 3.27512])
    waypoints.append([4.26180, 3.33754])
    waypoints.append([4.17530, 3.40235])
    waypoints.append([4.08489, 3.46878])
    waypoints.append([3.99518, 3.53345])
    waypoints.append([3.90774, 3.59565])
    waypoints.append([3.81867, 3.65841])
    waypoints.append([3.72189, 3.72081])
    waypoints.append([3.63224, 3.77964])
    waypoints.append([3.53923, 3.83945])
    waypoints.append([3.44729, 3.89790])
    waypoints.append([3.35132, 3.95916])
    waypoints.append([3.26369, 4.01799])
    waypoints.append([3.17407, 4.07969])
    waypoints.append([3.08191, 4.14083])
    waypoints.append([2.98798, 4.20203])
    waypoints.append([2.89438, 4.25623])
    waypoints.append([2.79186, 4.31141])
    waypoints.append([2.69876, 4.36126])
    waypoints.append([2.59641, 4.40900])
    waypoints.append([2.50294, 4.44537])
    waypoints.append([2.40025, 4.48177])
    waypoints.append([2.29632, 4.50958])
    waypoints.append([2.19150, 4.52780])
    waypoints.append([2.08776, 4.53561])
    waypoints.append([1.98272, 4.53286])
    waypoints.append([1.87751, 4.51871])
    waypoints.append([1.78383, 4.49599])
    waypoints.append([1.67747, 4.45735])
    waypoints.append([1.58868, 4.41331])
    waypoints.append([1.50254, 4.35837])
    waypoints.append([1.42071, 4.29213])
    waypoints.append([1.35023, 4.22042])
    waypoints.append([1.28665, 4.14057])
    waypoints.append([1.22575, 4.05442])
    waypoints.append([1.16794, 3.96425])
    waypoints.append([1.11840, 3.87166])
    waypoints.append([1.07298, 3.77300])
    waypoints.append([1.03696, 3.67298])
    waypoints.append([1.00876, 3.56911])
    waypoints.append([0.98705, 3.46776])
    waypoints.append([0.97171, 3.36056])
    waypoints.append([0.95832, 3.25276])
    waypoints.append([0.94507, 3.14507])
    waypoints.append([0.93245, 3.03383])
    waypoints.append([0.92280, 2.92892])
    waypoints.append([0.91546, 2.81899])
    waypoints.append([0.91328, 2.70969])
    waypoints.append([0.91206, 2.60120])
    waypoints.append([0.91657, 2.49030])
    waypoints.append([0.92763, 2.38257])
    waypoints.append([0.94457, 2.27760])
    waypoints.append([0.96568, 2.17103])
    waypoints.append([0.99408, 2.06711])
    waypoints.append([1.02893, 1.97116])
    waypoints.append([1.07285, 1.86996])
    waypoints.append([1.12149, 1.77867])
    waypoints.append([1.17619, 1.68837])
    waypoints.append([1.24018, 1.59355])
    waypoints.append([1.30077, 1.50615])
    waypoints.append([1.37250, 1.41350])
    waypoints.append([1.44130, 1.32522])
    waypoints.append([1.50773, 1.24100])
    waypoints.append([1.57681, 1.16213])
    waypoints.append([1.66123, 1.07984])
    waypoints.append([1.73763, 1.01690])
    waypoints.append([1.82111, 0.95415])
    waypoints.append([1.91037, 0.89273])
    waypoints.append([2.00284, 0.83696])
    waypoints.append([2.08473, 0.78986])
    waypoints.append([2.18922, 0.73820])
    waypoints.append([2.29205, 0.69781])
    waypoints.append([2.39109, 0.66681])
    waypoints.append([2.49374, 0.63929])
    waypoints.append([2.59927, 0.61723])
    waypoints.append([2.71634, 0.59569])
    waypoints.append([2.81734, 0.58463])
    waypoints.append([2.92307, 0.58032])
    waypoints.append([3.02865, 0.57800])
    waypoints.append([3.14022, 0.57641])
    waypoints.append([3.24197, 0.57641])
    waypoints.append([3.35573, 0.57641])
    waypoints.append([3.46304, 0.57641])
    waypoints.append([3.57530, 0.57641])
    waypoints.append([3.68463, 0.57641])
    waypoints.append([3.79238, 0.57641])
    waypoints.append([3.89746, 0.57641])
    waypoints.append([4.00890, 0.57641])
    waypoints.append([4.11321, 0.57641])
    waypoints.append([4.22035, 0.57641])
    waypoints.append([4.33201, 0.57641])
    waypoints.append([4.43774, 0.57641])
    waypoints.append([4.54842, 0.57641])
    waypoints.append([4.65328, 0.57641])
    waypoints.append([4.76025, 0.57641])
    waypoints.append([4.87003, 0.57641])
    waypoints.append([4.97708, 0.57641])
    waypoints.append([5.08520, 0.57641])
    waypoints.append([5.19848, 0.57641])
    waypoints.append([5.30278, 0.57641])
    waypoints.append([5.40901, 0.57641])
    waypoints.append([5.51939, 0.57641])
    waypoints.append([5.62710, 0.57641])
    waypoints.append([5.73860, 0.56684])
    waypoints.append([5.84820, 0.57902])
    waypoints.append([5.95438, 0.59667])
    waypoints.append([6.06670, 0.62173])
    waypoints.append([6.16413, 0.64439])
    waypoints.append([6.26660, 0.67257])
    waypoints.append([6.37120, 0.70992])
    waypoints.append([6.46828, 0.75404])
    waypoints.append([6.56308, 0.80790])
    waypoints.append([6.65050, 0.86945])
    waypoints.append([6.72325, 0.93156])
    waypoints.append([6.79710, 1.00810])
    waypoints.append([6.86082, 1.08905])
    waypoints.append([6.91696, 1.17714])
    waypoints.append([6.96320, 1.26909])
    waypoints.append([7.00070, 1.36828])
    waypoints.append([7.02702, 1.46944])
    waypoints.append([7.04228, 1.57130])
    waypoints.append([7.04673, 1.67736])
    waypoints.append([7.04029, 1.77860])
    waypoints.append([7.02358, 1.87856])
    waypoints.append([6.99463, 1.98352])
    waypoints.append([6.95588, 2.08201])
    waypoints.append([6.91098, 2.16922])
    waypoints.append([6.85610, 2.25426])
    waypoints.append([6.78774, 2.33934])
    waypoints.append([6.71276, 2.41444])
    waypoints.append([6.63917, 2.47454])
    waypoints.append([6.54690, 2.53522])
    waypoints.append([6.45868, 2.58235])
    waypoints.append([6.35789, 2.62892])
    waypoints.append([6.25949, 2.66389])
    waypoints.append([6.16167, 2.69020])
    waypoints.append([6.05213, 2.71517])
    waypoints.append([5.95114, 2.72931])
    waypoints.append([5.84659, 2.73562])
    waypoints.append([5.73849, 2.73923])

    return waypoints
