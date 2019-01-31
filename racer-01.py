### Gym Env ###
class DeepRacerEnv():

    def reward_function(self, on_track, x, y, distance_from_center, car_orientation, progress, steps,
                        throttle, steering, track_width, waypoints, closest_waypoints):
        reward = 1e-3

        # distance_from_center as reward
        if on_track and distance_from_center >= 0 and track_width > 0:
            reward = (1 - (distance_from_center / (track_width / 2))) * 100

        # add steering penalty
        # if abs(steering) > 0.8:
        #     reward *= 0.5

        # add throttle penalty
        if throttle < 0.3:
            reward *= throttle

        return float(reward)
