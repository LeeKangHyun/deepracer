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
import random

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

## NALBAM CONFIG ##
CHK_SPEED = True
CHK_STEER = True
CHK_ANGLE = False

MAX_SPEED = 5
MIN_SPEED = MAX_SPEED * 0.8

MAX_STEER = 15

MAX_ANGLE = 10

LOG_KEY = 'mat'

if CHK_SPEED:
    LOG_KEY += '-{}'.format(MAX_SPEED)
else:
    LOG_KEY += '-0'

if CHK_STEER:
    LOG_KEY += '-s{}'.format(MAX_STEER)

if CHK_ANGLE:
    LOG_KEY += '-a{}'.format(MAX_ANGLE)

START_POS = [[2.20, 0.58], [4.65, 2.00]]
## NALBAM CONFIG ##

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

        # print('Total Reward Reward=%.2f' % self.reward_in_episode,
        #       'Total Steps=%.2f' % self.steps)

        print('Episodes=%d' % self.episodes,
              'Total Steps=%d' % self.steps,
              'Total Reward=%.2f' % self.reward_in_episode)

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
        self.action_taken = 4  # straight
        self.prev_action = 4  # straight
        self.prev_closest_waypoint_index = 0  # always starts from first waypoint
        self.closest_waypoint_index = 0

        # Reset car in Gazebo
        self.send_action(0, 0)  # set the throttle to 0
        self.racecar_reset()
        self.steering_angle = 0.0
        self.throttle = 0.0
        self.action_taken = 4.0

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
            wayPoints = [2, 23]
            wayPoint = random.choice(wayPoints)

            modelState.pose.position.x = self.waypoints[wayPoint][0]
            modelState.pose.position.y = self.waypoints[wayPoint][1]

            if wayPoint < 5:
                yaw = 0.0
            else:
                yaw = math.pi

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
            quaternion = toQuaternion(roll=0.0, pitch=0.0, yaw=yaw)
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
        import json
        import math

        def calculate_distance(x1, x2, y1, y2):
            return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

        def get_closest_waypoints(w, c, x, y):
            z = len(w) - 1
            if c == 0:
                p1 = calculate_distance(w[z][0], x, w[z][1], y)
                p2 = calculate_distance(w[1][0], x, w[1][1], y)
                if p1 > p2:
                    return [c, 1]
                else:
                    return [z, c]
            elif c == z:
                p1 = calculate_distance(w[z-1][0], x, w[z-1][1], y)
                p2 = calculate_distance(w[0][0], x, w[0][1], y)
                if p1 > p2:
                    return [c, 0]
                else:
                    return [z-1, c]
            else:
                p1 = calculate_distance(w[c-1][0], x, w[c-1][1], y)
                p2 = calculate_distance(w[c+1][0], x, w[c+1][1], y)
                if p1 > p2:
                    return [c, c+1]
                else:
                    return [c-1, c]

        def is_range(yaw, angle, allow):
            in_range = False
            if angle > (math.pi - allow) or angle < (math.pi * -1) + allow:
                if yaw <= math.pi and yaw >= (angle - allow):
                    in_range = True
                elif yaw >= (math.pi * -1) and yaw <= (angle + allow):
                    in_range = True
            else:
                if yaw >= (angle - allow) and yaw <= (angle + allow):
                    in_range = True
            return in_range

        # def slack(message):
        #     import json
        #     import requests
        #     url = 'https://hooks.slack.com/services/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'
        #     data = json.dumps(message)
        #     requests.post(url, json={'text': data}, headers={'Content-Type': 'application/json'})

        closest_waypoints = get_closest_waypoints(
            waypoints, closest_waypoints, x, y)
        heading = math.cos(car_orientation)
        params = {
            'all_wheels_on_track': on_track,
            'x': x,
            'y': y,
            'distance_from_center': distance_from_center,
            'is_left_of_center': False,
            'is_reversed': False,
            'heading': heading,
            'progress': progress,
            'steps': steps,
            'speed': throttle,
            'steering_angle': steering,
            'track_width': track_width
            # 'closest_waypoints' : closest_waypoints,
            # 'waypoints' : waypoints
        }

        reward = 0.001

        speed = params['speed']
        heading = params['heading']
        track_width = params['track_width']
        distance_from_center = params['distance_from_center']
        # closest_waypoints = params['closest_waypoints']
        # waypoints = params['waypoints']

        # center
        distance_rate = distance_from_center / track_width

        if distance_rate <= 0.1:
            reward = 1.0
        elif distance_rate <= 0.2:
            reward = 0.5
        elif distance_rate <= 0.4:
            reward = 0.1

        # speed
        if CHK_SPEED and speed > MIN_SPEED:
            reward *= 1.5

        # steering
        if CHK_STEER and steering > MAX_STEER:
            reward *= 0.75

        # angle
        coor1 = waypoints[closest_waypoints[0]]
        coor2 = waypoints[closest_waypoints[1]]
        angle = math.atan2((coor2[1] - coor1[1]), (coor2[0] - coor1[0]))
        yaw = math.radians(heading)
        allow = math.radians(MAX_ANGLE)
        in_range = is_range(yaw, angle, allow)

        if CHK_ANGLE and in_range:
            reward *= 1.3

        params['log_key'] = LOG_KEY
        params['yaw'] = yaw
        params['angle'] = angle
        params['in_range'] = in_range
        params['reward'] = reward
        print(json.dumps(params))

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

        # total_progress = self.progress - self.progress_at_beginning_of_race
        # self.prev_progress = total_progress

        # calculate the closest way point
        self.closest_waypoint_index = self.get_closest_waypoint()
        # calculate the current progress with respect to the way points
        current_progress = self.calculate_current_progress(self.closest_waypoint_index, self.prev_closest_waypoint_index)
        self.total_progress = current_progress + self.prev_progress
        # re-assign the prev progress and way point variables
        self.prev_progress = self.total_progress
        self.prev_closest_waypoint_index = self.closest_waypoint_index

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

            reward += 0.5 #reward bonus for surviving

            # smooth
            # if self.action_taken == self.prev_action:
            #    reward += 0.5

            self.prev_action = self.action_taken

        # print('Step No=%.2f' % self.steps,
        #       'Step Reward=%.2f' % reward)

        print('Episodes=%d' % self.episodes,
              'This Steps=%d' % self.steps,
              'This Reward=%.2f' % reward)

        self.reward_in_episode += reward
        self.reward = reward
        self.done = done
        self.next_state = state

        # Trace logs to help us debug and visualize the training runs
        stdout_ = 'SIM_TRACE_LOG:%d,%d,%.4f,%.4f,%.4f,%.2f,%.2f,%d,%.4f,%.4f,%d,%s,%s,%.4f,%d,%d,%.2f,%s\n' % (
        self.episodes, self.steps, self.x, self.y,
        self.yaw,
        self.steering_angle,
        self.throttle,
        self.action_taken,
        self.reward,
        self.total_progress,
        0, #self.get_waypoint_action(), #the expert action at the next waypoint
        self.done,
        self.on_track,
        current_progress,
        0, #self.initidxWayPoint, #starting waypoint for an episode
        self.closest_waypoint_index,
        self.track_length,
        time.time())
        print(stdout_)

    def send_reward_to_cloudwatch(self, reward):
        session = boto3.session.Session()
        cloudwatch_client = session.client('cloudwatch', region_name=self.aws_region)
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
            vertices[0][0] = -0.99; vertices[0][1] = 2.25;
            vertices[1][0] = 0.69;  vertices[1][1] = 2.26;
            vertices[2][0] = 1.37;  vertices[2][1] = 1.67;
            vertices[3][0] = 1.48;  vertices[3][1] = -1.54;
            vertices[4][0] = 0.81;  vertices[4][1] = -2.44;
            vertices[5][0] = -1.25; vertices[5][1] = -2.30;
            vertices[6][0] = -1.67; vertices[6][1] = -1.64;
            vertices[7][0] = -1.73; vertices[7][1] = 1.63;

        elif self.world_name.startswith(EASY_TRACK_WORLD):
            self.waypoints = vertices = np.zeros((2, 2))
            self.road_width = 0.90
            vertices[0][0] = -1.08;   vertices[0][1] = -0.05;
            vertices[1][0] =  1.08;   vertices[1][1] = -0.05;

        else:
            self.waypoints = vertices = np.zeros((44, 2))
            self.road_width = 0.44
            vertices[0] =  [1.5, 0.58]
            vertices[1] =  [2, 0.58]
            vertices[2] =  [3, 0.58]
            vertices[3] =  [4, 0.58]
            vertices[4] =  [4.5, 0.58]
            vertices[5] =  [5, 0.58]
            vertices[6] =  [5.25, 0.58]
            vertices[7] =  [5.5, 0.58]
            vertices[8] =  [5.6, 0.6]
            vertices[9] =  [5.7, 0.65]
            vertices[10] =  [5.8, 0.7]
            vertices[11] =  [5.9, 0.8]
            vertices[12] =  [6, 0.9]
            vertices[13] =  [6.08, 1.1]
            vertices[14] =  [6.1, 1.2]
            vertices[15] =  [6.1, 1.3]
            vertices[16] =  [6.1, 1.4]
            vertices[17] =  [6.07, 1.5]
            vertices[18] =  [6.05, 1.6]
            vertices[19] =  [6, 1.7]
            vertices[20] =  [5.9, 1.8]
            vertices[21] =  [5.75, 1.9]
            vertices[22] =  [5.6, 2]
            vertices[23] =  [5.45, 2]
            vertices[24] =  [5.25, 2]
            vertices[25] =  [5, 2]
            vertices[26] =  [4.8, 2]
            vertices[27] =  [4.2, 2.02]
            vertices[28] =  [4, 2.1]
            vertices[29] =  [3.3, 3]
            vertices[30] =  [2.6, 3.92]
            vertices[31] =  [2.4, 4]
            vertices[32] =  [1.3, 4]
            vertices[33] =  [2, 4]
            vertices[34] =  [1.2, 3.95]
            vertices[35] =  [1.1, 3.92]
            vertices[36] =  [1, 3.88]
            vertices[37] =  [0.8, 3.72]
            vertices[38] =  [0.6, 3.4]
            vertices[39] =  [0.58, 3.3]
            vertices[40] =  [0.57, 3.2]
            vertices[41] =  [0.8, 2]
            vertices[42] =  [1, 1]
            vertices[43] =  [1.25, 0.7]

    def get_closest_waypoint(self):
        res = 0
        index = 0
        x = self.x
        y = self.y
        minDistance = float('inf')
        for row in self.waypoints:
            distance = math.sqrt((row[0] - x) * (row[0] - x) + (row[1] - y) * (row[1] - y))
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
        current_progress = math.sqrt((coor1[0] - coor2[0]) *(coor1[0] - coor2[0]) + (coor1[1] - coor2[1]) * (coor1[1] - coor2[1]))

        # convert to ratio and then percentage
        current_progress /= self.track_length
        current_progress *= 100.0

        return current_progress

    def calculate_track_length(self):
        track_length = 0.0
        prev_row = self.waypoints[0]
        for row in self.waypoints[1:]:
            track_length += math.sqrt((row[0] - prev_row[0]) * (row[0] - prev_row[0]) + (row[1] - prev_row[1]) * (row[1] - prev_row[1]))
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
        throttle = MAX_SPEED
        throttle_multiplier = 0.8
        throttle = throttle * throttle_multiplier
        steering_angle = 0.8

        self.throttle, self.steering_angle = self.two_steering_three_throttle_15_states(throttle, steering_angle, action)

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

    def two_steering_one_throttle_5_states(self,throttle_, steering_angle_, action):
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

    def two_steering_two_throttle_10_states(self,throttle_, steering_angle_, action):
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

    def two_steering_three_throttle_15_states(self,throttle_, steering_angle_, action):

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
