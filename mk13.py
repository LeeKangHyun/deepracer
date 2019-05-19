import json
import math
import time

NAME = 'mk13'
PARAM = '18 / 5 / 5 / 1 / 0.3'

SIGHT = 0.3

BASE_REWARD = 1.2

MAX_ANGLE = 5

MAX_STEER = 15
LEN_STEER = 2

MAX_STEPS = 200

g_episode = 0
g_progress = float(0)
g_completed = False
g_waypoints = []
g_total = float(0)
g_steer = []
g_start = 0


def get_episode(progress):
    global g_episode
    global g_progress
    global g_completed
    global g_waypoints
    global g_total
    global g_steer
    global g_start

    # reset
    if g_progress > progress:
        g_episode += 1
        g_total = float(0)
        g_start = time.time()
        del g_steer[:]

    # completed
    if g_progress < progress and progress == 100:
        g_completed = True
        seconds = time.time() - g_start
        print('--- episode completed -- {} -- {} seconds ---'.format(g_episode, seconds))
    else:
        g_completed = False

    # waypoints
    if len(g_waypoints) < 1:
        g_waypoints = get_waypoints()

    # prev progress
    g_progress = progress

    return g_episode


def get_closest_waypoint(waypoints, x, y):
    res = 0
    index = 0
    # waypoints = get_waypoints()
    min_distance = float('inf')
    for row in waypoints:
        distance = math.sqrt(
            (row[0] - x) * (row[0] - x) + (row[1] - y) * (row[1] - y))
        if distance < min_distance:
            min_distance = distance
            res = index
        index = index + 1
    return res


def get_distance(coor1, coor2):
    return math.sqrt((coor1[0] - coor2[0]) * (coor1[0] - coor2[0]) + (coor1[1] - coor2[1]) * (coor1[1] - coor2[1]))


def get_next_point(waypoints, this_point, closest, distance):
    next_index = closest
    next_point = []

    while True:
        next_point = waypoints[next_index]

        dist = get_distance(this_point, next_point)
        if dist >= distance:
            break

        next_index += 1
        if next_index >= len(waypoints):
            next_index = next_index - len(waypoints)

    return next_point


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
    global g_total
    global g_waypoints

    progress = params['progress']

    track_width = params['track_width']
    distance_from_center = params['distance_from_center']

    heading = params['heading']
    steering = params['steering_angle']

    x = params['x']
    y = params['y']

    # waypoints = params['waypoints']
    # closest_waypoints = params['closest_waypoints']
    # prev_waypoint = waypoints[closest_waypoints[0]]
    # next_waypoint = waypoints[closest_waypoints[1]]

    # default
    reward = 0.001

    # episode
    episode = get_episode(progress)

    # closest waypoint
    closest = get_closest_waypoint(g_waypoints, x, y)

    # point
    this_point = [x, y]
    next_point = get_next_point(g_waypoints, this_point, closest, SIGHT)

    # diff angle
    diff_angle = get_diff_angle(
        this_point, next_point, heading, steering)

    # diff steering
    diff_steer = get_diff_steering(steering)

    if diff_angle <= MAX_ANGLE and diff_steer <= MAX_STEER:
        # angle
        reward += (BASE_REWARD - (diff_angle / MAX_ANGLE))

        # steering
        reward += (BASE_REWARD - (diff_steer / MAX_STEER))

        # center bonus
        reward += (BASE_REWARD - (distance_from_center / (track_width / 2)))

    g_total += reward

    # log
    params['name'] = NAME
    params['params'] = PARAM
    params['episode'] = episode
    params['diff_angle'] = diff_angle
    params['diff_steer'] = diff_steer
    params['next_point'] = next_point
    params['reward'] = reward
    params['total'] = g_total
    print(json.dumps(params))

    return float(reward)


def get_waypoints():
    waypoints = []
    waypoints.append([7.24706, 3.12118])
    waypoints.append([7.18818, 3.23341])
    waypoints.append([7.10170, 3.35788])
    waypoints.append([6.96962, 3.46712])
    waypoints.append([6.81593, 3.57738])
    waypoints.append([6.66350, 3.67806])
    waypoints.append([6.51049, 3.77501])
    waypoints.append([6.36623, 3.86119])
    waypoints.append([6.22761, 3.94405])
    waypoints.append([6.05810, 4.04369])
    waypoints.append([5.90238, 4.13480])
    waypoints.append([5.74767, 4.22466])
    waypoints.append([5.57561, 4.31795])
    waypoints.append([5.41789, 4.39745])
    waypoints.append([5.23490, 4.48100])
    waypoints.append([5.07447, 4.54150])
    waypoints.append([4.89836, 4.59630])
    waypoints.append([4.73269, 4.63459])
    waypoints.append([4.54146, 4.64928])
    waypoints.append([4.37658, 4.63909])
    waypoints.append([4.18995, 4.61182])
    waypoints.append([4.01000, 4.61029])
    waypoints.append([3.82994, 4.61012])
    waypoints.append([3.65152, 4.59738])
    waypoints.append([3.47325, 4.57952])
    waypoints.append([3.28266, 4.58501])
    waypoints.append([3.10639, 4.58420])
    waypoints.append([2.91446, 4.58556])
    waypoints.append([2.73708, 4.59095])
    waypoints.append([2.54834, 4.59868])
    waypoints.append([2.36536, 4.57458])
    waypoints.append([2.17090, 4.58237])
    waypoints.append([1.99295, 4.57734])
    waypoints.append([1.79127, 4.54802])
    waypoints.append([1.61283, 4.50263])
    waypoints.append([1.41710, 4.42597])
    waypoints.append([1.26217, 4.33789])
    waypoints.append([1.09692, 4.22924])
    waypoints.append([0.95832, 4.12699])
    waypoints.append([0.81545, 4.00220])
    waypoints.append([0.69380, 3.87159])
    waypoints.append([0.59244, 3.72410])
    waypoints.append([0.51675, 3.56689])
    waypoints.append([0.46855, 3.39776])
    waypoints.append([0.44865, 3.23039])
    waypoints.append([0.45210, 3.03945])
    waypoints.append([0.46930, 2.85944])
    waypoints.append([0.48586, 2.66878])
    waypoints.append([0.49086, 2.49611])
    waypoints.append([0.50845, 2.33133])
    waypoints.append([0.53002, 2.12412])
    waypoints.append([0.55672, 1.94009])
    waypoints.append([0.58853, 1.76734])
    waypoints.append([0.61091, 1.58665])
    waypoints.append([0.65280, 1.41207])
    waypoints.append([0.72418, 1.23132])
    waypoints.append([0.81303, 1.07549])
    waypoints.append([0.91875, 0.92615])
    waypoints.append([1.03158, 0.79686])
    waypoints.append([1.17130, 0.67489])
    waypoints.append([1.33063, 0.57772])
    waypoints.append([1.50282, 0.51261])
    waypoints.append([1.67236, 0.48235])
    waypoints.append([1.88603, 0.48883])
    waypoints.append([2.06508, 0.52995])
    waypoints.append([2.24538, 0.59704])
    waypoints.append([2.41329, 0.67158])
    waypoints.append([2.58141, 0.75289])
    waypoints.append([2.73189, 0.82888])
    waypoints.append([2.88508, 0.90308])
    waypoints.append([3.05031, 0.97506])
    waypoints.append([3.23862, 1.04469])
    waypoints.append([3.42279, 1.09849])
    waypoints.append([3.60573, 1.13717])
    waypoints.append([3.76836, 1.15574])
    waypoints.append([3.96776, 1.14695])
    waypoints.append([4.15547, 1.11002])
    waypoints.append([4.32405, 1.05619])
    waypoints.append([4.48032, 0.98812])
    waypoints.append([4.64982, 0.89865])
    waypoints.append([4.81990, 0.80160])
    waypoints.append([4.97442, 0.71069])
    waypoints.append([5.12390, 0.62699])
    waypoints.append([5.29239, 0.54832])
    waypoints.append([5.45917, 0.49469])
    waypoints.append([5.63090, 0.46548])
    waypoints.append([5.81092, 0.45965])
    waypoints.append([5.99641, 0.48635])
    waypoints.append([6.16473, 0.54799])
    waypoints.append([6.32694, 0.64488])
    waypoints.append([6.47338, 0.76179])
    waypoints.append([6.59949, 0.89445])
    waypoints.append([6.72207, 1.02691])
    waypoints.append([6.83570, 1.15668])
    waypoints.append([6.94741, 1.29613])
    waypoints.append([7.05349, 1.45469])
    waypoints.append([7.14519, 1.59510])
    waypoints.append([7.25180, 1.76676])
    waypoints.append([7.33164, 1.93337])
    waypoints.append([7.38525, 2.09243])
    waypoints.append([7.41646, 2.27033])
    waypoints.append([7.41948, 2.43760])
    waypoints.append([7.39488, 2.60284])
    waypoints.append([7.35110, 2.78244])
    waypoints.append([7.31704, 2.93444])
    return waypoints
