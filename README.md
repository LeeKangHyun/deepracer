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
fields name, episode, steps, progress, total, time
| filter progress == 100
| order by time

fields steps, progress, x, y, reward, total, steering_angle, diff_steer, closest, distance, time
| filter name == 'mk31-d' and episode == 91
| order by steps
```

## track

```bash
cat reinvent.json | jq -r '.waypoints[] | "\(.[0]),\(.[1])"'
```

## ssh

```bash
sudo ufw allow 22/tcp
```

## npy

```python
import numpy as np

x = np.load('/Users/nalbam/work/src/github.com/nalbam/aws-deepracer-workshops/log-analysis/tracks/reinvent_base.npy')

np.savetxt('/Users/nalbam/work/src/github.com/nalbam/aws-deepracer-workshops/log-analysis/tracks/reinvent_base.csv', x, delimiter=',')
```
