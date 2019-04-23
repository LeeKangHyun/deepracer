'''
1	00:00:21.954	100%
2	00:00:09.514	42%
3	00:00:24.985	100%

## action
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
-20degrees
1.67m/s
4	
-20degrees
3.33m/s
5	
-20degrees
5m/s
6	
-10degrees
1.67m/s
7	
-10degrees
3.33m/s
8	
-10degrees
5m/s
9	
0degree
1.67m/s
10	
0degree
3.33m/s
11	
0degree
5m/s
12	
10degrees
1.67m/s
13	
10degrees
3.33m/s
14	
10degrees
5m/s
15	
20degrees
1.67m/s
16	
20degrees
3.33m/s
17	
20degrees
5m/s
18	
30degrees
1.67m/s
19	
30degrees
3.33m/s
20	
30degrees
5m/s
##

## hyper
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
    import math
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    
    # Calculate 3 marks that are farther and father away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    marker_4 = 0.75 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.6
    elif distance_from_center <= marker_3:
        reward = 0.3
    elif distance_from_center <= marker_4:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track
    
    # Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 15
    
    # Penalize reward if the car is steering too much
    steeringAngle = params['steering_angle']
    if abs(steeringAngle) > ABS_STEERING_THRESHOLD:  # Only need the absolute steering angle
        reward *= 0.5

    # penalize reward for the car taking slow actions
    # speed is in m/s
    # the below assumes your action space has a maximum speed of 5 m/s and speed granularity of 3
    # we penalize any speed less than 2m/s
    SPEED_THRESHOLD = 2
    speed = params['speed']
    if speed < SPEED_THRESHOLD:
        reward *= 0.5
    elif speed < (SPEED_THRESHOLD / 2):
        reward *= 0.2
    
    # penalize reward for the car heading
    heading = params['heading']
    
    currX = params['x']
    cuurY = params['y']
    #waypoints = params['waypoints']
    prevWaypoint = params['waypoints'][params['closest_waypoints'][0]]
    nextWaypoint = params['waypoints'][params['closest_waypoints'][1]]
    prevX = prevWaypoint[0]
    prevY = prevWaypoint[1]
    nextX = prevWaypoint[0]
    nextY = prevWaypoint[1]
    
    pathDirection = 0
    if prevX == nextX :
        if prevY < nextY :      pathDirection = 90
        elif prevY > nextY :    pathDirection = -90
        else :                  directionAngle = 0          # car stopped
    elif prevY == nextY :
        if prevX <= nextX :      pathDirection = 0
        else :                  pathDirection = -180
    elif prevX < nextX :
        diffX = abs(nextX - prevX)
        diffY = abs(nextY - prevY)
        if nextY > prevY :      pathDirection = math.degrees( math.atan(diffY/diffX) )
        else :                  pathDirection = math.degrees( math.atan(diffY/diffX) ) * -1
    else :
        diffX = abs(prevX - nextX)
        diffY = abs(prevY - nextY)
        if nextY > prevY :      pathDirection = 180 - math.degrees( math.atan(diffY/diffX))
        else :                  pathDirection = mathd.degrees( math.atan(diffY/diffX)) - 180

    if (pathDirection > 0 and heading > 0) :
        if abs(pathDirection - heading) < 5 :
            reward *= 1.1
        elif abs(pathDirection - heading) < 10 :
            reward *= 0.9
        elif abs(pathDirection - heading) < 15 :
            reward *= 0.6
        else :
            reward *= 0.1
    elif (pathDirection < 0 and heading < 0) :
        if abs(pathDirection - heading) < 5 :
            reward *= 1.10
        elif abs(pathDirection - heading) < 10 :
            reward *= 0.9
        elif abs(pathDirection - heading) < 15 :
            reward *= 0.6
        else :
            reward *= 0.1
    else :
        reward *- 0.10
    
    return float(reward)
