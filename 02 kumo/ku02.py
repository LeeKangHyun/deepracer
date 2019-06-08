import json
import math
import time

NAME = 'ku02-5-3'
ACTION = '30 / 7 / 5.3 / 1'
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
        if steps > 0 and steps <= max_steps:
            reward += ((progress * 2) / steps)

        # # progress bonus
        # if diff_progress > 0:
        #     reward += (diff_progress * 2)

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
    params['time'] = lap_time
    print(json.dumps(params))

    return float(reward)


def get_waypoints():
    waypoints = []

    waypoints.append([3.29848, -0.52544])
    waypoints.append([3.16102, -0.52048])
    waypoints.append([3.04591, -0.54132])
    waypoints.append([2.93000, -0.55306])
    waypoints.append([2.81016, -0.55443])
    waypoints.append([2.68615, -0.54620])
    waypoints.append([2.57181, -0.53446])
    waypoints.append([2.44937, -0.52335])
    waypoints.append([2.33380, -0.52388])
    waypoints.append([2.20583, -0.54259])
    waypoints.append([2.07706, -0.58601])
    waypoints.append([1.97248, -0.63982])
    waypoints.append([1.86922, -0.71496])
    waypoints.append([1.78841, -0.80546])
    waypoints.append([1.72684, -0.90519])
    waypoints.append([1.68923, -1.00689])
    waypoints.append([1.67072, -1.11613])
    waypoints.append([1.67119, -1.23983])
    waypoints.append([1.68501, -1.36675])
    waypoints.append([1.71722, -1.48732])
    waypoints.append([1.75970, -1.59800])
    waypoints.append([1.81479, -1.70596])
    waypoints.append([1.89120, -1.80551])
    waypoints.append([1.97852, -1.88131])
    waypoints.append([2.08005, -1.94719])
    waypoints.append([2.19633, -2.00398])
    waypoints.append([2.32400, -2.04128])
    waypoints.append([2.43473, -2.07099])
    waypoints.append([2.55770, -2.11628])
    waypoints.append([2.67361, -2.16108])
    waypoints.append([2.79521, -2.20607])
    waypoints.append([2.90954, -2.24879])
    waypoints.append([3.01012, -2.28368])
    waypoints.append([3.12599, -2.32044])
    waypoints.append([3.23860, -2.35600])
    waypoints.append([3.35676, -2.38665])
    waypoints.append([3.47172, -2.41009])
    waypoints.append([3.59118, -2.43300])
    waypoints.append([3.71735, -2.45373])
    waypoints.append([3.83204, -2.46550])
    waypoints.append([3.96360, -2.46183])
    waypoints.append([4.09136, -2.44285])
    waypoints.append([4.20994, -2.42217])
    waypoints.append([4.32592, -2.40325])
    waypoints.append([4.44234, -2.38393])
    waypoints.append([4.56881, -2.36620])
    waypoints.append([4.69320, -2.35768])
    waypoints.append([4.81693, -2.35770])
    waypoints.append([4.92458, -2.35943])
    waypoints.append([5.04407, -2.36720])
    waypoints.append([5.16051, -2.38174])
    waypoints.append([5.28696, -2.39938])
    waypoints.append([5.40529, -2.41489])
    waypoints.append([5.52454, -2.41904])
    waypoints.append([5.64840, -2.41113])
    waypoints.append([5.76177, -2.39678])
    waypoints.append([5.89180, -2.37476])
    waypoints.append([6.01821, -2.35773])
    waypoints.append([6.12829, -2.35306])
    waypoints.append([6.25175, -2.35609])
    waypoints.append([6.37988, -2.36466])
    waypoints.append([6.50170, -2.38030])
    waypoints.append([6.63184, -2.40119])
    waypoints.append([6.74691, -2.41783])
    waypoints.append([6.91370, -2.40869])
    waypoints.append([7.04481, -2.38562])
    waypoints.append([7.15920, -2.36364])
    waypoints.append([7.27325, -2.33222])
    waypoints.append([7.38642, -2.28690])
    waypoints.append([7.49285, -2.22580])
    waypoints.append([7.59540, -2.15889])
    waypoints.append([7.68983, -2.09213])
    waypoints.append([7.79948, -2.00313])
    waypoints.append([7.88501, -1.91663])
    waypoints.append([7.96910, -1.83408])
    waypoints.append([8.05978, -1.75172])
    waypoints.append([8.14877, -1.66398])
    waypoints.append([8.23076, -1.57997])
    waypoints.append([8.30691, -1.49286])
    waypoints.append([8.38654, -1.39225])
    waypoints.append([8.45340, -1.28860])
    waypoints.append([8.50760, -1.17849])
    waypoints.append([8.54307, -1.06290])
    waypoints.append([8.56891, -0.92982])
    waypoints.append([8.59093, -0.80889])
    waypoints.append([8.60800, -0.69037])
    waypoints.append([8.61490, -0.57119])
    waypoints.append([8.61927, -0.45400])
    waypoints.append([8.62142, -0.33430])
    waypoints.append([8.61886, -0.20586])
    waypoints.append([8.61170, -0.07384])
    waypoints.append([8.60201, 0.04221])
    waypoints.append([8.58530, 0.16625])
    waypoints.append([8.56190, 0.28912])
    waypoints.append([8.53184, 0.40717])
    waypoints.append([8.49927, 0.52267])
    waypoints.append([8.46324, 0.65376])
    waypoints.append([8.43741, 0.77152])
    waypoints.append([8.42353, 0.89128])
    waypoints.append([8.41961, 1.02350])
    waypoints.append([8.42102, 1.14869])
    waypoints.append([8.41827, 1.27164])
    waypoints.append([8.41660, 1.39101])
    waypoints.append([8.41498, 1.51441])
    waypoints.append([8.41791, 1.66612])
    waypoints.append([8.43108, 1.85768])
    waypoints.append([8.44146, 1.98695])
    waypoints.append([8.43680, 2.09827])
    waypoints.append([8.40991, 2.23152])
    waypoints.append([8.35085, 2.37001])
    waypoints.append([8.27358, 2.48122])
    waypoints.append([8.19190, 2.55833])
    waypoints.append([8.07753, 2.62819])
    waypoints.append([7.95533, 2.67209])
    waypoints.append([7.82091, 2.69728])
    waypoints.append([7.68644, 2.69948])
    waypoints.append([7.57954, 2.68640])
    waypoints.append([7.43551, 2.66108])
    waypoints.append([7.30209, 2.62844])
    waypoints.append([7.16696, 2.58401])
    waypoints.append([7.05277, 2.52759])
    waypoints.append([6.96937, 2.40600])
    waypoints.append([6.92217, 2.27400])
    waypoints.append([6.90248, 2.15846])
    waypoints.append([6.88047, 2.03603])
    waypoints.append([6.86177, 1.91369])
    waypoints.append([6.84556, 1.79371])
    waypoints.append([6.83135, 1.67814])
    waypoints.append([6.82228, 1.56223])
    waypoints.append([6.82054, 1.43388])
    waypoints.append([6.81920, 1.31656])
    waypoints.append([6.81946, 1.18540])
    waypoints.append([6.81198, 1.06563])
    waypoints.append([6.79132, 0.94327])
    waypoints.append([6.75365, 0.83039])
    waypoints.append([6.70213, 0.73095])
    waypoints.append([6.63162, 0.62828])
    waypoints.append([6.55639, 0.53560])
    waypoints.append([6.47282, 0.44567])
    waypoints.append([6.36668, 0.36348])
    waypoints.append([6.25547, 0.30148])
    waypoints.append([6.13550, 0.24986])
    waypoints.append([6.03173, 0.20751])
    waypoints.append([5.92075, 0.16247])
    waypoints.append([5.79822, 0.11417])
    waypoints.append([5.68387, 0.07003])
    waypoints.append([5.56837, 0.03196])
    waypoints.append([5.44844, -0.00293])
    waypoints.append([5.33320, -0.03782])
    waypoints.append([5.21180, -0.06753])
    waypoints.append([5.08937, -0.08723])
    waypoints.append([4.96933, -0.10066])
    waypoints.append([4.84279, -0.11179])
    waypoints.append([4.70730, -0.11913])
    waypoints.append([4.58838, -0.12871])
    waypoints.append([4.46769, -0.14467])
    waypoints.append([4.34902, -0.17666])
    waypoints.append([4.22410, -0.22720])
    waypoints.append([4.11338, -0.27663])
    waypoints.append([3.99768, -0.33526])
    waypoints.append([3.88427, -0.39281])
    waypoints.append([3.77462, -0.44682])
    waypoints.append([3.66215, -0.49201])
    waypoints.append([3.54068, -0.52906])
    waypoints.append([3.42727, -0.53494])

    return waypoints
