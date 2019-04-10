# reward_function 2

def reward_function(params):
    import json

    speed = params['speed']

    reward = 0.001

    if speed <= 0.1:
        reward = 1.0
    elif speed <= 0.3:
        reward = 0.5
    elif speed <= 0.5:
        reward = 0.1

    params['log_key'] = 'MATDORI_STEP2'
    print(json.dumps(params))

    return float(reward)
