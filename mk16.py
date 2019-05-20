import json
import math
import time

NAME = 'mk16'
ACTION = '18 / 7 / 5 / 1 / 0.3 / 10'

SIGHT = 0.3

MAX_ANGLE = 10

BASE_REWARD = 1.2

g_episode = 0
g_progress = float(0)
g_completed = False
g_waypoints = []
g_total = float(0)
g_start = float(0)
g_time = float(0)


def get_episode(progress, steps):
    global g_episode
    global g_progress
    global g_completed
    global g_waypoints
    global g_total
    global g_start
    global g_time

    # reset
    if g_progress > progress:
        g_episode += 1
        g_total = float(0)
        g_start = time.time()

    g_time = time.time() - g_start

    # completed
    if g_progress < progress and progress == 100:
        g_completed = True
        print('- episode completed - {} - {} - {} - {} - {}'.format(NAME, g_episode,
                                                                    g_time, steps, g_total))
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


def get_next_point(waypoints, coor, closest, distance):
    idx = closest
    dest = []

    while True:
        dest = waypoints[idx]

        dist = get_distance(coor, dest)
        if dist >= distance:
            break

        idx += 1
        if idx >= len(waypoints):
            idx = idx - len(waypoints)

    return dest


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
    closest = get_closest_waypoint(g_waypoints, x, y)

    # distance
    distance = get_distance(g_waypoints[closest], location)

    # point
    destination = get_next_point(g_waypoints, location, closest, SIGHT)

    # diff angle
    diff_angle = get_diff_angle(location, destination, heading, steering)

    if diff_angle <= MAX_ANGLE:
        # angle
        reward += (BASE_REWARD - (diff_angle / MAX_ANGLE))

    # center bonus
    # reward += (BASE_REWARD - (distance_from_center / (track_width / 2)))
    reward += (BASE_REWARD - distance)

    g_total += reward

    # log
    params['name'] = NAME
    params['params'] = ACTION
    params['episode'] = episode
    params['distance'] = distance
    params['diff_angle'] = diff_angle
    params['destination'] = destination
    params['reward'] = reward
    params['total'] = g_total
    params['time'] = g_time
    print(json.dumps(params))

    return float(reward)


def get_waypoints():
    waypoints = []
    waypoints.append([1.94035, 0.49098])
    waypoints.append([2.10949, 0.47186])
    waypoints.append([2.30366, 0.52216])
    waypoints.append([2.49187, 0.57896])
    waypoints.append([2.70113, 0.64410])
    waypoints.append([2.88690, 0.70188])
    waypoints.append([3.07826, 0.75694])
    waypoints.append([3.25871, 0.79749])
    waypoints.append([3.47214, 0.82828])
    waypoints.append([3.69149, 0.85033])
    waypoints.append([3.89634, 0.85518])
    waypoints.append([4.12205, 0.84851])
    waypoints.append([4.29125, 0.83434])
    waypoints.append([4.49736, 0.81931])
    waypoints.append([4.69932, 0.80759])
    waypoints.append([4.89158, 0.79107])
    waypoints.append([5.10026, 0.77661])
    waypoints.append([5.29462, 0.76527])
    waypoints.append([5.49817, 0.75747])
    waypoints.append([5.71260, 0.76328])
    waypoints.append([5.91528, 0.78745])
    waypoints.append([6.12700, 0.83327])
    waypoints.append([6.31700, 0.90607])
    waypoints.append([6.49802, 1.00629])
    waypoints.append([6.65979, 1.12388])
    waypoints.append([6.80490, 1.25931])
    waypoints.append([6.92218, 1.40834])
    waypoints.append([7.01669, 1.56798])
    waypoints.append([7.09863, 1.75796])
    waypoints.append([7.15636, 1.95954])
    waypoints.append([7.19392, 2.16291])
    waypoints.append([7.21113, 2.35393])
    waypoints.append([7.20189, 2.54991])
    waypoints.append([7.16573, 2.75440])
    waypoints.append([7.11127, 2.92866])
    waypoints.append([7.01160, 3.12424])
    waypoints.append([6.88809, 3.28435])
    waypoints.append([6.76799, 3.40563])
    waypoints.append([6.61787, 3.54034])
    waypoints.append([6.44836, 3.67616])
    waypoints.append([6.29044, 3.77696])
    waypoints.append([6.10325, 3.87371])
    waypoints.append([5.92457, 3.95275])
    waypoints.append([5.74289, 4.02382])
    waypoints.append([5.54650, 4.09696])
    waypoints.append([5.35939, 4.16388])
    waypoints.append([5.17303, 4.23065])
    waypoints.append([4.96617, 4.29904])
    waypoints.append([4.77407, 4.34854])
    waypoints.append([4.57539, 4.38311])
    waypoints.append([4.39471, 4.40423])
    waypoints.append([4.18440, 4.41512])
    waypoints.append([3.99403, 4.42345])
    waypoints.append([3.77245, 4.44454])
    waypoints.append([3.58816, 4.47556])
    waypoints.append([3.39611, 4.52311])
    waypoints.append([3.20049, 4.57629])
    waypoints.append([2.93933, 4.65000])
    waypoints.append([2.71416, 4.69749])
    waypoints.append([2.51779, 4.71436])
    waypoints.append([2.29636, 4.70257])
    waypoints.append([2.09302, 4.66396])
    waypoints.append([1.90692, 4.60414])
    waypoints.append([1.71415, 4.51179])
    waypoints.append([1.54774, 4.41156])
    waypoints.append([1.38543, 4.29854])
    waypoints.append([1.23436, 4.17660])
    waypoints.append([1.08817, 4.02995])
    waypoints.append([0.94511, 3.85753])
    waypoints.append([0.83656, 3.70939])
    waypoints.append([0.73716, 3.54193])
    waypoints.append([0.66898, 3.37523])
    waypoints.append([0.61094, 3.14707])
    waypoints.append([0.58670, 2.95627])
    waypoints.append([0.58438, 2.74616])
    waypoints.append([0.59740, 2.55920])
    waypoints.append([0.61999, 2.34588])
    waypoints.append([0.64842, 2.16324])
    waypoints.append([0.68767, 1.99314])
    waypoints.append([0.74499, 1.78968])
    waypoints.append([0.81659, 1.58004])
    waypoints.append([0.88380, 1.41273])
    waypoints.append([0.98521, 1.21572])
    waypoints.append([1.10468, 1.04623])
    waypoints.append([1.24541, 0.88841])
    waypoints.append([1.39852, 0.75614])
    waypoints.append([1.56837, 0.65048])
    waypoints.append([1.73908, 0.57367])
    return waypoints
