# reward_function

def reward_function(self, on_track, x, y, distance_from_center, car_orientation, progress, steps,
                    throttle, steering, track_width, waypoints, closest_waypoints):
    reward = 1e-3

    track_half = track_width * 0.5

    if on_track and distance_from_center < track_half:
        if distance_from_center <= 0.12:
            reward = 1.0
        else:
            reward = 1.0 - (distance_from_center / track_half)

        if x > 5.6 and steering < 0:
            reward *= 1.2

        # add steering penalty
        if abs(steering) > 0.5:
            reward *= 0.8

        # add throttle penalty
        if throttle < 0.5:
            reward *= 0.8

    return float(reward)
