'''
Trial Time Trial results (% track completed)
1	00:00:28.580	100%
2	00:00:28.050	100%
3	00:00:27.668	100%
4	00:00:28.529	100%
5	00:00:27.832	100%

# action
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
-15degrees
1m/s
4	
-15degrees
2m/s
5	
-15degrees
3m/s
6	
0degree
1m/s
7	
0degree
2m/s
8	
0degree
3m/s
9	
15degrees
1m/s
10	
15degrees
2m/s
11	
15degrees
3m/s
12	
30degrees
1m/s
13	
30degrees
2m/s
14	
30degrees
3m/s

# action
Hyperparameter
Value
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

def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    
    
    all_wheels_on_track = params['all_wheels_on_track']
    if all_wheels_on_track == False:
        return 1e-3
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']

    # Calculate 3 marks that are farther and father away from the center line
    marker_1 = 0.025 * track_width
    marker_2 = 0.05 * track_width
    marker_3 = 0.075 * track_width
    marker_4 = 0.1 * track_width
    marker_11 = 0.125 * track_width
    marker_12 = 0.15 * track_width
    marker_13 = 0.175 * track_width
    marker_14 = 0.2 * track_width
    marker_21 = 0.225 * track_width
    marker_22 = 0.25 * track_width
    marker_23 = 0.275 * track_width
    marker_24 = 0.3 * track_width
    marker_31 = 0.325 * track_width
    marker_32 = 0.35 * track_width
    marker_33 = 0.375 * track_width
    marker_34 = 0.4 * track_width
    marker_41 = 0.425 * track_width
    marker_42 = 0.45 * track_width
    marker_43 = 0.475 * track_width
    marker_44 = 0.5 * track_width
    marker_51 = 0.525 * track_width
    marker_52 = 0.55 * track_width
    marker_53 = 0.575 * track_width
    marker_54 = 0.6 * track_width
    marker_61 = 0.625 * track_width
    marker_62 = 0.65 * track_width
    marker_63 = 0.675 * track_width
    marker_64 = 0.7 * track_width
    marker_71 = 0.725 * track_width
    marker_72 = 0.75 * track_width
    marker_73 = 0.775 * track_width
    marker_74 = 0.8 * track_width
    marker_81 = 0.825 * track_width
    marker_82 = 0.85 * track_width
    marker_83 = 0.875 * track_width
    marker_84 = 0.9 * track_width
    marker_91 = 0.925 * track_width
    marker_92 = 0.95 * track_width
    marker_93 = 0.975 * track_width
    marker_94 = 0.999 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 0.99
    elif distance_from_center <= marker_2:
        reward = 0.95
    elif distance_from_center <= marker_3:
        reward = 0.93
    elif distance_from_center <= marker_4:
        reward = 0.90
    elif distance_from_center <= marker_11:
        reward = 0.87
    elif distance_from_center <= marker_12:
        reward = 0.85
    elif distance_from_center <= marker_13:
        reward = 0.83
    elif distance_from_center <= marker_14:
        reward = 0.80
    elif distance_from_center <= marker_21:
        reward = 0.57
    elif distance_from_center <= marker_22:
        reward = 0.55
    elif distance_from_center <= marker_23:
        reward = 0.53
    elif distance_from_center <= marker_24:
        reward = 0.50
    elif distance_from_center <= marker_31:
        reward = 0.37
    elif distance_from_center <= marker_32:
        reward = 0.35
    elif distance_from_center <= marker_33:
        reward = 0.33
    elif distance_from_center <= marker_34:
        reward = 0.30
    elif distance_from_center <= marker_41:
        reward = 0.27
    elif distance_from_center <= marker_42:
        reward = 0.25
    elif distance_from_center <= marker_43:
        reward = 0.23
    elif distance_from_center <= marker_44:
        reward = 0.20
    elif distance_from_center <= marker_51:
        reward = 0.17
    elif distance_from_center <= marker_52:
        reward = 0.15
    elif distance_from_center <= marker_53:
        reward = 0.13
    else:
        reward = 1e-3  # likely crashed/ close to off track
        
        
    is_left_of_center = params['is_left_of_center']
    if is_left_of_center == True:
        reward += 0.1
    else:
        reward *= 0.8
        
        
    ABS_STEERING_THRESHOLD = 20
    # Penalize reward if the car is steering too much
    if abs(params['steering_angle']) > ABS_STEERING_THRESHOLD:
        reward *= 0.1
    else:
        reward *= 1.1
      
    SPEED_THRESHOLD = 2
    speed = params['speed']
    if speed < SPEED_THRESHOLD:
        reward *= 0.1
    else:
        reward *= 1.1


    return float(reward)