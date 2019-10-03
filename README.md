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
| 5 | 5933.238 | JimWu | |
| 6 | 5933.200 | nalbam-me | |
| 7 | 5931.691 | kimwooglae | |
| 8 | 5929.387 | hiroisojp | |
| 9 | 5928.808 | leo-DNPds | |
| 10 | 5927.931 | ABaykov | |
| 11 | 5923.629 | TonyJ | |
| 12 | 5922.067 | BespinRacer | |
| 13 | 5917.834 | Etaggel | |
| 14 | 5914.759 | Robin-Castro | |
| 15 | 5908.888 | t-maru078 | |
| 16 | 5902.050 | GWP | |
| 17 | 5901.350 | Alex-Schultz | |
| 18 | 5899.328 | Karl-NAB | |
| 19 | 5892.072 | woodstocktimes | <<< |
| 20 | 4948.864 | Fumiaki | |
| 21 | 4944.273 | Aiis-DNP | |
| 22 | 4943.274 | sola-DNPds | |
| 23 | 4942.940 | Jouni-Cybercom | |
| 24 | 4942.034 | maeda-ai | |
| 25 | 4940.973 | Jochem | |
| 26 | 4937.950 | mogamin | |
| 27 | 4935.566 | Kire | |
| 28 | 4934.802 | hyeonwoo | |
| 29 | 4932.351 | nalbam | |
| 30 | 4931.985 | RayG | |
| 31 | 4929.189 | HY-DNP | |
| 32 | 4927.538 | KAGRAZAKA-DNP | |
| 33 | 4926.918 | SF | |
| 34 | 4925.840 | Maverick | |
| 35 | 4914.609 | StarlightDreamStudio | |
