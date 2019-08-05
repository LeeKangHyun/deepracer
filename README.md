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
| 1 | 3955.512 | nero-DNPds | |
| 2 | 3951.624 | nalbam-me | |
| 3 | 3951.207 | Jouni-Cybercom | |
| 4 | 3950.563 | hiroisojp | |
| 5 | 3950.397 | Aiis-DNP | |
| 6 | 3947.285 | ABaykov | |
| 7 | 3946.609 | Breadcentric | |
| 8 | 3946.365 | kimwooglae | |
| 9 | 3944.698 | nalbam | |
| 10 | 3938.179 | RayG | |
| 11 | 3937.783 | Etaggel | |
| 12 | 3937.220 | Maverick | * |
| 13 | 3936.079 | KAGRAZAKA-DNP | |
| 14 | 3935.732 | KJH | |
| 15 | 3933.089 | Alex-Schultz | |
| 16 | 3856.880 | kito-DNPds | |
| 17 | 2970.874 | Karl-NAB | |
| 18 | 2967.584 | Fumiaki | |
| 19 | 2965.850 | PGS-Tomasz-Panek | |
| 20 | 2964.173 | maeda-ai | |
| 21 | 2963.992 | sola-DNPds | |
| 22 | 2963.478 | JasonLian | |
| 23 | 2962.347 | mogamin | |
| 24 | 2961.115 | Jochem | |
| 25 | 2961.093 | leo-DNPds | |
| 26 | 2960.280 | yuki-h | |
| 27 | 2959.766 | JimWu | |
| 28 | 2957.114 | hyeonwoo | |
| 29 | 2956.178 | TonyJ | |
| 30 | 2955.560 | t-maru078 | |
| 31 | 2955.534 | BespinRacer | |
| 32 | 2954.999 | Kire | |
| 33 | 2954.772 | Robin-Castro | |
| 34 | 2953.608 | SF | |
| 35 | 2953.045 | RichardFan | |
