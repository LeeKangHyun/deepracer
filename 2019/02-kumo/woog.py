import time

NAME = "ku03-kimwooglae"
ACTION = "22 / 7 / 8.0 / 2"
HYPER = "512 / 0.999 / 0.00001 / 30"

"""
Gradient descent batch size	512
Entropy	0.01
Discount factor	0.999
Loss type	Huber
Learning rate	0.00001
Number of experience episodes between each policy-updating iteration	30
Number of epochs	10
"""


def reward_function(params):
    prev_waypoint = params["closest_waypoints"][0]
    next_waypoint = params["closest_waypoints"][1]

    # rules1A = [
    #     1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  # 0
    #     1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    #     1, 1, 1, 1, 1, 1, 9, 9, 9, 9,
    #     9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    #     9, 9, 9, 9, 9, 1, 1, 1, 1, 1,
    #     1, 1, 1, 1, 9, 9, 9, 9, 9, 9,  # 50
    #     9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    #     9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    #     9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    #     9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    #     9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  # 100
    #     9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    #     9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    #     9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    #     9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    #     9, 9, 9, 9, 1, 1, 1, 1, 1, 1,  # 150
    #     1, 1, 1, 1, 1, 1, 1, 1, 1,
    #     9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  # prevent error
    #     9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  # prevent error
    #     9, 9, 9, 9, 9, 9, 9, 9, 9, 9  # prevent error
    # ]

    # rules2 = [
    #     1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  # 0
    #     1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    #     1, 1, 1, 1, 1, 9, 9, 9, 9, 9,
    #     9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    #     9, 9, 9, 9, 9, 1, 1, 1, 1, 1,
    #     1, 1, 1, 9, 9, 9, 9, 9, 9, 9,  # 50
    #     9, 9, 9, 9, 2, 2, 2, 2, 2, 2,
    #     2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    #     2, 2, 2, 2, 2, 2, 3, 3, 3, 3,
    #     3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    #     9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  # 100
    #     9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    #     9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    #     9, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    #     2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    #     2, 2, 2, 2, 1, 1, 1, 1, 1, 1,  # 150
    #     1, 1, 1, 1, 1, 1, 1, 1, 1,
    #     9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  # prevent error
    #     9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  # prevent error
    #     9, 9, 9, 9, 9, 9, 9, 9, 9, 9  # prevent error
    # ]

    rules3 = [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,  # 0
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        9,
        9,
        9,
        9,
        9,
        9,
        9,  # 50
        9,
        9,
        9,
        9,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        9,
        9,
        9,
        9,
        9,
        9,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,  # 100
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        1,
        1,
        1,
        1,
        1,
        1,  # 150
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,  # prevent error
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,  # prevent error
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        9,  # prevent error
    ]

    if rules3[next_waypoint] == 1:
        reward = type1(params)
    elif rules3[next_waypoint] == 2:
        reward = type2(params)
    elif rules3[next_waypoint] == 3:
        reward = type3(params)
    else:
        reward = type9(params)

    stdout_ = (
        "MYLOG48A,step=%d,x=%.4f,y=%.4f,reward=%.2f,prev_waypoint=%d,next_waypoint=%d,rule=%d,steering_angle=%.4f,speed=%.4f,distance_from_center=%.2f,track_width=%.2f,progress=%.4f,all_wheels_on_track=%s,is_left_of_center=%s,%s\n"
        % (
            params["steps"],
            params["x"],
            params["y"],
            reward,
            prev_waypoint,
            next_waypoint,
            rules3[next_waypoint],
            params["steering_angle"],
            params["speed"],
            params["distance_from_center"],
            params["track_width"],
            params["progress"],
            params["all_wheels_on_track"],
            params["is_left_of_center"],
            time.time(),
        )
    )
    print(stdout_)

    stdout_ = (
        "MYLOG48B,%d,%.4f,%.4f,%.2f,%d,%d,%d,%.4f,%.4f,%.2f,%.2f,%.4f,%s,%s,%s\n"
        % (
            params["steps"],
            params["x"],
            params["y"],
            reward,
            prev_waypoint,
            next_waypoint,
            rules3[next_waypoint],
            params["steering_angle"],
            params["speed"],
            params["distance_from_center"],
            params["track_width"],
            params["progress"],
            params["all_wheels_on_track"],
            params["is_left_of_center"],
            time.time(),
        )
    )
    print(stdout_)

    return reward


"""
Action number	Steering	Speed
0	-20degrees	4m/s
1	-20degrees	8m/s
2	-13.33degrees	4m/s
3	-13.33degrees	8m/s
4	-6.67degrees	4m/s
5	-6.67degrees	8m/s
6	0degrees	4m/s
7	0degrees	8m/s
8	6.67degrees	4m/s
9	6.67degrees	8m/s
10	13.33degrees	4m/s
11	13.33degrees	8m/s
12	20degrees	4m/s
13	20degrees	8m/s
"""


def type1(params):  # straight
    all_wheels_on_track = params["all_wheels_on_track"]
    steering = params["steering_angle"]
    speed = params["speed"]
    distance_from_center = abs(params["distance_from_center"])
    track_width = params["track_width"]

    if all_wheels_on_track and (0.5 * track_width - distance_from_center) >= 0.05:
        reward = 1
    else:
        print("MYLOG48C-1-A")
        return float(1e-3)

    ABS_STEERING_THRESHOLD10 = 10

    if abs(steering) > ABS_STEERING_THRESHOLD10:
        print("MYLOG48C-1-B")
        return float(1e-3)

    if speed < 5.5:
        print("MYLOG48C-1-C1")
        reward = 0.1
    else:
        print("MYLOG48C-1-C2")
        reward = 1.0
    return float(reward)


def type2(params):  # left
    all_wheels_on_track = params["all_wheels_on_track"]
    speed = params["speed"]
    distance_from_center = abs(params["distance_from_center"])
    track_width = params["track_width"]
    steering = params["steering_angle"]  # left plus, right minus

    if all_wheels_on_track and (0.5 * track_width - distance_from_center) >= 0.05:
        reward = 1
    else:
        print("MYLOG48C-2-A")
        return float(1e-3)

    if speed < 5.5:
        print("MYLOG48C-2-C1")
        reward = 0.1
        if steering > -1:  # turn left or straight
            print("MYLOG48C-2-C11")
            reward = 0.3
    else:
        print("MYLOG48C-2-C2")
        reward = 0.7
        if steering > -1:  # turn left or straight
            print("MYLOG48C-2-C11")
            reward = 1.0
    return float(reward)


def type3(params):  # right
    all_wheels_on_track = params["all_wheels_on_track"]
    speed = params["speed"]
    distance_from_center = abs(params["distance_from_center"])
    track_width = params["track_width"]
    steering = params["steering_angle"]  # left plus, right minus

    if all_wheels_on_track and (0.5 * track_width - distance_from_center) >= 0.05:
        reward = 1
    else:
        print("MYLOG48C-3-A")
        return float(1e-3)

    if speed < 5.5:
        print("MYLOG48C-3-C1")
        reward = 0.1
        if steering < 1:  # turn right or straight
            print("MYLOG48C-3-C11")
            reward = 0.3
    else:
        print("MYLOG48C-3-C2")
        reward = 0.7
        if steering < 1:  # turn right or straight
            print("MYLOG48C-2-C11")
            reward = 1.0
    return float(reward)


def type9(params):
    all_wheels_on_track = params["all_wheels_on_track"]
    speed = params["speed"]
    distance_from_center = abs(params["distance_from_center"])
    track_width = params["track_width"]

    if all_wheels_on_track and (0.5 * track_width - distance_from_center) >= 0.05:
        reward = 1
    else:
        print("MYLOG48C-9-A")
        return float(1e-3)

    if speed < 5.5:
        print("MYLOG48C-9-C1")
        reward = 0.1
    else:
        print("MYLOG48C-9-C2")
        reward = 1.0
    return float(reward)
