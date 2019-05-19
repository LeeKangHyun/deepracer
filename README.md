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
fields episode, steps, progress, reward, total, diff_angle, diff_steer, heading, steering_angle, speed, x, y, distance, time
| filter name == 'mk13-2'
| order by episode desc, steps desc

fields episode, steps, progress, reward, total, diff_angle, diff_steer, heading, steering_angle, speed, x, y, distance, time
| filter name == 'mk13-2' and episode == 737
| order by steps

fields episode, steps, progress, reward, total, diff_angle, diff_steer, heading, steering_angle, speed, x, y, distance, time
| filter name == 'mk13-2' and progress == 100
| order by total desc
```

## track

```bash
cat reinvent.json | jq -r '.waypoints[] | "\(.[0]),\(.[1])"'
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
