import json
import math
import time

NAME = 'mk32-a'
TRACK = 'reinvent'
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
        g_waypoints = get_waypoints(TRACK)

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


def get_waypoints(track):
    waypoints = []

    if track == 'reinvent' or track == 're':
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

    elif track == 'london':
        waypoints.append([2.78516, 0.88389])
        waypoints.append([3.00210, 0.92191])
        waypoints.append([3.24228, 0.93979])
        waypoints.append([3.43895, 0.94095])
        waypoints.append([3.64282, 0.94445])
        waypoints.append([3.83728, 0.93332])
        waypoints.append([4.03120, 0.92461])
        waypoints.append([4.22864, 0.88846])
        waypoints.append([4.42092, 0.85040])
        waypoints.append([4.63225, 0.80347])
        waypoints.append([4.83639, 0.76128])
        waypoints.append([5.02109, 0.72908])
        waypoints.append([5.24634, 0.70376])
        waypoints.append([5.44646, 0.70209])
        waypoints.append([5.62823, 0.70819])
        waypoints.append([5.83734, 0.71630])
        waypoints.append([6.03133, 0.78517])
        waypoints.append([6.19027, 0.87204])
        waypoints.append([6.39219, 1.02337])
        waypoints.append([6.56588, 1.18874])
        waypoints.append([6.71011, 1.34754])
        waypoints.append([6.83824, 1.52072])
        waypoints.append([6.94134, 1.69367])
        waypoints.append([7.02293, 1.86446])
        waypoints.append([7.08530, 2.03980])
        waypoints.append([7.13529, 2.25710])
        waypoints.append([7.16171, 2.46162])
        waypoints.append([7.15546, 2.66745])
        waypoints.append([7.09099, 2.90010])
        waypoints.append([6.99730, 3.13196])
        waypoints.append([6.86965, 3.31578])
        waypoints.append([6.73540, 3.49761])
        waypoints.append([6.58204, 3.62602])
        waypoints.append([6.41950, 3.73876])
        waypoints.append([6.24180, 3.84979])
        waypoints.append([6.00841, 3.97356])
        waypoints.append([5.78578, 4.07673])
        waypoints.append([5.58962, 4.15950])
        waypoints.append([5.38585, 4.22341])
        waypoints.append([5.20490, 4.27989])
        waypoints.append([5.00956, 4.34099])
        waypoints.append([4.83229, 4.38635])
        waypoints.append([4.63737, 4.42875])
        waypoints.append([4.42915, 4.47570])
        waypoints.append([4.24614, 4.50815])
        waypoints.append([4.02831, 4.53060])
        waypoints.append([3.83690, 4.53579])
        waypoints.append([3.62654, 4.53819])
        waypoints.append([3.44725, 4.53950])
        waypoints.append([3.23626, 4.53550])
        waypoints.append([3.03778, 4.52209])
        waypoints.append([2.84770, 4.50638])
        waypoints.append([2.64940, 4.48949])
        waypoints.append([2.44031, 4.46102])
        waypoints.append([2.23700, 4.42053])
        waypoints.append([2.04307, 4.36778])
        waypoints.append([1.86264, 4.30674])
        waypoints.append([1.67327, 4.22687])
        waypoints.append([1.50094, 4.14162])
        waypoints.append([1.32608, 4.07294])
        waypoints.append([1.14272, 3.97461])
        waypoints.append([0.97463, 3.85109])
        waypoints.append([0.82884, 3.70877])
        waypoints.append([0.70241, 3.52906])
        waypoints.append([0.61001, 3.34826])
        waypoints.append([0.53975, 3.16684])
        waypoints.append([0.49325, 2.98457])
        waypoints.append([0.46288, 2.77479])
        waypoints.append([0.44751, 2.56595])
        waypoints.append([0.45194, 2.37323])
        waypoints.append([0.47490, 2.17106])
        waypoints.append([0.51405, 1.96758])
        waypoints.append([0.57494, 1.77093])
        waypoints.append([0.65068, 1.59584])
        waypoints.append([0.75332, 1.41837])
        waypoints.append([0.88079, 1.26289])
        waypoints.append([1.02783, 1.12557])
        waypoints.append([1.18436, 1.00860])
        waypoints.append([1.35744, 0.91070])
        waypoints.append([1.54779, 0.83196])
        waypoints.append([1.75400, 0.77941])
        waypoints.append([1.94836, 0.75995])
        waypoints.append([2.15829, 0.76682])
        waypoints.append([2.35673, 0.80025])
        waypoints.append([2.55503, 0.84813])

    return waypoints
