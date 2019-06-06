import json
import math
import time

NAME = 'ku02-a'
ACTION = '30 / 7 / 5 / 1'
HYPER = '256 / 0.999 / 40'

SIGHT = 3

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

        # # speed bonus
        # if speed > 0:
        #     reward += (speed / MAX_SPEED)

        # # steer panelity
        # if abs_steer > MAX_STEER:
        #     reward *= 0.5

        # progress bonus
        if steps > 0 and progress > 0:
            reward += (progress / steps * 2)

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

    waypoints.append([3.01908, -2.32783])
    waypoints.append([3.12616, -2.33027])
    waypoints.append([3.25953, -2.33563])
    waypoints.append([3.37981, -2.34069])
    waypoints.append([3.50152, -2.34465])
    waypoints.append([3.62205, -2.32818])
    waypoints.append([3.73629, -2.31406])
    waypoints.append([3.85078, -2.30657])
    waypoints.append([3.97567, -2.30448])
    waypoints.append([4.09774, -2.30422])
    waypoints.append([4.21368, -2.30522])
    waypoints.append([4.34770, -2.30757])
    waypoints.append([4.46656, -2.31205])
    waypoints.append([4.58696, -2.31930])
    waypoints.append([4.71759, -2.32678])
    waypoints.append([4.84030, -2.33310])
    waypoints.append([4.96052, -2.33570])
    waypoints.append([5.08484, -2.33822])
    waypoints.append([5.19236, -2.34074])
    waypoints.append([5.31699, -2.34275])
    waypoints.append([5.44332, -2.34389])
    waypoints.append([5.57017, -2.34839])
    waypoints.append([5.68910, -2.35633])
    waypoints.append([5.79994, -2.36530])
    waypoints.append([5.92655, -2.37684])
    waypoints.append([6.04626, -2.38602])
    waypoints.append([6.16700, -2.39108])
    waypoints.append([6.30180, -2.39024])
    waypoints.append([6.43846, -2.38393])
    waypoints.append([6.56582, -2.37730])
    waypoints.append([6.69322, -2.36899])
    waypoints.append([6.80998, -2.36321])
    waypoints.append([6.94101, -2.35836])
    waypoints.append([7.07115, -2.35298])
    waypoints.append([7.19158, -2.35200])
    waypoints.append([7.31878, -2.35100])
    waypoints.append([7.44822, -2.35063])
    waypoints.append([7.57400, -2.34662])
    waypoints.append([7.70329, -2.32486])
    waypoints.append([7.82180, -2.28248])
    waypoints.append([7.92863, -2.21836])
    waypoints.append([8.01924, -2.13313])
    waypoints.append([8.08904, -2.02984])
    waypoints.append([8.13602, -1.92619])
    waypoints.append([8.17508, -1.81980])
    waypoints.append([8.20885, -1.70252])
    waypoints.append([8.24272, -1.56414])
    waypoints.append([8.27207, -1.44556])
    waypoints.append([8.30880, -1.32931])
    waypoints.append([8.35599, -1.20431])
    waypoints.append([8.39775, -1.09327])
    waypoints.append([8.43470, -0.97220])
    waypoints.append([8.46144, -0.84345])
    waypoints.append([8.47838, -0.72621])
    waypoints.append([8.48382, -0.61142])
    waypoints.append([8.48224, -0.47182])
    waypoints.append([8.47540, -0.34175])
    waypoints.append([8.46826, -0.20652])
    waypoints.append([8.46170, -0.08593])
    waypoints.append([8.46048, 0.04187])
    waypoints.append([8.47136, 0.16843])
    waypoints.append([8.49410, 0.30440])
    waypoints.append([8.51820, 0.42387])
    waypoints.append([8.54264, 0.54262])
    waypoints.append([8.56364, 0.65320])
    waypoints.append([8.58035, 0.77676])
    waypoints.append([8.58192, 0.91120])
    waypoints.append([8.57231, 1.02756])
    waypoints.append([8.55580, 1.14567])
    waypoints.append([8.53208, 1.27020])
    waypoints.append([8.50302, 1.39500])
    waypoints.append([8.47630, 1.52052])
    waypoints.append([8.44260, 1.65083])
    waypoints.append([8.41365, 1.75917])
    waypoints.append([8.38329, 1.88408])
    waypoints.append([8.36219, 2.00340])
    waypoints.append([8.34014, 2.13658])
    waypoints.append([8.31420, 2.27720])
    waypoints.append([8.27715, 2.39565])
    waypoints.append([8.22180, 2.50650])
    waypoints.append([8.14713, 2.60641])
    waypoints.append([8.04314, 2.70313])
    waypoints.append([7.94227, 2.77275])
    waypoints.append([7.82946, 2.83343])
    waypoints.append([7.70909, 2.87275])
    waypoints.append([7.57560, 2.89015])
    waypoints.append([7.45200, 2.88367])
    waypoints.append([7.33343, 2.86310])
    waypoints.append([7.21657, 2.83672])
    waypoints.append([7.10379, 2.79644])
    waypoints.append([6.99637, 2.73510])
    waypoints.append([6.90691, 2.65823])
    waypoints.append([6.83381, 2.56628])
    waypoints.append([6.77620, 2.45681])
    waypoints.append([6.73500, 2.32086])
    waypoints.append([6.72255, 2.20228])
    waypoints.append([6.73169, 2.07573])
    waypoints.append([6.76144, 1.94645])
    waypoints.append([6.79909, 1.82961])
    waypoints.append([6.84345, 1.70905])
    waypoints.append([6.88538, 1.58488])
    waypoints.append([6.91855, 1.45986])
    waypoints.append([6.93750, 1.34326])
    waypoints.append([6.94330, 1.21223])
    waypoints.append([6.92244, 1.08256])
    waypoints.append([6.87370, 0.95183])
    waypoints.append([6.80945, 0.84095])
    waypoints.append([6.72871, 0.74139])
    waypoints.append([6.65578, 0.65174])
    waypoints.append([6.57583, 0.57238])
    waypoints.append([6.47770, 0.49510])
    waypoints.append([6.37494, 0.41953])
    waypoints.append([6.26850, 0.34827])
    waypoints.append([6.16403, 0.28498])
    waypoints.append([6.05874, 0.22018])
    waypoints.append([5.95715, 0.16030])
    waypoints.append([5.84556, 0.10086])
    waypoints.append([5.72518, 0.05217])
    waypoints.append([5.61490, 0.01264])
    waypoints.append([5.49289, -0.02739])
    waypoints.append([5.37838, -0.06339])
    waypoints.append([5.26930, -0.09585])
    waypoints.append([5.14721, -0.12766])
    waypoints.append([5.02778, -0.15168])
    waypoints.append([4.90087, -0.17384])
    waypoints.append([4.78687, -0.19294])
    waypoints.append([4.66876, -0.21129])
    waypoints.append([4.54460, -0.22976])
    waypoints.append([4.41906, -0.24568])
    waypoints.append([4.30060, -0.25547])
    waypoints.append([4.18441, -0.25720])
    waypoints.append([4.05680, -0.25097])
    waypoints.append([3.93120, -0.24364])
    waypoints.append([3.80422, -0.24381])
    waypoints.append([3.68916, -0.24884])
    waypoints.append([3.56973, -0.26681])
    waypoints.append([3.45187, -0.29881])
    waypoints.append([3.33937, -0.33458])
    waypoints.append([3.22180, -0.37029])
    waypoints.append([3.10598, -0.40483])
    waypoints.append([2.98721, -0.42620])
    waypoints.append([2.86888, -0.43561])
    waypoints.append([2.74637, -0.44099])
    waypoints.append([2.62414, -0.44067])
    waypoints.append([2.51136, -0.43559])
    waypoints.append([2.38222, -0.43204])
    waypoints.append([2.26489, -0.44012])
    waypoints.append([2.14764, -0.46717])
    waypoints.append([2.03789, -0.51242])
    waypoints.append([1.93512, -0.57513])
    waypoints.append([1.84930, -0.64809])
    waypoints.append([1.78071, -0.72930])
    waypoints.append([1.72130, -0.83449])
    waypoints.append([1.68170, -0.96219])
    waypoints.append([1.67212, -1.08247])
    waypoints.append([1.68064, -1.21090])
    waypoints.append([1.69961, -1.33361])
    waypoints.append([1.73330, -1.44825])
    waypoints.append([1.78289, -1.56943])
    waypoints.append([1.84367, -1.69126])
    waypoints.append([1.90551, -1.80012])
    waypoints.append([1.96638, -1.91057])
    waypoints.append([2.03835, -2.01154])
    waypoints.append([2.11790, -2.09698])
    waypoints.append([2.21170, -2.17265])
    waypoints.append([2.31743, -2.23252])
    waypoints.append([2.43191, -2.27698])
    waypoints.append([2.55010, -2.30346])
    waypoints.append([2.66649, -2.31872])
    waypoints.append([2.77991, -2.31730])
    waypoints.append([2.90586, -2.30754])

    return waypoints
