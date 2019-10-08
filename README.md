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
| 1 | 5944.317 | Karl-NAB | <<< |
| 2 | 5938.308 | Breadcentric | |
| 3 | 5938.100 | Etaggel | |
| 4 | 5937.822 | PGS-Tomasz-Panek | |
| 5 | 5937.491 | JasonLian | |
| 6 | 5937.289 | nero-DNPds | |
| 7 | 5934.197 | Aiis-DNP | |
| 8 | 5933.782 | Jouni-Cybercom | |
| 9 | 5933.316 | JimWu | |
| 10 | 5933.200 | nalbam-me | |
| 11 | 5932.703 | kimwooglae | <<< |
| 12 | 5930.987 | Jochem | |
| 13 | 5929.387 | hiroisojp | |
| 14 | 5928.808 | leo-DNPds | |
| 15 | 5928.211 | ABaykov | |
| 16 | 5923.629 | TonyJ | |
| 17 | 5922.375 | BespinRacer | |
| 18 | 5920.920 | RayG | |
| 19 | 5917.795 | Robin-Castro | |
| 20 | 5915.790 | SF | |
| 21 | 5908.888 | t-maru078 | |
| 22 | 5902.050 | GWP | |
| 23 | 5901.895 | StarlightDreamStudio | |
| 24 | 5901.350 | Alex-Schultz | |
| 25 | 5892.072 | woodstocktimes | |
| 26 | 4948.864 | Fumiaki | |
| 27 | 4946.495 | RichardFan | |
| 28 | 4943.274 | sola-DNPds | |
| 29 | 4942.034 | maeda-ai | |
| 30 | 4937.950 | mogamin | |
| 31 | 4935.566 | Kire | |
| 32 | 4934.802 | hyeonwoo | |
| 33 | 4932.351 | nalbam | |
| 34 | 4929.189 | HY-DNP | |
| 35 | 4927.538 | KAGRAZAKA-DNP | |
