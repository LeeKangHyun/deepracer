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
| 1 | 3962.846 | Karl-NAB | |
| 2 | 3958.175 | Fumiaki | |
| 3 | 3957.463 | Breadcentric | |
| 4 | 3956.187 | Etaggel | |
| 5 | 3956.177 | PGS-Tomasz-Panek | |
| 6 | 3955.775 | nero-DNPds | |
| 7 | 3955.065 | JasonLian | |
| 8 | 3953.709 | sola-DNPds | |
| 9 | 3953.164 | hiroisojp | |
| 10 | 3953.035 | nalbam-me | |
| 11 | 3952.399 | Aiis-DNP | |
| 12 | 3952.129 | maeda-ai | |
| 13 | 3951.848 | Jouni-Cybercom | * |
| 14 | 3951.253 | JimWu | |
| 15 | 3950.448 | kimwooglae | |
| 16 | 3950.365 | ABaykov | |
| 17 | 3950.312 | leo-DNPds | |
| 18 | 3950.223 | Jochem | |
| 19 | 3946.386 | hyeonwoo | |
| 20 | 3945.067 | TonyJ | |
| 21 | 3944.833 | nalbam | |
| 22 | 3944.418 | Kire | |
| 23 | 3943.138 | RichardFan | |
| 24 | 3942.541 | BespinRacer | |
| 25 | 3942.303 | t-maru078 | |
| 26 | 3941.339 | RayG | |
| 27 | 3939.448 | SF | |
| 28 | 3939.003 | HY-DNP | |
| 29 | 3938.550 | KAGRAZAKA-DNP | |
| 30 | 3937.442 | Maverick | |
| 31 | 3937.000 | KJH | |
| 32 | 3933.624 | Alex-Schultz | |
| 33 | 3856.897 | kito-DNPds | |
| 34 | 2970.379 | Paul-NAB | |
| 35 | 2962.347 | mogamin | |
