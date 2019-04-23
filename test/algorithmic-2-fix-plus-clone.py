'''
1	00:00:25.549	100%
2	00:00:23.815	100%
3	00:00:24.388	100%
4	00:00:12.221	53%
5	00:00:24.839	100%
# action
0	
-30degrees
	
1.67m/s
1	
-30degrees
	
3.33m/s
2	
-30degrees
	
5m/s
3	
-15degrees
	
1.67m/s
4	
-15degrees
	
3.33m/s
5	
-15degrees
	
5m/s
6	
0degree
	
1.67m/s
7	
0degree
	
3.33m/s
8	
0degree
	
5m/s
9	
15degrees
	
1.67m/s
10	
15degrees
	
3.33m/s
11	
15degrees
	
5m/s
12	
30degrees
	
1.67m/s
13	
30degrees
	
3.33m/s
14	
30degrees
	
5m/s
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

import math

def speed_up(params):
	'''
	Example that penalizes slow driving. This create a non-linear reward function so it may take longer to learn.
	'''

	# Calculate 3 marks that are farther and father away from the center line
	marker_1 = 0.1 * params['track_width']
	marker_2 = 0.25 * params['track_width']
	marker_3 = 0.5 * params['track_width']

	# Give higher reward if the car is closer to center line and vice versa
	if params['distance_from_center'] <= marker_1:
		reward = 1
	elif params['distance_from_center'] <= marker_2:
		reward = 0.5
	elif params['distance_from_center'] <= marker_3:
		reward = 0.1
	else:
		reward = 1e-3  # likely crashed/ close to off track

	# penalize reward for the car taking slow actions
	# speed is in m/s
	# the below assumes your action space has a maximum speed of 5 m/s and speed granularity of 3
	# we penalize any speed less than 2m/s
	SPEED_THRESHOLD = 2
	if params['speed'] < SPEED_THRESHOLD:
		reward *= 0.5

	return float(reward)

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

def is_strait(c, n, heading, w):
    n = n + 4;
    if n > len(w) - 1:
        n -= len(w)
    
    a = w[n][0] - w[c][0]
    b = w[n][1] - w[c][1]
    deg = 0
    if a == 0:
        deg = 0
    else:
        deg = math.atan(b/a) * 180.0 / math.pi
    
    if abs(heading-deg)>=30.0:
        return 3

    if abs(heading-deg)>=15.0:
        return 2 

    return 1
    
def reward_function(params):
    currentIndex = params['closest_waypoints'][0]
    nextIndex = params['closest_waypoints'][1]
    heading = params['heading']
    steering = params['steering_angle']
    deg = heading + steering
    
    if params['is_reversed']:
        return 1e-3;
    
    f = is_strait(currentIndex, nextIndex, deg, params['waypoints'])
    
    if 1e-3 == stay_inside(params):
        reward = 1e-3
    elif f == 3:
        reward = prevent_zigzag(params)
    elif f == 2:
        reward = follow_center(params)
    else:
        reward = speed_up(params)

    if params['progress'] == 100:
        reward = reward + 10000.0
    
    # print ("YOON {0}/{1}".format(reward, params))
    return float(reward)    
