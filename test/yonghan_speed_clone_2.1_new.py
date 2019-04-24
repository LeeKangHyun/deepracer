def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    import math

    # Read input parameters

    all_wheels_on_track = params['all_wheels_on_track']
    x = params['x']
    y = params['y']
    distance_from_center = params['distance_from_center']
    is_left_of_center = params['is_left_of_center']
    is_reversed = params['is_reversed']
    heading = params['heading']
    progress = params['progress']
    steps = params['steps']
    speed = params['speed']
    steering_angle = params['steering_angle']
    track_width = params['track_width']
    waypoints = params['waypoints']
    prev_closest_waypoint_index = params['closest_waypoints'][0]
    closest_waypoint_index = params['closest_waypoints'][1]
    prev_closest_waypoint = waypoints[prev_closest_waypoint_index]
    next_closest_waypoint = waypoints[closest_waypoint_index]


    # Calculate 3 marks that are farther and father away from the center line
    marker_1 = 0.2 * track_width
    marker_2 = 0.35 * track_width
    marker_3 = 0.5 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.45
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track


    # (차체 + 바퀴 steering 각도) - (인접 전후 waypoint의 각도) 가 5도 이하 일때 리워드
    waypoints_yaw = math.atan2(next_closest_waypoint[1] - prev_closest_waypoint[1],
                               next_closest_waypoint[0] - prev_closest_waypoint[0])
    yaw = math.radians(heading + steering_angle)
    if math.fabs(yaw - waypoints_yaw) <= math.radians(5):
        reward *= 2

    # 직선 구간에서 최대 속도 낼 때 리워드
    straight_index = [[0, 10],[25,30],[45,50],[53, 61]]
    for from_, to_ in straight_index:
        if closest_waypoint_index in list(range(from_, to_)) and speed > 4:
            reward += .45

    # 전 구간에서 속도 클 때 리워드
    if speed > 4 :
        reward *= 2

    import time
    stdout_ = 'steps: %d, x: %.4f, y: %.4f, heading: %.2f, steering: %.2f, speed: %.2f, reward: %.4f, progress: %.4f,' \
              ' on_track: %s, closest_waypoint_idx: %d, is_left_of_center: %s, is_reversed: %s, time: %s\n' % (
                  steps, x, y,
                  heading,
                  steering_angle,
                  speed,
                  reward,
                  progress,
                  all_wheels_on_track,
                  closest_waypoint_index,
                  is_left_of_center,
                  is_reversed,
                  time.time())
    print(stdout_)

    return float(reward)
