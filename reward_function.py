# reward_function


def reward_function(self, on_track, x, y, distance_from_center, car_orientation, progress, steps,
                    throttle, steering, track_width, waypoints, closest_waypoints):
    reward = 0.001

    if on_track:
        distance_rate = distance_from_center / (track_width * 0.5)

        if distance_rate <= 0.2:
            reward = 1.0
        elif distance_rate <= 0.4:
            reward = 0.5
        elif distance_rate <= 0.8:
            reward = 0.1

        # if x > 5.6 and steering < 0:
        #     reward *= 1.2

        # add steering penalty (math.radians(15) = 0.26)
        if abs(steering) > 0.26:
            reward *= 0.8

        # add throttle penalty
        if throttle < 2.0:
            reward *= 0.8

    return float(reward)
