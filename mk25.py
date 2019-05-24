import json
import math
import time

NAME = 'mk25'
ACTION = '18 / 7 / 5 / 1'

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

    # reset
    if g_progress > progress:
        print('- episode reset - {} - {} - {} - {} - {}'.format(NAME, g_episode,
                                                                g_time, g_steps, g_total))
        g_episode += 1
        g_total = float(0)
        g_start = time.time()
        del g_steer[:]

    g_time = time.time() - g_start

    # completed
    if g_progress < progress and progress == 100:
        print('- episode completed - {} - {} - {} - {} - {}'.format(NAME, g_episode,
                                                                    g_time, steps, g_total))

    # waypoints
    if len(g_waypoints) < 1:
        g_waypoints = get_waypoints()

    # prev
    g_progress = progress
    g_steps = steps

    return g_episode


def get_closest_waypoint(location):
    global g_waypoints

    dist_list = []
    for waypoint in g_waypoints:
        dist_list.append(get_distance(waypoint, location))

    index = 0
    closest = 0
    min_dist = float('inf')

    for dist in dist_list:
        if dist < min_dist:
            min_dist = dist
            closest = index
        index += 1

    prev_index = closest - 1
    if prev_index < 0:
        prev_index = len(g_waypoints) - 1

    dist1 = dist_list[prev_index]
    dist2 = get_distance(g_waypoints[prev_index], g_waypoints[closest])

    if dist1 > dist2:
        closest = closest + 1
        if closest >= len(g_waypoints):
            closest = closest - len(g_waypoints)

    return closest, dist_list[closest]


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
    reward = 0.001

    # episode
    episode = get_episode(progress, steps)

    # closest waypoint
    closest, distance = get_closest_waypoint(location)

    # center bonus
    if distance < MAX_CENTER:
        reward += (BASE_REWARD - (distance / MAX_CENTER))

    # point
    destination = get_destination(closest, SIGHT)

    # diff angle
    diff_angle = get_diff_angle(g_waypoints[closest], destination, heading, steering)

    if diff_angle <= MAX_ANGLE:
        reward += (BASE_REWARD - (diff_angle / MAX_ANGLE))

    # diff steering
    diff_steer = get_diff_steering(steering)

    if diff_steer <= MAX_STEER:
        reward += (BASE_REWARD - (diff_steer / MAX_STEER))

    # total reward
    g_total += reward

    # log
    params['name'] = NAME
    params['params'] = ACTION
    params['episode'] = episode
    params['distance'] = distance
    params['destination'] = destination
    params['diff_angle'] = diff_angle
    params['diff_steer'] = diff_steer
    params['reward'] = reward
    params['total'] = g_total
    params['time'] = g_time
    print(json.dumps(params))

    return float(reward)


def get_waypoints():
    # mk20-3097 : 11.92635
    waypoints = []
    waypoints.append([2.65302, 0.86523])
    waypoints.append([2.85704, 0.88381])
    waypoints.append([3.04267, 0.90109])
    waypoints.append([3.22823, 0.90951])
    waypoints.append([3.44010, 0.90914])
    waypoints.append([3.64244, 0.88496])
    waypoints.append([3.82836, 0.86350])
    waypoints.append([4.03112, 0.84479])
    waypoints.append([4.24454, 0.82507])
    waypoints.append([4.43640, 0.80571])
    waypoints.append([4.64771, 0.78351])
    waypoints.append([4.84458, 0.75499])
    waypoints.append([5.02585, 0.71956])
    waypoints.append([5.23589, 0.68451])
    waypoints.append([5.42970, 0.66851])
    waypoints.append([5.64390, 0.67781])
    waypoints.append([5.83260, 0.71351])
    waypoints.append([6.03133, 0.78517])
    waypoints.append([6.19027, 0.87204])
    waypoints.append([6.39219, 1.02337])
    waypoints.append([6.56588, 1.18874])
    waypoints.append([6.71011, 1.34754])
    waypoints.append([6.83824, 1.52072])
    waypoints.append([6.94134, 1.69367])
    waypoints.append([7.02293, 1.86446])
    waypoints.append([7.07930, 2.03980])
    waypoints.append([7.12029, 2.26710])
    waypoints.append([7.14171, 2.46162])
    waypoints.append([7.13546, 2.66745])
    waypoints.append([7.09099, 2.90010])
    waypoints.append([6.98730, 3.13196])
    waypoints.append([6.86965, 3.31578])
    waypoints.append([6.73540, 3.49761])
    waypoints.append([6.58204, 3.62602])
    waypoints.append([6.41950, 3.73876])
    waypoints.append([6.26180, 3.84979])
    waypoints.append([6.08424, 3.96388])
    waypoints.append([5.90272, 4.04633])
    waypoints.append([5.73536, 4.11491])
    waypoints.append([5.56518, 4.19570])
    waypoints.append([5.37289, 4.25654])
    waypoints.append([5.17537, 4.32076])
    waypoints.append([4.99219, 4.37453])
    waypoints.append([4.78635, 4.41665])
    waypoints.append([4.59071, 4.45763])
    waypoints.append([4.40201, 4.46724])
    waypoints.append([4.21323, 4.48554])
    waypoints.append([4.01391, 4.48727])
    waypoints.append([3.79248, 4.47685])
    waypoints.append([3.59518, 4.46578])
    waypoints.append([3.39718, 4.45549])
    waypoints.append([3.20560, 4.45019])
    waypoints.append([2.99041, 4.44586])
    waypoints.append([2.77678, 4.43912])
    waypoints.append([2.57805, 4.42200])
    waypoints.append([2.40000, 4.40207])
    waypoints.append([2.19940, 4.37100])
    waypoints.append([1.99272, 4.33451])
    waypoints.append([1.80467, 4.29110])
    waypoints.append([1.61292, 4.24006])
    waypoints.append([1.42354, 4.18023])
    waypoints.append([1.24024, 4.10657])
    waypoints.append([1.05230, 4.00534])
    waypoints.append([0.89043, 3.88285])
    waypoints.append([0.75640, 3.74500])
    waypoints.append([0.64238, 3.59145])
    waypoints.append([0.53389, 3.40189])
    waypoints.append([0.45542, 3.21429])
    waypoints.append([0.40134, 3.01003])
    waypoints.append([0.38030, 2.80480])
    waypoints.append([0.37849, 2.59737])
    waypoints.append([0.38726, 2.41583])
    waypoints.append([0.41264, 2.23351])
    waypoints.append([0.46003, 2.03406])
    waypoints.append([0.52376, 1.82717])
    waypoints.append([0.60142, 1.64276])
    waypoints.append([0.69965, 1.46500])
    waypoints.append([0.82935, 1.28521])
    waypoints.append([0.95358, 1.15421])
    waypoints.append([1.11083, 1.02714])
    waypoints.append([1.28139, 0.93129])
    waypoints.append([1.48186, 0.85620])
    waypoints.append([1.67607, 0.81144])
    waypoints.append([1.87706, 0.77171])
    waypoints.append([2.06655, 0.79304])
    waypoints.append([2.25617, 0.82425])
    waypoints.append([2.44861, 0.84523])
    return waypoints
