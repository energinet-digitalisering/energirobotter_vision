import rclpy
from rclpy.node import Node

from .src.SCServo_Python.scservo_sdk import PortHandler, sms_sts, scservo_def

from energirobotter_interfaces.msg import ServoCommand


class PortManagerWaveshare(Node):

    def __init__(self):
        super().__init__("port_manager_waveshare")

        # Parameters
        self.declare_parameter("port", "/dev/ttyACM0")
        port = self.get_parameter("port").get_parameter_value().string_value

        self.declare_parameter("baudrate", 115200)
        baudrate = self.get_parameter("baudrate").get_parameter_value().integer_value

        # Subscriptions
        self.subscription = self.create_subscription(
            ServoCommand, "waveshare/servo_command", self.callback_servo_command, 10
        )

        # Port Setup
        self.port_handler = PortHandler(port)
        self.packet_handler = sms_sts(self.port_handler)

        if not self.port_handler.openPort():
            self.get_logger().error("Failed to open port")
            return
        if not self.port_handler.setBaudRate(baudrate):
            self.get_logger().error("Failed to set baud rate")
            return

    def callback_servo_command(self, msg):

        scs_comm_result, scs_error = self.packet_handler.WritePosEx(
            msg.servo_id, msg.pwm, SCS_MOVING_SPEED := 255, SCS_MOVING_ACC := 255
        )

        if scs_comm_result != scservo_def.COMM_SUCCESS:
            self.get_logger().error(
                f"Error in servo communication for servo id {msg.servo_id}: {scs_comm_result}"
            )

        # if scs_comm_result != scservo_def.COMM_SUCCESS:
        #     print("%s" % self.packet_handler.getTxRxResult(scs_comm_result))
        # elif scs_error != 0:
        #     print("%s" % self.packet_handler.getRxPacketError(scs_error))


def main(args=None):
    rclpy.init(args=args)

    port_manager_waveshare = PortManagerWaveshare()

    rclpy.spin(port_manager_waveshare)
    port_manager_waveshare.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
