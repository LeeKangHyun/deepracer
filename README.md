# deepracer

* <https://github.com/aws-samples/aws-deepracer-workshops>
* <https://github.com/aws-robotics/aws-robomaker-sample-application-deepracer>
* <https://us-west-2.console.aws.amazon.com/sagemaker/home?region=us-west-2>
* <https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-build-your-track.html>
* <https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-vehicle-factory-reset-preparation.html>

## ssh

```bash
sudo ufw allow 22/tcp
```

## wifi

```
# wifi-creds.txt
ssid: 'nalbam-bs'
password: '01067684010'
```

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
fields steps, all_wheels_on_track, x, y, distance_from_center, heading, progress, speed, steering_angle, track_width, closest_waypoints.0, closest_waypoints.1, is_left_of_center, is_reversed
| filter log_key == 'MATDORI_LOG'
| order by @timestamp desc
```

```
fields episodes, steps, x, y, distance, reward, suggest, yaw, range, steering, throttle, waypoint, total, time
| filter log == 'NALBAM_LOG' and waypoint > 40
| order by time desc
```

```json
{"log":"NALBAM_LOG", "json":{"all_wheels_on_track": false, "x": 12, "y": 2, "distance_from_center": 1, "heading": 359.9, "progress": 0, "steps": 1, "speed": 1, "steering_angle": 15, "track_width": 2.5, "waypoints": [[2.5, 0.75], [3.33, 0.75], [4.17, 0.75], [5.0, 0.75], [5.83, 0.75], [6.67, 0.75], [7.5, 0.75], [8.33, 0.75], [9.17, 0.75], [9.75, 0.94], [10.0, 1.5], [10.0, 1.875], [9.92, 2.125], [9.58, 2.375], [9.17, 2.75], [8.33, 2.5], [7.5, 2.5], [7.08, 2.56], [6.67, 2.625], [5.83, 3.44], [5.0, 4.375], [4.67, 4.69], [4.33, 4.875], [4.0, 5.0], [3.33, 5.0], [2.5, 4.95], [2.08, 4.94], [1.67, 4.875], [1.33, 4.69], [0.92, 4.06], [1.17, 3.185], [1.5, 1.94], [1.6, 1.5], [1.83, 1.125], [2.17, 0.885]], "closest_waypoints": [0, 1], "is_left_of_center": true, "is_reversed": true}, "time":"1554780989.8637955"}
```
