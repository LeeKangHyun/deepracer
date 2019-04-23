'''
1	00:00:31.210	100%
2	00:00:32.231	100%
3	00:00:33.095	100%
# action
0	
-30degrees
0.83m/s
1	
-30degrees
1.67m/s
2	
-30degrees
2.5m/s
3	
-20degrees
0.83m/s
4	
-20degrees
1.67m/s
5	
-20degrees
2.5m/s
6	
-10degrees
0.83m/s
7	
-10degrees
1.67m/s
8	
-10degrees
2.5m/s
9	
0degree
0.83m/s
10	
0degree
1.67m/s
11	
0degree
2.5m/s
12	
10degrees
0.83m/s
13	
10degrees
1.67m/s
14	
10degrees
2.5m/s
15	
20degrees
0.83m/s
16	
20degrees
1.67m/s
17	
20degrees
2.5m/s
18	
30degrees
0.83m/s
19	
30degrees
1.67m/s
20	
30degrees
2.5m/s
# hyper
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
    
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    is_left_of_center = params['is_left_of_center']
    
    
    if all_wheels_on_track == False:
        return 1e-3
    
    
    # Calculate 3 marks that are farther and father away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    marker_4 = 0.75 * track_width
    marker_5 = 0.99 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 0.75
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.3
    elif distance_from_center <= marker_4:
        reward = 0.2
    elif distance_from_center <= marker_5:
        reward = 0.1
        
    else:
        reward = 1e-3  # likely crashed/ close to off track
        
    if is_left_of_center == True:
        reward *= 0.1
    
    if speed < 1:
        reward -= 0.05
    elif speed < 2:
        reward += 0.1
    elif speed < 3:
        reward += 0.1
        
    ABS_STEERING_THRESHOLD = 30
    # Penalize reward if the car is steering too much
    if abs(params['steering_angle']) > ABS_STEERING_THRESHOLD:
       reward *= 0.5
      
    SPEED_THRESHOLD = 2
    if params['speed'] < SPEED_THRESHOLD:
       reward *= 0.3
    
    return float(reward)