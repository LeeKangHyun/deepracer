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

## log download

```bash
aws logs get-log-events --log-group-name "/aws/robomaker/SimulationJobs" --log-stream-name "<STREAM_NAME>" --output text --region us-east-1 > deepracer-sim.log
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
| 1 | 5945.337 | Karl-NAB | |
| 2 | 5938.308 | Breadcentric | |
| 3 | 5938.100 | Etaggel | |
| 4 | 5937.822 | PGS-Tomasz-Panek | |
| 5 | 5937.491 | JasonLian | |
| 6 | 5937.289 | nero-DNPds | |
| 7 | 5934.197 | Aiis-DNP | |
| 8 | 5933.782 | Jouni-Cybercom | |
| 9 | 5933.328 | JimWu | |
| 10 | 5933.200 | nalbam-me | |
| 11 | 5933.154 | sola-DNPds | |
| 12 | 5932.703 | kimwooglae | |
| 13 | 5931.388 | Jochem | |
| 14 | 5929.387 | hiroisojp | |
| 15 | 5929.084 | ABaykov | |
| 16 | 5928.808 | leo-DNPds | |
| 17 | 5923.629 | TonyJ | |
| 18 | 5922.873 | RayG | |
| 19 | 5922.375 | BespinRacer | |
| 20 | 5917.856 | Robin-Castro | |
| 21 | 5916.687 | KAGRAZAKA-DNP | |
| 22 | 5916.057 | SF | <<< |
| 23 | 5910.845 | Alex-Schultz | |
| 24 | 5908.888 | t-maru078 | |
| 25 | 5902.471 | StarlightDreamStudio | |
| 26 | 5902.050 | GWP | |
| 27 | 5892.072 | woodstocktimes | |
| 28 | 4948.864 | Fumiaki | |
| 29 | 4946.495 | RichardFan | |
| 30 | 4942.034 | maeda-ai | |
| 31 | 4937.950 | mogamin | |
| 32 | 4935.566 | Kire | |
| 33 | 4934.802 | hyeonwoo | |
| 34 | 4932.351 | nalbam | |
| 35 | 4929.189 | HY-DNP | |
