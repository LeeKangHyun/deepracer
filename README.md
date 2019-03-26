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

## NALBAM_LOG

```
fields episodes, steps, x, y, distance, reward, steering, throttle
| filter log == 'NALBAM_LOG' and reward == 1.5
```
