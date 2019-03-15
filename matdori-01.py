### Gym Env ###
class DeepRacerEnv():

    def __init__(self):

        self.episodes = 0
        self.steps = 0
        self.x = 0
        self.y = 0
        self.distance_from_center = 0
        self.yaw = 0
        self.road_width = 0
        self.y = 0
        self.on_track = 0
        self.done = 0

    def reward_function(self, on_track, x, y, distance_from_center, car_orientation, progress, steps,
                        throttle, steering, track_width, waypoints, closest_waypoints):
        reward = 1e-3

        track_half = track_width / 2.0

        # distance_from_center as reward
        if on_track and distance_from_center < track_half:
            reward = 1.0 - (distance_from_center / track_half)

        # # add steering penalty
        # if abs(steering) > 0.8:
        #     reward *= 0.5

        # # add throttle penalty
        # if throttle < 0.3:
        #     reward *= throttle

        return float(reward)

    def infer_reward_state(self, steering_angle, throttle):
        reward = 0

        print('MATDORI_LOG',
              'ep=%d' % self.episodes,
              'step=%d' % self.steps,
              'x=%.2f' % self.x,
              'y=%.2f' % self.y,
              'distance=%.2f' % self.distance_from_center,
              'yaw=%.2f' % self.yaw,
              'throttle=%.2f' % throttle,
              'steering=%.2f' % steering_angle,
              'road_width=%.2f' % self.road_width,
              'reward=%.2f' % reward,
              'on_track=%s' % self.on_track,
              'done=%s' % self.done)
