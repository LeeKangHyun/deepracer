# deepracer

* <https://github.com/aws-samples/aws-deepracer-workshops>
* <https://github.com/aws-robotics/aws-robomaker-sample-application-deepracer>
* <https://us-west-2.console.aws.amazon.com/sagemaker/home?region=us-west-2>

* <https://docs.aws.amazon.com/ko_kr/deepracer/latest/developerguide/deepracer-build-your-track.html>

## python

```
sudo pip3 install --upgrade gym
sudo pip3 install --upgrade boto3
sudo pip3 install --upgrade Image
```

## reward_function

```
def reward_function (on_track, x, y, distance_from_center, car_orientation, progress, steps,
                     throttle, steering, track_width, waypoints, closest_waypoint):
```

| Name | Type | Description |
| --- | --- | --- |
| on_track | boolean |
| x | float range: [0, 1] |
| y | float range: [0, 1] |
| distance_from_center | float [0, track_width/2] |
| car_orientation | float: [-3.14, 3.14] |
| progress | float: [0, 1] |
| steps | int |
| throttle | float: [0, 1] |
| steering | float: [-1, 1] |
| track_width | float |
| waypoints | ordered list |
| closest_waypoint | int |
| reward | float: [-1e5, 1e5] |

> 1e5 == 100,000

### Advanced Reward Function 1

```python
def reward_function (on_track, x, y, distance_from_center, car_orientation, progress, steps,
                     throttle, steering, track_width, waypoints, closest_waypoint):

    import math

    marker_1 = 0.1 * track_width
    marker_2 = 0.3 * track_width
    marker_3 = 0.5 * track_width

    reward = 1e-3
    if distance_from_center >= 0.0 and distance_from_center <= marker_1:
        reward = 1
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track

    # penalize reward if the car is steering way too much
    ABS_STEERING_THRESHOLD = 0.5
    if abs(steering) > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    return float(reward)
```

### Advanced Reward Function 2

```python
def reward_function (on_track, x, y, distance_from_center, car_orientation, progress, steps,
                     throttle, steering, track_width, waypoints, closest_waypoint):

    import math

    marker_1 = 0.1 * track_width
    marker_2 = 0.3 * track_width
    marker_3 = 0.5 * track_width

    reward = 1e-3
    if distance_from_center >= 0.0 and distance_from_center <= marker_1:
        reward = 1
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track

    # penalize reward for the car taking slow actions
    THROTTLE_THRESHOLD = 0.5
    if throttle < THROTTLE_THRESHOLD:
        reward *= 0.8

    return float(reward)
```

### Advanced Reward Function 3

```python
def reward_function (on_track, x, y, distance_from_center, car_orientation, progress, steps,
                     throttle, steering, track_width, waypoints, closest_waypoint):

    reward = 1e-3
    if distance_from_center >= 0.0 and distance_from_center <= 0.03:
        reward = 1.0

    # add steering penalty
    if abs(steering) > 0.5:
        reward *= 0.80

    # add throttle penalty
    if throttle < 0.5:
        reward *= 0.80

    return reward
```

## MATDORI_LOG

```
fields episodes, steps, x, y, distance, reward, steering, throttle
| filter log == 'MATDORI_LOG' and reward == 1.5
```
