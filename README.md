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
| 1 | 5938.308 | Breadcentric | |
| 2 | 5937.822 | PGS-Tomasz-Panek | |
| 3 | 5937.491 | JasonLian | |
| 4 | 5937.289 | nero-DNPds | |
| 5 | 5934.197 | Aiis-DNP | |
| 6 | 5933.782 | Jouni-Cybercom | |
| 7 | 5933.316 | JimWu | |
| 8 | 5933.200 | nalbam-me | |
| 9 | 5931.691 | kimwooglae | |
| 10 | 5930.987 | Jochem | |
| 11 | 5929.387 | hiroisojp | |
| 12 | 5928.808 | leo-DNPds | |
| 13 | 5928.211 | ABaykov | |
| 14 | 5923.629 | TonyJ | |
| 15 | 5922.375 | BespinRacer | |
| 16 | 5919.977 | RayG | |
| 17 | 5917.834 | Etaggel | |
| 18 | 5917.795 | Robin-Castro | |
| 19 | 5915.544 | SF | <<< |
| 20 | 5908.888 | t-maru078 | |
| 21 | 5902.050 | GWP | |
| 22 | 5901.350 | Alex-Schultz | |
| 23 | 5899.328 | Karl-NAB | |
| 24 | 5892.072 | woodstocktimes | |
| 25 | 4948.864 | Fumiaki | |
| 26 | 4946.495 | RichardFan | |
| 27 | 4943.274 | sola-DNPds | |
| 28 | 4942.034 | maeda-ai | |
| 29 | 4937.950 | mogamin | |
| 30 | 4935.566 | Kire | |
| 31 | 4934.802 | hyeonwoo | |
| 32 | 4932.351 | nalbam | |
| 33 | 4929.189 | HY-DNP | |
| 34 | 4927.538 | KAGRAZAKA-DNP | |
| 35 | 4925.840 | Maverick | |
