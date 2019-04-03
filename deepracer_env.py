from __future__ import print_function

import time

# only needed for fake driver setup
import boto3
# gym
import gym
import numpy as np
from gym import spaces
from PIL import Image
import os
import math

# Type of worker
SIMULATION_WORKER = "SIMULATION_WORKER"
SAGEMAKER_TRAINING_WORKER = "SAGEMAKER_TRAINING_WORKER"

node_type = os.environ.get("NODE_TYPE", SIMULATION_WORKER)

if node_type == SIMULATION_WORKER:
    import rospy
    from ackermann_msgs.msg import AckermannDriveStamped
    from gazebo_msgs.msg import ModelState
    from gazebo_msgs.srv import SetModelState

    from sensor_msgs.msg import Image as sensor_image
    from deepracer_msgs.msg import Progress

TRAINING_IMAGE_SIZE = (160, 120)
FINISH_LINE = 100

# REWARD ENUM
CRASHED = 0
NO_PROGRESS = -1
FINISHED = 10000000.0
MAX_STEPS = 1000000

# WORLD NAME
EASY_TRACK_WORLD = 'easy_track'
MEDIUM_TRACK_WORLD = 'medium_track'
HARD_TRACK_WORLD = 'hard_track'

# SLEEP INTERVALS
SLEEP_AFTER_RESET_TIME_IN_SECOND = 0.5
SLEEP_BETWEEN_ACTION_AND_REWARD_CALCULATION_TIME_IN_SECOND = 0.1
SLEEP_WAITING_FOR_IMAGE_TIME_IN_SECOND = 0.01

### Gym Env ###


class DeepRacerEnv(gym.Env):
    def __init__(self):

        screen_height = TRAINING_IMAGE_SIZE[1]
        screen_width = TRAINING_IMAGE_SIZE[0]

        self.on_track = 0
        self.progress = 0
        self.yaw = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.distance_from_center = 0
        self.distance_from_border_1 = 0
        self.distance_from_border_2 = 0
        self.steps = 0
        self.episodes = 0
        self.progress_at_beginning_of_race = 0
        self.prev_closest_waypoint_index = 0
        self.closest_waypoint_index = 0

        # actions -> steering angle, throttle
        self.action_space = spaces.Box(low=np.array(
            [-1, 0]), high=np.array([+1, +1]), dtype=np.float32)

        # given image from simulator
        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(screen_height, screen_width, 3), dtype=np.uint8)

        if node_type == SIMULATION_WORKER:
            # ROS initialization
            self.ack_publisher = rospy.Publisher('/vesc/low_level/ackermann_cmd_mux/output',
                                                 AckermannDriveStamped, queue_size=100)
            self.racecar_service = rospy.ServiceProxy(
                '/gazebo/set_model_state', SetModelState)
            rospy.init_node('rl_coach', anonymous=True)

            # Subscribe to ROS topics and register callbacks
            rospy.Subscriber('/progress', Progress, self.callback_progress)
            rospy.Subscriber('/camera/zed/rgb/image_rect_color',
                             sensor_image, self.callback_image)
            self.world_name = rospy.get_param('WORLD_NAME')
            self.set_waypoints()
            self.track_length = self.calculate_track_length()

            self.aws_region = rospy.get_param('ROS_AWS_REGION')

        self.reward_in_episode = 0
        self.prev_progress = 0

    def reset(self):
        if node_type == SAGEMAKER_TRAINING_WORKER:
            return self.observation_space.sample()

        print('Total Reward=%.2f' % self.reward_in_episode,
              'Total Steps=%.2f' % self.steps)

        self.send_reward_to_cloudwatch(self.reward_in_episode)

        self.reward_in_episode = 0
        self.reward = None
        self.done = False
        self.next_state = None
        self.image = None
        self.steps = 0
        self.episodes += 1
        self.prev_progress = 0
        self.total_progress = 0
        self.action_taken = 2  # straight
        self.prev_action = 2  # straight
        self.prev_closest_waypoint_index = 0  # always starts from first waypoint
        self.closest_waypoint_index = 0

        # Reset car in Gazebo
        self.send_action(0, 0)  # set the throttle to 0
        self.racecar_reset()
        self.steering_angle = 0.0
        self.throttle = 0.0
        self.action_taken = 2.0

        self.infer_reward_state(0, 0)
        return self.next_state

    def racecar_reset(self):
        rospy.wait_for_service('gazebo/set_model_state')

        modelState = ModelState()
        modelState.pose.position.z = 0
        modelState.pose.orientation.x = 0
        modelState.pose.orientation.y = 0
        modelState.pose.orientation.z = 0
        # Use this to randomize the orientation of the car
        modelState.pose.orientation.w = 0
        modelState.twist.linear.x = 0
        modelState.twist.linear.y = 0
        modelState.twist.linear.z = 0
        modelState.twist.angular.x = 0
        modelState.twist.angular.y = 0
        modelState.twist.angular.z = 0
        modelState.model_name = 'racecar'

        if self.world_name.startswith(MEDIUM_TRACK_WORLD):
            modelState.pose.position.x = -1.40
            modelState.pose.position.y = 2.13
        elif self.world_name.startswith(EASY_TRACK_WORLD):
            modelState.pose.position.x = -1.44
            modelState.pose.position.y = -0.06
        elif self.world_name.startswith(HARD_TRACK_WORLD):
            modelState.pose.position.x = 1.75
            modelState.pose.position.y = 0.6

            def toQuaternion(pitch, roll, yaw):
                cy = np.cos(yaw * 0.5)
                sy = np.sin(yaw * 0.5)
                cr = np.cos(roll * 0.5)
                sr = np.sin(roll * 0.5)
                cp = np.cos(pitch * 0.5)
                sp = np.sin(pitch * 0.5)

                w = cy * cr * cp + sy * sr * sp
                x = cy * sr * cp - sy * cr * sp
                y = cy * cr * sp + sy * sr * cp
                z = sy * cr * cp - cy * sr * sp
                return [x, y, z, w]

            # clockwise
            quaternion = toQuaternion(roll=0.0, pitch=0.0, yaw=np.pi)
            # anti-clockwise
            quaternion = toQuaternion(roll=0.0, pitch=0.0, yaw=0.0)
            modelState.pose.orientation.x = quaternion[0]
            modelState.pose.orientation.y = quaternion[1]
            modelState.pose.orientation.z = quaternion[2]
            modelState.pose.orientation.w = quaternion[3]

        else:
            raise ValueError(
                "Unknown simulation world: {}".format(self.world_name))

        self.racecar_service(modelState)
        time.sleep(SLEEP_AFTER_RESET_TIME_IN_SECOND)
        self.progress_at_beginning_of_race = self.progress

    def step(self, action):
        if node_type == SAGEMAKER_TRAINING_WORKER:
            return self.observation_space.sample(), 0, False, {}

        # initialize rewards, next_state, done
        self.reward = None
        self.done = False
        self.next_state = None

        steering_angle = float(action[0])
        throttle = float(action[1])
        self.steps += 1
        self.send_action(steering_angle, throttle)
        time.sleep(SLEEP_BETWEEN_ACTION_AND_REWARD_CALCULATION_TIME_IN_SECOND)
        self.infer_reward_state(steering_angle, throttle)

        info = {}  # additional data, not to be used for training
        return self.next_state, self.reward, self.done, info

    def callback_image(self, data):
        self.image = data

    def callback_progress(self, data):
        self.on_track = not (data.off_track)
        self.progress = data.progress
        self.yaw = data.yaw
        self.x = data.x
        self.y = data.y
        self.z = data.z
        self.distance_from_center = data.distance_from_center
        self.distance_from_border_1 = data.distance_from_border_1
        self.distance_from_border_2 = data.distance_from_border_2

    def send_action(self, steering_angle, throttle):
        ack_msg = AckermannDriveStamped()
        ack_msg.header.stamp = rospy.Time.now()
        ack_msg.drive.steering_angle = steering_angle
        ack_msg.drive.speed = throttle
        self.ack_publisher.publish(ack_msg)

    def reward_function(self, on_track, x, y, distance_from_center, car_orientation, progress, steps,
                        throttle, steering, track_width, waypoints, closest_waypoints):
        reward = 0.001

        distance_rate = distance_from_center / (track_width * 0.5)

        if distance_rate <= 0.1:
            reward = 1.0
        elif distance_rate <= 0.3:
            reward = 0.5
        elif distance_rate <= 0.5:
            reward = 0.1

        # penalize reward if the car is steering way too much
        if abs(steering) > math.radians(15):
            reward *= 0.5

        # penalize reward for the car taking slow actions
        if throttle < 1.0:
            reward *= 0.5

        return float(reward)

        # if distance_from_center >= 0.0 and distance_from_center <= 0.02:
        #     return 1.0
        # elif distance_from_center >= 0.02 and distance_from_center <= 0.03:
        #     return 0.3
        # elif distance_from_center >= 0.03 and distance_from_center <= 0.05:
        #     return 0.1
        # return 1e-3  # like crashed

    def infer_reward_state(self, steering_angle, throttle):
        # Wait till we have a image from the camera
        while not self.image:
            time.sleep(SLEEP_WAITING_FOR_IMAGE_TIME_IN_SECOND)

        # Car environment spits out BGR images by default. Converting to the
        # image to RGB.
        image = Image.frombytes('RGB', (self.image.width, self.image.height),
                                self.image.data, 'raw', 'RGB', 0, 1)
        # resize image ans perform anti-aliasing
        image = image.resize(TRAINING_IMAGE_SIZE, resample=2).convert("RGB")
        state = np.array(image)

        #total_progress = self.progress - self.progress_at_beginning_of_race
        #self.prev_progress = total_progress

        # calculate the closest way point
        self.closest_waypoint_index = self.get_closest_waypoint()
        # calculate the current progress with respect to the way points
        current_progress = self.calculate_current_progress(
            self.closest_waypoint_index, self.prev_closest_waypoint_index)
        self.total_progress = current_progress + self.prev_progress
        # re-assign the prev progress and way point variables
        self.prev_progress = self.total_progress
        self.prev_closest_waypoint_index = self.closest_waypoint_index

        suggest_radians = self.get_suggest_radians(self.closest_waypoint_index)

        done = False
        on_track = self.on_track
        if on_track != 1:
            reward = CRASHED
            done = True
        # elif total_progress >= FINISH_LINE:  # reached max waypoints
        #    print("Congratulations! You finished the race!")
        #    if self.steps == 0:
        #        reward = 0.0
        #        done = False
        #    else:
        #        reward = FINISHED / self.steps
        #        done = True
        else:
            reward = self.reward_function(on_track, self.x, self.y, self.distance_from_center, self.yaw,
                                          self.total_progress, self.steps, throttle, steering_angle, self.road_width,
                                          list(self.waypoints), self.get_closest_waypoint())

            # reward += 0.5  # reward bonus for surviving

            in_allow = False
            pi_allow_range = 0.2

            if suggest_radians > (math.pi - pi_allow_range) or suggest_radians < (math.pi * -1) + pi_allow_range:
                if self.yaw <= math.pi and self.yaw >= (suggest_radians - pi_allow_range):
                    in_allow = True
                elif self.yaw >= (math.pi * -1) and self.yaw <= (suggest_radians + pi_allow_range):
                    in_allow = True
            else:
                if self.yaw >= (suggest_radians - pi_allow_range) and self.yaw <= (suggest_radians + pi_allow_range):
                    in_allow = True

            if in_allow == True:
                reward += 0.7
            else:
                reward -= 0.3

            # smooth
            # if self.action_taken == self.prev_action:
            #    reward += 0.5

            self.prev_action = self.action_taken

        print('Step No=%.2f' % self.steps,
              'Step Reward=%.2f' % reward)

        self.reward_in_episode += reward
        self.reward = reward
        self.done = done
        self.next_state = state

        print('{"log":"NALBAM_LOG",',
              '"episodes":%d,' % self.episodes,
              '"steps":%d,' % self.steps,
              '"x":%.2f,' % self.x,
              '"y":%.2f,' % self.y,
              '"waypoint":%d,' % self.closest_waypoint_index,
              '"distance":%.2f,' % self.distance_from_center,
              '"rad":%.2f,' % suggest_radians,
              '"yaw":%.2f,' % self.yaw,
              '"steering":%.2f,' % steering_angle,
              '"throttle":%.2f,' % throttle,
              '"action":%d,' % self.action_taken,
              '"reward":%.2f,' % self.reward,
              '"total":%.2f,' % self.reward_in_episode,
              '"progress":%d,' % self.total_progress,
              '"current":%.2f,' % current_progress,
              '"on":"%s",' % self.on_track,
              '"done":"%s"}' % self.done)

        # aws cloudwatch insights
        # fields episodes, steps, x, y
        # | filter log == 'NALBAM_LOG'

        # Trace logs to help us debug and visualize the training runs
        stdout_ = 'SIM_TRACE_LOG:%d,%d,%.4f,%.4f,%.4f,%.2f,%.2f,%d,%.4f,%.4f,%d,%s,%s,%.4f,%d,%d,%.2f,%s\n' % (
            self.episodes, self.steps, self.x, self.y,
            self.yaw,
            self.steering_angle,
            self.throttle,
            self.action_taken,
            self.reward,
            self.total_progress,
            0,  # self.get_waypoint_action(), #the expert action at the next waypoint
            self.done,
            self.on_track,
            current_progress,
            0,  # self.initidxWayPoint, #starting waypoint for an episode
            self.closest_waypoint_index,
            self.track_length,
            time.time())
        print(stdout_)

    def send_reward_to_cloudwatch(self, reward):
        session = boto3.session.Session()
        cloudwatch_client = session.client(
            'cloudwatch', region_name=self.aws_region)
        cloudwatch_client.put_metric_data(
            MetricData=[
                {
                    'MetricName': 'DeepRacerRewardPerEpisode',
                    'Unit': 'None',
                    'Value': reward
                },
            ],
            Namespace='AWSRoboMakerSimulation'
        )

    def set_waypoints(self):
        if self.world_name.startswith(MEDIUM_TRACK_WORLD):
            self.waypoints = vertices = np.zeros((8, 2))
            self.road_width = 0.50
            vertices[0] = [-0.99, 2.25]
            vertices[1] = [0.69, 2.26]
            vertices[2] = [1.37, 1.67]
            vertices[3] = [1.48, -1.54]
            vertices[4] = [0.81, -2.44]
            vertices[5] = [-1.25, -2.30]
            vertices[6] = [-1.67, -1.64]
            vertices[7] = [-1.73, 1.63]

        elif self.world_name.startswith(EASY_TRACK_WORLD):
            self.waypoints = vertices = np.zeros((2, 2))
            self.road_width = 0.90
            vertices[0] = [-1.08, -0.05]
            vertices[1] = [1.08, -0.05]

        else:
            self.waypoints = vertices = np.zeros((42, 2))
            self.road_width = 0.44
            vertices[0] = [1.50, 0.58]
            vertices[1] = [2.50, 0.58]
            vertices[2] = [3.50, 0.58]
            vertices[3] = [4.50, 0.58]
            vertices[4] = [5.50, 0.58]
            vertices[5] = [5.60, 0.60]
            vertices[6] = [5.70, 0.65]
            vertices[7] = [5.80, 0.70]
            vertices[8] = [5.90, 0.80]
            vertices[9] = [6.00, 0.90]

            vertices[10] = [6.08, 1.10]
            vertices[11] = [6.10, 1.20]
            vertices[12] = [6.10, 1.30]
            vertices[13] = [6.10, 1.40]
            vertices[14] = [6.07, 1.50]
            vertices[15] = [6.05, 1.60]
            vertices[16] = [6.00, 1.70]
            vertices[17] = [5.90, 1.80]
            vertices[18] = [5.75, 1.90]
            vertices[19] = [5.60, 2.00]

            vertices[20] = [5.10, 2.00]
            vertices[21] = [4.60, 2.00]
            vertices[22] = [4.20, 2.00]
            vertices[23] = [4.10, 2.05]
            vertices[24] = [4.00, 2.10]
            vertices[25] = [3.90, 2.15]
            vertices[26] = [2.70, 3.80]
            vertices[27] = [2.60, 3.90]
            vertices[28] = [2.40, 4.00]
            vertices[29] = [2.30, 4.00]

            vertices[30] = [1.20, 3.95]
            vertices[31] = [1.10, 3.92]
            vertices[32] = [1.00, 3.88]
            vertices[33] = [0.80, 3.72]
            vertices[34] = [0.60, 3.40]
            vertices[35] = [0.58, 3.30]
            vertices[36] = [0.57, 3.20]
            vertices[37] = [1.00, 1.00]
            vertices[38] = [1.10, 0.90]
            vertices[39] = [1.20, 0.80]

            vertices[40] = [1.30, 0.70]
            vertices[41] = [1.40, 0.60]

    def get_suggest_radians(self, closest_waypoint_index):
        coor1 = self.waypoints[closest_waypoint_index]

        if closest_waypoint_index == 0:
            coor2 = self.waypoints[1]

            res = math.atan2((coor2[1] - coor1[1]), (coor2[0] - coor1[0]))

        elif closest_waypoint_index == (len(self.waypoints) - 1):
            coor2 = self.waypoints[0]

            res = math.atan2((coor2[1] - coor1[1]), (coor2[0] - coor1[0]))

        else:
            coor3 = self.waypoints[closest_waypoint_index - 1]
            coor4 = self.waypoints[closest_waypoint_index + 1]

            distance3 = self.calculate_distance(
                coor1[0], coor3[0], coor1[1], coor3[1])
            distance4 = self.calculate_distance(
                coor1[0], coor4[0], coor1[1], coor4[1])

            if distance3 > distance4:
                res = math.atan2((coor4[1] - coor1[1]), (coor4[0] - coor1[0]))
            else:
                res = math.atan2((coor1[1] - coor3[1]), (coor1[0] - coor3[0]))

        return res

    def calculate_distance(self, x1, x2, y1, y2):
        return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

    def get_closest_waypoint(self):
        res = 0
        index = 0
        x = self.x
        y = self.y
        minDistance = float('inf')
        for row in self.waypoints:
            distance = self.calculate_distance(row[0], x, row[1],  y)
            if distance < minDistance:
                minDistance = distance
                res = index
            index = index + 1
        return res

    def calculate_current_progress(self, closest_waypoint_index, prev_closest_waypoint_index):
        current_progress = 0.0

        # calculate distance in meters
        coor1 = self.waypoints[closest_waypoint_index]
        coor2 = self.waypoints[prev_closest_waypoint_index]
        current_progress = self.calculate_distance(
            coor1[0], coor2[0], coor1[1], coor2[1])

        # convert to ratio and then percentage
        current_progress /= self.track_length
        current_progress *= 100.0

        return current_progress

    def calculate_track_length(self):
        track_length = 0.0
        prev_row = self.waypoints[0]
        for row in self.waypoints[1:]:
            track_length += self.calculate_distance(
                row[0], prev_row[0], row[1], prev_row[1])
            prev_row = row

        if track_length == 0.0:
            print('ERROR: Track length is zero.')
            raise

        return track_length


class DeepRacerDiscreteEnv(DeepRacerEnv):
    def __init__(self):
        DeepRacerEnv.__init__(self)

        self.action_space = spaces.Discrete(15)

    def step(self, action):

        # Convert discrete to continuous
        throttle = 1.0
        throttle_multiplier = 0.8
        throttle = throttle * throttle_multiplier
        steering_angle = 0.8

        self.throttle, self.steering_angle = self.two_steering_three_throttle_15_states(
            throttle, steering_angle, action)

        self.action_taken = action

        continous_action = [self.steering_angle, self.throttle]

        return super().step(continous_action)

    def default_6_actions(self, throttle, steering_angle, action):
        if action == 0:  # move left
            steering_angle = 0.8
        elif action == 1:  # move right
            steering_angle = -0.8
        elif action == 2:  # straight
            steering_angle = 0
        elif action == 3:  # move slight left
            steering_angle = 0.2
        elif action == 4:  # move slight right
            steering_angle = -0.2
        elif action == 5:  # slow straight
            steering_angle = 0
            throttle = throttle / 2
        else:  # should not be here
            raise ValueError("Invalid action")

        return throttle, steering_angle

    def two_steering_one_throttle_5_states(self, throttle_, steering_angle_, action):
        if action == 0:  # move left
            steering_angle = 1 * steering_angle_
            throttle = throttle_
        elif action == 1:  # move right
            steering_angle = -1 * steering_angle_
            throttle = throttle_
        elif action == 2:  # move left
            steering_angle = 0.5 * steering_angle_
            throttle = throttle_
        elif action == 3:  # move right
            steering_angle = -0.5 * steering_angle_
            throttle = throttle_
        elif action == 4:  # straight
            steering_angle = 0
            throttle = throttle_

        else:  # should not be here
            raise ValueError("Invalid action")

        return throttle, steering_angle

    def two_steering_two_throttle_10_states(self, throttle_, steering_angle_, action):
        if action == 0:  # move left
            steering_angle = 1 * steering_angle_
            throttle = throttle_
        elif action == 1:  # move right
            steering_angle = -1 * steering_angle_
            throttle = throttle_
        elif action == 2:  # move left
            steering_angle = 0.5 * steering_angle_
            throttle = throttle_
        elif action == 3:  # move right
            steering_angle = -0.5 * steering_angle_
            throttle = throttle_
        elif action == 4:  # straight
            steering_angle = 0
            throttle = throttle_

        elif action == 5:  # move left
            steering_angle = 1 * steering_angle_
            throttle = throttle_ * 0.5
        elif action == 6:  # move right
            steering_angle = -1 * steering_angle_
            throttle = throttle_ * 0.5
        elif action == 7:  # move left
            steering_angle = 0.5 * steering_angle_
            throttle = throttle_ * 0.5
        elif action == 8:  # move right
            steering_angle = -0.5 * steering_angle_
            throttle = throttle_ * 0.5
        elif action == 9:  # straight
            steering_angle = 0
            throttle = throttle_ * 0.5

        else:  # should not be here
            raise ValueError("Invalid action")

        return throttle, steering_angle

    def two_steering_three_throttle_15_states(self, throttle_, steering_angle_, action):

        # Convert discrete to continuous
        if action == 0:  # move left
            steering_angle = steering_angle_
            throttle = throttle_
        elif action == 1:  # move right
            steering_angle = -1 * steering_angle_
            throttle = throttle_
        elif action == 2:  # move left
            steering_angle = 0.5 * steering_angle_
            throttle = throttle_
        elif action == 3:  # move right
            steering_angle = -0.5 * steering_angle_
            throttle = throttle_
        elif action == 4:  # straight
            steering_angle = 0
            throttle = throttle_

        elif action == 5:  # move left
            steering_angle = steering_angle_
            throttle = 0.5 * throttle_
        elif action == 6:  # move right
            steering_angle = -1 * steering_angle_
            throttle = 0.5 * throttle_
        elif action == 7:  # move left
            steering_angle = 0.5 * steering_angle_
            throttle = 0.5 * throttle_
        elif action == 8:  # move right
            steering_angle = -0.5 * steering_angle_
            throttle = 0.5 * throttle_
        elif action == 9:  # slow straight
            steering_angle = 0
            throttle = throttle_ * 0.5

        elif action == 10:  # move left
            steering_angle = 1 * steering_angle_
            throttle = throttle_ * 2.0
        elif action == 11:  # move right
            steering_angle = -1 * steering_angle_
            throttle = throttle_ * 2.0
        elif action == 12:  # move left
            steering_angle = 0.5 * steering_angle_
            throttle = throttle_ * 2.0
        elif action == 13:  # move right
            steering_angle = -0.5 * steering_angle_
            throttle = throttle_ * 2.0
        elif action == 14:  # fast straight
            steering_angle = 0
            throttle = throttle_ * 2.0

        else:  # should not be here
            raise ValueError("Invalid action")

        return throttle, steering_angle
