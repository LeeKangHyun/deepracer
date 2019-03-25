# reward_function

def reward_function(self, on_track, x, y, distance_from_center, car_orientation, progress, steps,
                    throttle, steering, track_width, waypoints, closest_waypoints):
    reward = 0.001

    track_half = track_width * 0.5

    if on_track and distance_from_center < track_half:
        rate = distance_from_center / track_half

        # reward = 1.0 - rate

        if rate < 0.2:
            reward = 1.0
        elif rate < 0.5:
            reward = 0.5
        else:
            reward - 0.1

        # if x > 5.6 and steering < 0:
        #     reward *= 1.2

        # add steering penalty
        if abs(steering) > 0.5:
            reward *= 0.8

        # add throttle penalty
        if throttle < 0.5:
            reward *= 0.8

    return float(reward)
