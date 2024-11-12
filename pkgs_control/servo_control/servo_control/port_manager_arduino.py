import serial

import rclpy
from rclpy.node import Node

from energirobotter_interfaces.msg import ServoCommand


class PortManagerArduino(Node):

    def __init__(self):
        super().__init__("port_manager_arduino")

        # Parameters
        self.declare_parameter("port", "/dev/ttyACM0")
        port = self.get_parameter("port").get_parameter_value().string_value

        self.declare_parameter("baudrate", 115200)
        baudrate = self.get_parameter("baudrate").get_parameter_value().integer_value

        self.declare_parameter("timeout", 115200)
        timeout = self.get_parameter("timeout").get_parameter_value().double_value

        # Subscriptions
        self.subscription = self.create_subscription(
            ServoCommand, "arduino/servo_command", self.callback_servo_command, 10
        )

        # Port Setup
        self.get_logger().info("Initializing serial communication...")
        try:
            self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
            self.get_logger().info("Serial communication succesful")
        except:
            self.get_logger().error(
                "Communication with Arduino unsuccesful, serial not available"
            )
            return

    def callback_servo_command(self, msg):
        # write packet to serial
        self.serial.write(bytes(str(int(msg.angle)), "utf-8"))
        self.serial.write(bytes("\n", "utf-8"))  # End character


def main(args=None):
    rclpy.init(args=args)

    port_manager_arduino = PortManagerArduino()

    rclpy.spin(port_manager_arduino)
    port_manager_arduino.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
