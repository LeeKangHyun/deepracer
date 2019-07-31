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
| filter progress < 0 and name =~ 'em01-'
| order by diff_progress desc, time

fields steps, progress, x, y, reward, total, diff_progress, speed, steering_angle, abs_steer, time
| filter progress > 0 and name == 'em01-70-a2-678-a' and episode == 792
| order by steps

fields @timestamp, @message
| filter @message =~ 'SIM_TRACE_LOG' #and @message =~ '0,True'
| order by @timestamp desc, @message desc
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
| # | Score | RacerName |   |
| - | ----- | --------- | - |
| 1 | 2970.874 | Karl-NAB | |
| 2 | 2967.584 | Fumiaki | |
| 3 | 2965.850 | PGS-Tomasz-Panek | |
| 4 | 2965.574 | Breadcentric | |
| 5 | 2965.071 | nero-DNPds | |
| 6 | 2965.000 | Etaggel | |
| 7 | 2964.209 | Jouni-Cybercom | |
| 8 | 2964.155 | maeda-ai | * |
| 9 | 2963.992 | sola-DNPds | |
| 10 | 2963.478 | JasonLian | |
| 11 | 2963.137 | hiroisojp | |
| 12 | 2963.031 | nalbam-me | |
| 13 | 2962.967 | Aiis-DNP | |
| 14 | 2962.347 | mogamin | |
| 15 | 2961.899 | ABaykov | |
| 16 | 2961.115 | Jochem | |
| 17 | 2961.093 | leo-DNPds | |
| 18 | 2960.280 | yuki-h | |
| 19 | 2959.766 | JimWu | |
| 20 | 2959.485 | kimwooglae | |
| 21 | 2957.322 | nalbam | |
| 22 | 2956.178 | TonyJ | |
| 23 | 2955.560 | t-maru078 | |
| 24 | 2955.534 | BespinRacer | |
| 25 | 2954.999 | Kire | |
