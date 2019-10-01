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
| 1 | 5934.911 | nero-DNPds | <<< |
| 2 | 5874.202 | BespinRacer | |
| 3 | 4953.296 | Karl-NAB | |
| 4 | 4948.898 | Breadcentric | |
| 5 | 4948.864 | Fumiaki | |
| 6 | 4947.274 | Etaggel | |
| 7 | 4947.059 | PGS-Tomasz-Panek | |
| 8 | 4946.342 | JasonLian | |
| 9 | 4944.273 | Aiis-DNP | |
| 10 | 4943.274 | sola-DNPds | |
| 11 | 4942.940 | Jouni-Cybercom | |
| 12 | 4942.916 | nalbam-me | |
| 13 | 4942.098 | JimWu | |
| 14 | 4942.034 | maeda-ai | |
| 15 | 4941.706 | hiroisojp | |
| 16 | 4941.212 | kimwooglae | |
| 17 | 4940.973 | Jochem | |
| 18 | 4939.588 | leo-DNPds | |
| 19 | 4939.540 | ABaykov | |
| 20 | 4937.950 | mogamin | |
| 21 | 4935.566 | Kire | |
| 22 | 4934.802 | hyeonwoo | |
| 23 | 4934.419 | TonyJ | |
| 24 | 4932.351 | nalbam | |
| 25 | 4931.985 | RayG | |
| 26 | 4929.189 | HY-DNP | |
| 27 | 4929.051 | Robin-Castro | |
| 28 | 4927.538 | KAGRAZAKA-DNP | |
| 29 | 4926.918 | SF | |
| 30 | 4925.840 | Maverick | |
| 31 | 4925.620 | t-maru078 | |
| 32 | 4922.017 | Alex-Schultz | |
| 33 | 4917.132 | GWP | |
| 34 | 4914.609 | StarlightDreamStudio | |
| 35 | 4907.201 | woodstocktimes | |
