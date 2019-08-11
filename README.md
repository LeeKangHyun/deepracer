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
| 1 | 3958.175 | Fumiaki | |
| 2 | 3957.004 | Breadcentric | |
| 3 | 3956.187 | Etaggel | |
| 4 | 3955.650 | nero-DNPds | |
| 5 | 3954.432 | PGS-Tomasz-Panek | |
| 6 | 3954.030 | JasonLian | |
| 7 | 3953.709 | sola-DNPds | |
| 8 | 3953.035 | nalbam-me | |
| 9 | 3952.399 | Aiis-DNP | |
| 10 | 3951.726 | Jouni-Cybercom | |
| 11 | 3950.997 | JimWu | |
| 12 | 3950.563 | hiroisojp | |
| 13 | 3949.933 | leo-DNPds | |
| 14 | 3949.045 | kimwooglae | |
| 15 | 3949.001 | Jochem | |
| 16 | 3948.547 | ABaykov | |
| 17 | 3944.833 | nalbam | |
| 18 | 3943.625 | Kire | |
| 19 | 3942.790 | RichardFan | |
| 20 | 3942.541 | BespinRacer | * |
| 21 | 3942.303 | t-maru078 | |
| 22 | 3939.309 | RayG | |
| 23 | 3939.003 | HY-DNP | |
| 24 | 3938.550 | KAGRAZAKA-DNP | |
| 25 | 3937.442 | Maverick | |
| 26 | 3937.375 | TonyJ | |
| 27 | 3937.000 | KJH | |
| 28 | 3933.248 | Alex-Schultz | |
| 29 | 3931.429 | GWP | |
| 30 | 3922.198 | woodstocktimes | |
| 31 | 3856.897 | kito-DNPds | |
| 32 | 2970.874 | Karl-NAB | |
| 33 | 2970.379 | Paul-NAB | |
| 34 | 2964.173 | maeda-ai | |
| 35 | 2962.347 | mogamin | |
