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
| 3 | 3950.563 | hiroisojp | |
| 4 | 3950.397 | Aiis-DNP | |
| 5 | 3946.609 | Breadcentric | |
| 6 | 3945.536 | ABaykov | |
| 7 | 3944.698 | nalbam | |
| 8 | 3942.214 | kimwooglae | |
| 9 | 3937.783 | Etaggel | |
| 10 | 3936.764 | Maverick | * |
| 11 | 3936.079 | KAGRAZAKA-DNP | |
| 12 | 3935.732 | KJH | |
| 13 | 3933.089 | Alex-Schultz | |
| 14 | 3856.880 | kito-DNPds | |
| 15 | 2970.874 | Karl-NAB | |
| 16 | 2967.584 | Fumiaki | |
| 17 | 2965.850 | PGS-Tomasz-Panek | |
| 18 | 2964.209 | Jouni-Cybercom | |
| 19 | 2964.173 | maeda-ai | |
| 20 | 2963.992 | sola-DNPds | |
| 21 | 2963.478 | JasonLian | |
| 22 | 2962.347 | mogamin | |
| 23 | 2961.115 | Jochem | |
| 24 | 2961.093 | leo-DNPds | |
| 25 | 2960.280 | yuki-h | |
| 26 | 2959.766 | JimWu | |
| 27 | 2957.114 | hyeonwoo | |
| 28 | 2956.178 | TonyJ | |
| 29 | 2955.560 | t-maru078 | |
| 30 | 2955.534 | BespinRacer | |
| 31 | 2954.999 | Kire | |
| 32 | 2954.772 | Robin-Castro | |
| 33 | 2953.608 | SF | |
| 34 | 2953.045 | RichardFan | |
| 35 | 2950.718 | RayG | |
