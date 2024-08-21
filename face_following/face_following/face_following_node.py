import numpy as np

import rclpy
from rclpy.node import Node
import vision_msgs.msg

from .servo_control import ServoControl


class FaceFollowingNode(Node):

    def __init__(self):
        super().__init__("face_following_node")

        # Parameters
        self.declare_parameter("timer_period", 0.1)
        self.timer_period = (
            self.get_parameter("timer_period").get_parameter_value().double_value
        )

        self.declare_parameter("image_w", 1280)
        self.image_w = self.get_parameter("image_w").get_parameter_value().integer_value

        self.declare_parameter("image_h", 720)
        self.image_h = self.get_parameter("image_h").get_parameter_value().integer_value

        self.declare_parameter("fov_w", 70)
        self.fov_w = self.get_parameter("fov_w").get_parameter_value().integer_value

        self.declare_parameter("fov_h", 50)
        self.fov_h = self.get_parameter("fov_h").get_parameter_value().integer_value

        self.declare_parameter("servo_pos_min", 0)
        servo_pos_min = (
            self.get_parameter("servo_pos_min").get_parameter_value().integer_value
        )
        self.declare_parameter("servo_pos_max", 180)
        servo_pos_max = (
            self.get_parameter("servo_pos_max").get_parameter_value().integer_value
        )

        self.declare_parameter("servo_speed_min", -100.0)
        servo_speed_min = (
            self.get_parameter("servo_speed_min").get_parameter_value().double_value
        )

        self.declare_parameter("servo_speed_max", 100.0)
        servo_speed_max = (
            self.get_parameter("servo_speed_max").get_parameter_value().double_value
        )

        self.declare_parameter("servo_pan_dir", 1)
        servo_pan_dir = (
            self.get_parameter("servo_pan_dir").get_parameter_value().integer_value
        )

        self.declare_parameter("servo_tilt_dir", 1)
        servo_tilt_dir = (
            self.get_parameter("servo_tilt_dir").get_parameter_value().integer_value
        )

        self.declare_parameter("servo_p_gain", 1.0)
        servo_p_gain = (
            self.get_parameter("servo_p_gain").get_parameter_value().double_value
        )

        # Subscriptions
        self.subscription = self.create_subscription(
            vision_msgs.msg.BoundingBox2D,
            "/face_bounding_box",
            self.bounding_box_callback,
            1,
        )

        # Timers
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        # Node variables
        self.center_x = round(self.image_w / 2)
        self.center_y = round(self.image_h / 2)

        self.target_x = self.center_x
        self.target_y = self.center_y

        # Servo config
        self.servo_pan = ServoControl(
            servo_pos_min,
            servo_pos_max,
            servo_speed_min,
            servo_speed_max,
            servo_pan_dir,
            servo_p_gain,
        )

        # self.servo_tilt = ServoControl(
        #     servo_pos_min,
        #     servo_pos_max,
        #     servo_speed_min,
        #     servo_speed_max,
        #     servo_tilt_dir,
        #     servo_p_gain,
        # )

    def bounding_box_callback(self, msg):

        self.target_x = msg.center.position.x
        self.target_y = msg.center.position.y

    def timer_callback(self):

        error_pan = self.center_x - self.target_x
        # error_tilt = self.center_y - self.target_y

        self.servo_pan.compute_control(error_pan, self.timer_period)
        # self.servo_tilt.compute_control(error_tilt, self.timer_period)


def main(args=None):
    rclpy.init(args=args)

    face_following_node = FaceFollowingNode()

    rclpy.spin(face_following_node)
    face_following_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
