# deepracer

* <https://github.com/aws-samples/aws-deepracer-workshops>
* <https://github.com/aws-robotics/aws-robomaker-sample-application-deepracer>
* <https://us-west-2.console.aws.amazon.com/sagemaker/home?region=us-west-2>
* <https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-build-your-track.html>
* <https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-vehicle-factory-reset-preparation.html>
* <https://github.com/aws-samples/aws-deepracer-workshops/blob/master/Workshops/2019-AWSSummits-AWSDeepRacerService/Lab1/Readme-Korean.md>

## python

```bash
sudo pip3 install --upgrade gym
sudo pip3 install --upgrade boto3
sudo pip3 install --upgrade Image
```

## insight

```
fields name, episode, steps, total, progress, time
| filter progress == 100 #and name == 'em01-70-a'
#| order by time

fields episode, steps, x, y, name, total, diff_progress, time
| filter progress < 0 #and name == 'em01-70-a'
| order by diff_progress desc, time

fields steps, progress, x, y, reward, total, diff_progress, speed, steering_angle, diff_steer, time
| filter progress > 0 and name == 'em01-70-a' and episode == 1783
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

x = np.load('aws.npy')

np.savetxt('new.csv', x, delimiter=',')
```

## leaderboard

<!-- leaderboard -->
| # | RacerName | Point |   |
| - | --------- | ----- | - |
| 1 | 2969.488 | Karl-NAB | |
| 2 | 2966.789 | Fumiaki | |
| 3 | 2965.215 | Breadcentric | |
| 4 | 2964.209 | Jouni-Cybercom | |
| 5 | 2964.15 | Etaggel | |
| 6 | 2963.848 | sola-DNPds | |
| 7 | 2963.302 | nero-DNPds | |
| 8 | 2963.295 | maeda-ai | |
| 9 | 2963.031 | nalbam-me | |
| 10 | 2962.95 | hiroisojp | |
| 11 | 2962.92 | Aiis-DNP | |
| 12 | 2962.732 | JasonLian | |
| 13 | 2962.426 | PGS-Tomasz-Panek | |
| 14 | 2960.431 | ABaykov | |
| 15 | 2959.315 | leo-DNPds | * |
| 16 | 2959.016 | kimwooglae | |
| 17 | 2957.322 | nalbam | |
| 18 | 2957.277 | Jochem | |
| 19 | 2956.151 | TonyJ | |
| 20 | 2955.56 | t-maru078 | |
| 21 | 2954.999 | Kire | |
| 22 | 2953.207 | KAGRAZAKA-DNP | |
| 23 | 2953.045 | RichardFan | |
| 24 | 2946.848 | rkom | |
| 25 | 2946.237 | HY-DNP | |
