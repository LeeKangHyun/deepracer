def reward_function (on_track, x, y, distance_from_center, car_orientation, progress, steps, throttle, steering, track_width, waypoints, closest_waypoint):

    reward = 1e-3

    marker = 0.4 * track_width

    if distance_from_center >= 0.0 and distance_from_center <= marker:
        reward = throttle + progress

    return float(reward)
