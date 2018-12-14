def reward_function (on_track, x, y, distance_from_center, car_orientation, progress, steps, throttle, steering, track_width, waypoints, closest_waypoint):

    reward = 1e-3

    marker = 0.3 * track_width

    # distance_from_center as reward
    if distance_from_center <= marker:
        reward = (track_width * 0.5) - distance_from_center

    # add steering penalty
    if abs(steering) > 0.5:
        reward *= 0.8

    # add throttle penalty
    if throttle < 0.5:
        reward *= 0.8

    # if not on_track:
    #     reward *= 0.1

    return float(reward)
