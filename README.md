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
| 1 | 2969.488 | Karl-NAB | |
| 2 | 2967.584 | Fumiaki | |
| 3 | 2965.574 | Breadcentric | |
| 4 | 2965.549 | PGS-Tomasz-Panek | |
| 5 | 2964.683 | nero-DNPds | |
| 6 | 2964.35 | Etaggel | |
| 7 | 2964.209 | Jouni-Cybercom | |
| 8 | 2963.992 | sola-DNPds | |
| 9 | 2963.335 | JasonLian | |
| 10 | 2963.295 | maeda-ai | |
| 11 | 2963.137 | hiroisojp | |
| 12 | 2963.031 | nalbam-me | |
| 13 | 2962.967 | Aiis-DNP | |
| 14 | 2961.416 | ABaykov | |
| 15 | 2961.115 | Jochem | |
| 16 | 2960.28 | yuki-h | |
| 17 | 2959.677 | JimWu | |
| 18 | 2959.165 | kimwooglae | |
| 19 | 2949.858 | HY-DNP | * |
| 20 | 2946.848 | rkom | * |
| 21 | 2943.282 | Alex-Schultz | * |
| 22 | 2943.073 | Holly | * |
| 23 | 2924.652 | mogamin | * |
| 24 | 1973.989 | ICBart | * |
| 25 | 1973.78 | hyeonwoo | * |
