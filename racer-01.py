def reward_function (on_track, x, y, distance_from_center, car_orientation, progress, steps, throttle, steering, track_width, waypoints, closest_waypoint):

    reward = 1e-3

    marker = 0.3 * track_width

    # distance_from_center as reward
    if distance_from_center <= marker:
        reward = 1 - (distance_from_center / track_width / 2)

    return float(reward)
