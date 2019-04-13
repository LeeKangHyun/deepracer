# deepracer

* <https://github.com/aws-samples/aws-deepracer-workshops>
* <https://github.com/aws-robotics/aws-robomaker-sample-application-deepracer>
* <https://us-west-2.console.aws.amazon.com/sagemaker/home?region=us-west-2>
* <https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-build-your-track.html>
* <https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-vehicle-factory-reset-preparation.html>

## python

```bash
sudo pip3 install --upgrade gym
sudo pip3 install --upgrade boto3
sudo pip3 install --upgrade Image
```

## insight

```
fields steps, progress, reward, in_range, angle, yaw, heading, steering_angle, speed, x, y, distance_from_center, closest_waypoints, is_left_of_center, is_reversed
| filter log_key == 'mat-5-10' and reward > 0.9
| order by @timestamp desc, steps desc
```

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
