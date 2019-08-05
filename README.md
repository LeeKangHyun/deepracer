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
| filter progress == 100 #and name == 'sh01-70-a'
#| order by time

fields episode, steps, x, y, name, total, diff_progress, time
| filter progress < 0 and name =~ 'sh01-'
| order by diff_progress desc, time

fields steps, progress, x, y, reward, total, diff_progress, speed, steering_angle, abs_steer, time
| filter progress > 0 and name == 'sh01-80-30' and episode == 4084
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
| 1 | 3957.599 | Fumiaki | * |
| 2 | 3955.512 | nero-DNPds | |
| 3 | 3951.624 | nalbam-me | |
| 4 | 3951.207 | Jouni-Cybercom | |
| 5 | 3950.563 | hiroisojp | |
| 6 | 3950.397 | Aiis-DNP | |
| 7 | 3947.285 | ABaykov | |
| 8 | 3947.192 | kimwooglae | |
| 9 | 3946.609 | Breadcentric | |
| 10 | 3945.988 | JimWu | |
| 11 | 3944.698 | nalbam | |
| 12 | 3938.320 | KAGRAZAKA-DNP | |
| 13 | 3938.179 | RayG | |
| 14 | 3937.783 | Etaggel | |
| 15 | 3937.220 | Maverick | |
| 16 | 3935.732 | KJH | |
| 17 | 3933.089 | Alex-Schultz | |
| 18 | 3856.880 | kito-DNPds | |
| 19 | 2970.874 | Karl-NAB | |
| 20 | 2965.850 | PGS-Tomasz-Panek | |
| 21 | 2964.173 | maeda-ai | |
| 22 | 2963.992 | sola-DNPds | |
| 23 | 2963.478 | JasonLian | |
| 24 | 2962.347 | mogamin | |
| 25 | 2961.115 | Jochem | |
| 26 | 2961.093 | leo-DNPds | |
| 27 | 2960.280 | yuki-h | |
| 28 | 2957.114 | hyeonwoo | |
| 29 | 2956.178 | TonyJ | |
| 30 | 2955.560 | t-maru078 | |
| 31 | 2955.534 | BespinRacer | |
| 32 | 2954.999 | Kire | |
| 33 | 2954.772 | Robin-Castro | |
| 34 | 2953.608 | SF | |
| 35 | 2953.045 | RichardFan | |
