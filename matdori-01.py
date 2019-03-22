### Gym Env ###
class DeepRacerEnv():

    def reward_function(self, on_track, x, y, distance_from_center, car_orientation, progress, steps,
                        throttle, steering, track_width, waypoints, closest_waypoints):
        reward = 1e-3

        track_half = track_width * 0.5

        # distance_from_center as reward
        if on_track and distance_from_center < track_half:
            reward = 1.0 - (distance_from_center / track_half)

        return float(reward)
