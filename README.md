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
| filter progress == 100 #and name =~ 'sh-'
#| order by time

fields episode, steps, x, y, name, total, diff_progress, time
| filter progress < 0 and name =~ 'sh-'
| order by diff_progress desc, time

fields steps, progress, x, y, reward, total, diff_progress, speed, steering_angle, abs_steer, time
| filter progress > 0 and name == 'sh-30-5-50-1' and episode == 4084
| order by steps

fields @timestamp, @message
| filter @message =~ 'SIM_TRACE_LOG' and @message =~ '0,True'
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
| 1 | 3957.922 | Fumiaki | |
| 2 | 3955.969 | Breadcentric | |
| 3 | 3955.512 | nero-DNPds | |
| 4 | 3954.432 | PGS-Tomasz-Panek | |
| 5 | 3953.479 | JasonLian | * |
| 6 | 3951.753 | nalbam-me | |
| 7 | 3951.207 | Jouni-Cybercom | |
| 8 | 3950.563 | hiroisojp | |
| 9 | 3950.397 | Aiis-DNP | |
| 10 | 3949.508 | leo-DNPds | |
| 11 | 3948.416 | JimWu | |
| 12 | 3947.515 | kimwooglae | |
| 13 | 3947.285 | ABaykov | |
| 14 | 3944.833 | nalbam | |
| 15 | 3942.354 | RichardFan | |
| 16 | 3942.303 | t-maru078 | |
| 17 | 3939.313 | Kire | |
| 18 | 3939.033 | RayG | |
| 19 | 3938.550 | KAGRAZAKA-DNP | |
| 20 | 3938.205 | HY-DNP | |
| 21 | 3937.783 | Etaggel | |
| 22 | 3937.220 | Maverick | |
| 23 | 3937.000 | KJH | |
| 24 | 3933.089 | Alex-Schultz | |
| 25 | 3931.429 | GWP | |
| 26 | 3922.198 | woodstocktimes | |
| 27 | 3856.880 | kito-DNPds | |
| 28 | 2970.874 | Karl-NAB | |
| 29 | 2970.379 | Paul-NAB | |
| 30 | 2964.173 | maeda-ai | |
| 31 | 2963.992 | sola-DNPds | |
| 32 | 2962.347 | mogamin | |
| 33 | 2961.115 | Jochem | |
| 34 | 2960.280 | yuki-h | |
| 35 | 2957.114 | hyeonwoo | |
