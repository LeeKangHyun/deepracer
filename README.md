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
| 1 | 3958.116 | Fumiaki | * |
| 2 | 3956.382 | Breadcentric | |
| 3 | 3955.650 | nero-DNPds | |
| 4 | 3954.432 | PGS-Tomasz-Panek | |
| 5 | 3954.008 | JasonLian | |
| 6 | 3953.559 | sola-DNPds | |
| 7 | 3952.251 | Aiis-DNP | |
| 8 | 3952.095 | nalbam-me | |
| 9 | 3951.726 | Jouni-Cybercom | |
| 10 | 3950.563 | hiroisojp | |
| 11 | 3949.933 | leo-DNPds | |
| 12 | 3949.521 | JimWu | |
| 13 | 3947.896 | kimwooglae | |
| 14 | 3947.285 | ABaykov | |
| 15 | 3944.833 | nalbam | |
| 16 | 3943.011 | Kire | |
| 17 | 3942.790 | RichardFan | |
| 18 | 3942.303 | t-maru078 | |
| 19 | 3939.309 | RayG | |
| 20 | 3939.003 | HY-DNP | |
| 21 | 3938.550 | KAGRAZAKA-DNP | |
| 22 | 3937.783 | Etaggel | |
| 23 | 3937.442 | Maverick | |
| 24 | 3937.000 | KJH | |
| 25 | 3933.248 | Alex-Schultz | |
| 26 | 3931.429 | GWP | |
| 27 | 3922.198 | woodstocktimes | |
| 28 | 3856.880 | kito-DNPds | |
| 29 | 2970.874 | Karl-NAB | |
| 30 | 2970.379 | Paul-NAB | |
| 31 | 2964.173 | maeda-ai | |
| 32 | 2962.347 | mogamin | |
| 33 | 2961.115 | Jochem | |
| 34 | 2960.280 | yuki-h | |
| 35 | 2957.114 | hyeonwoo | |
