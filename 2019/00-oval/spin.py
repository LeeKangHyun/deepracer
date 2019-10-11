def reward_function(params):
    progress = params["progress"]
    steering = params["steering_angle"]

    reward = 1e-3

    if steering < 0:
        reward = 1.0

    if progress == 100:
        reward = 1000.0

    return float(reward)
