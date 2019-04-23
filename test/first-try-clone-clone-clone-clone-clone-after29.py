'''
Trial	Time	Trial results (% track completed)
1	00:00:33.867	100%
2	00:00:32.820	100%
3	00:00:33.982	100%
4	00:00:34.597	100%
5	00:00:34.771	100%
#action
0	
-30degrees
	
1m/s
1	
-30degrees
	
2m/s
2	
-30degrees
	
3m/s
3	
-20degrees
	
1m/s
4	
-20degrees
	
2m/s
5	
-20degrees
	
3m/s
6	
-10degrees
	
1m/s
7	
-10degrees
	
2m/s
8	
-10degrees
	
3m/s
9	
0degree
	
1m/s
10	
0degree
	
2m/s
11	
0degree
	
3m/s
12	
10degrees
	
1m/s
13	
10degrees
	
2m/s
14	
10degrees
	
3m/s
15	
20degrees
	
1m/s
16	
20degrees
	
2m/s
17	
20degrees
	
3m/s
18	
30degrees
	
1m/s
19	
30degrees
	
2m/s
20	
30degrees
	
3m/s

# hyper

Hyperparameter	Value
Batch size	64
Entropy	0.01
Discount factor	0.999
Final value	1
Epsilon steps	10000
Exploration type	Categorical
Loss type	Huber
Learning rate	0.0003
Number of episodes between each training	20
Number of epochs	10
Stack size	1
'''
from random import randint

def prevent_zigzag(params):
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

def stay_inside(params):
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    
    # Give a very low reward by default
    reward = 1e-3

    # Give a high reward if no wheels go off the track and
    # the car is somewhere in between the track borders
    if all_wheels_on_track and (0.5*track_width - distance_from_center) >= 0.05:
        reward = 1.0

    # Always return a float value
    return float(reward)

def follow_center(params):
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

def is_curve(i):
    if 63 >= i & 67 <= i:
        return True

    if 51 >= i & 53 <= i:
        return True

    if 40 >= i & 45 <= i:
        return True

    if 11 <= i & 24 <= i:
        return True

    return False

def is_stay(i):
    if 63 >= i & 67 <= i:
        return True

    if 51 >= i & 53 <= i:
        return True

    if 40 >= i & 45 <= i:
        return True

    return False
    
def is_strait(i):
    if 12 >= i & 67 <= i:
        return True

    if 53 >= i & 63 <= i:
        return True

    if 43 >= i & 51 <= i:
        return True

    return False
    
def reward_function(params):
    
    nextIndex = params['closest_waypoints'][1]
    if is_strait(nextIndex):
        reward = prevent_zigzag(params)
    elif is_curve(nextIndex):
        reward = stay_inside(params)
    else:
        reward = follow_center(params)

    if params['progress'] == 100:
        reward = reward + 10000.0
    
    print ("YOON {0}/{1}".format(reward, params))
    return float(reward)    
