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
fields steps, x, y, distance, reward, suggest, yaw, range, steering, throttle, waypoint, progress, time
| filter log == 'NALBAM_LOG'
| order by time desc
```

```
fields episodes, steps, x, y, distance, reward, suggest, yaw, range, steering, throttle, waypoint, total, time
| filter log == 'NALBAM_LOG' and waypoint > 40
| order by time desc
```
