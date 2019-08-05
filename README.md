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
| 1 | 3957.771 | Fumiaki | |
| 2 | 3955.512 | nero-DNPds | |
| 3 | 3954.432 | PGS-Tomasz-Panek | * |
| 4 | 3951.624 | nalbam-me | |
| 5 | 3951.207 | Jouni-Cybercom | |
| 6 | 3950.563 | hiroisojp | |
| 7 | 3950.397 | Aiis-DNP | |
| 8 | 3947.515 | kimwooglae | |
| 9 | 3947.285 | ABaykov | |
| 10 | 3946.609 | Breadcentric | |
| 11 | 3945.988 | JimWu | |
| 12 | 3944.833 | nalbam | |
| 13 | 3938.320 | KAGRAZAKA-DNP | |
| 14 | 3938.179 | RayG | |
| 15 | 3937.783 | Etaggel | |
| 16 | 3937.220 | Maverick | |
| 17 | 3936.215 | HY-DNP | |
| 18 | 3935.732 | KJH | |
| 19 | 3933.089 | Alex-Schultz | |
| 20 | 3931.429 | GWP | |
| 21 | 3922.198 | woodstocktimes | |
| 22 | 3856.880 | kito-DNPds | |
| 23 | 2970.874 | Karl-NAB | |
| 24 | 2970.379 | Paul-NAB | |
| 25 | 2964.173 | maeda-ai | |
| 26 | 2963.992 | sola-DNPds | |
| 27 | 2963.478 | JasonLian | |
| 28 | 2962.347 | mogamin | |
| 29 | 2961.115 | Jochem | |
| 30 | 2961.093 | leo-DNPds | |
| 31 | 2960.280 | yuki-h | |
| 32 | 2957.114 | hyeonwoo | |
| 33 | 2956.178 | TonyJ | |
| 34 | 2955.560 | t-maru078 | |
| 35 | 2955.534 | BespinRacer | |
