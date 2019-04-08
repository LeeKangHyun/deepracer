
def reward_function(params):
    import time

    track_width = params['track_width']
    distance_from_center = params['distance_from_center']

    reward = 0.001

    distance_rate = distance_from_center / (track_width * 0.5)

    if distance_rate <= 0.1:
        reward = 1.0
    elif distance_rate <= 0.3:
        reward = 0.5
    elif distance_rate <= 0.5:
        reward = 0.1

    suggest = 0
    in_range = True

    print('{"log":"NALBAM_LOG",',
            '"steps":%d,' % params['steps'],
            '"x":%.2f,' % params['x'],
            '"y":%.2f,' % params['y'],
            '"waypoint":%d,' % params['closest_waypoint'],
            '"distance":%.2f,' % params['distance_from_center'],
            '"yaw":%.2f,' % params['car_orientation'],
            '"steering":%.2f,' % params['steering_angle'],
            '"throttle":%.2f,' % params['throttle'],
            '"progress":%d,' % params['progress'],
            '"reward":%.2f,' % reward,
            '"suggest":%.2f,' % suggest,
            '"range":"%s",' % in_range,
            '"time":"%s"}' % time.time())

    return float(reward)


def reward_function_example1(params):
    '''
    Example of rewarding the agent to follow center line
    '''

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']

    # Calculate 3 marks that are farther and father away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track

    return float(reward)

def reward_function_example2(params):
    '''
    Example of rewarding the agent to stay inside the two borders of the track
    '''

    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']

    # Give a very low reward by default
    reward = 1e-3

    # Give a high reward if no wheels go off the track and
    # the car is somewhere in between the track borders
    if all_wheels_on_track and (0.5 * track_width - distance_from_center) >= 0.05:
        reward = 1.0

    # Always return a float value
    return float(reward)

def reward_function_example3(params):
    '''
    Example of penalize steering, which helps mitigate zig-zag behaviors
    '''

    # Read input parameters
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering = abs(params['steering_angle']) # Only need the absolute steering angle

    # Calculate 3 marks that are farther and father away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track

    # Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 15

    # Penalize reward if the car is steering too much
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    return float(reward)
