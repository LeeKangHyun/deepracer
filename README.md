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
| 1 | 5937.289 | nero-DNPds | |
| 2 | 5936.790 | Breadcentric | |
| 3 | 5933.053 | JimWu | |
| 4 | 5930.791 | nalbam-me | |
| 5 | 5930.748 | PGS-Tomasz-Panek | |
| 6 | 5929.387 | hiroisojp | |
| 7 | 5926.414 | kimwooglae | |
| 8 | 5922.419 | TonyJ | <<< |
| 9 | 5922.067 | BespinRacer | |
| 10 | 5917.834 | Etaggel | |
| 11 | 5908.888 | t-maru078 | |
| 12 | 4953.296 | Karl-NAB | |
| 13 | 4948.864 | Fumiaki | |
| 14 | 4946.342 | JasonLian | |
| 15 | 4944.273 | Aiis-DNP | |
| 16 | 4943.274 | sola-DNPds | |
| 17 | 4942.940 | Jouni-Cybercom | |
| 18 | 4942.034 | maeda-ai | |
| 19 | 4940.973 | Jochem | |
| 20 | 4939.588 | leo-DNPds | |
| 21 | 4939.540 | ABaykov | |
| 22 | 4937.950 | mogamin | |
| 23 | 4935.566 | Kire | |
| 24 | 4934.802 | hyeonwoo | |
| 25 | 4932.351 | nalbam | |
| 26 | 4931.985 | RayG | |
| 27 | 4929.189 | HY-DNP | |
| 28 | 4929.051 | Robin-Castro | |
| 29 | 4927.538 | KAGRAZAKA-DNP | |
| 30 | 4926.918 | SF | |
| 31 | 4925.840 | Maverick | |
| 32 | 4922.017 | Alex-Schultz | |
| 33 | 4917.132 | GWP | |
| 34 | 4914.609 | StarlightDreamStudio | |
| 35 | 4907.201 | woodstocktimes | |
