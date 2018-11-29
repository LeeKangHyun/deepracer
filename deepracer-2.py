def reward_function (on_track, x, y, distance_from_center, car_orientation, progress, steps, throttle, steering, track_width, waypoints, closest_waypoint):

    reward = 1e-3

    marker = 0.5 * track_width

    bonus = 0.01 * steps

    if throttle > 0.5 and distance_from_center >= 0.0 and distance_from_center <= marker:
        reward = throttle + bonus - distance_from_center

    return float(reward)
