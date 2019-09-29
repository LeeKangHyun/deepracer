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
| 1 | 4953.203 | Karl-NAB | |
| 2 | 4948.900 | Breadcentric | |
| 3 | 4948.735 | Fumiaki | |
| 4 | 4947.269 | Etaggel | |
| 5 | 4947.062 | PGS-Tomasz-Panek | |
| 6 | 4946.359 | nero-DNPds | |
| 7 | 4946.345 | JasonLian | |
| 8 | 4944.271 | Aiis-DNP | |
| 9 | 4943.271 | sola-DNPds | |
| 10 | 4942.915 | nalbam-me | |
| 11 | 4942.320 | Jouni-Cybercom | <<< |
| 12 | 4942.097 | JimWu | |
| 13 | 4942.031 | maeda-ai | |
| 14 | 4941.702 | hiroisojp | |
| 15 | 4941.208 | kimwooglae | |
| 16 | 4940.972 | Jochem | |
| 17 | 4939.589 | leo-DNPds | |
| 18 | 4939.540 | ABaykov | |
| 19 | 4935.562 | Kire | |
| 20 | 4934.806 | hyeonwoo | |
| 21 | 4934.418 | TonyJ | |
| 22 | 4933.870 | RichardFan | |
| 23 | 4932.403 | BespinRacer | |
| 24 | 4932.355 | nalbam | |
| 25 | 4931.984 | RayG | |
| 26 | 4929.189 | HY-DNP | |
| 27 | 4927.536 | KAGRAZAKA-DNP | |
| 28 | 4926.921 | SF | |
| 29 | 4924.470 | t-maru078 | |
| 30 | 4922.020 | Alex-Schultz | |
| 31 | 4844.969 | kito-DNPds | |
| 32 | 3952.837 | mogamin | |
| 33 | 3937.442 | Maverick | |
| 34 | 3937.075 | Carl | |
| 35 | 3937.000 | KJH | |
