from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

package_name = "elrik_bringup"


def launch_setup(context, *args, **kwargs):
    camera_enabled = LaunchConfiguration("camera_enabled")

    camera_model = "zedm"
    image_topic_left = "/zed/zed_node/left/image_rect_color/compressed"
    image_topic_right = "/zed/zed_node/right/image_rect_color/compressed"

    zed_camera_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare("zed_wrapper"), "/launch", "/zed_camera.launch.py"]
        ),
        launch_arguments={"camera_model": camera_model}.items(),
    )

    ik_control_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare(package_name), "/launch", "/ik_control.launch.py"]
        )
    )

    teleoperation_node = Node(
        package="teleoperation",
        executable="teleoperation_node",
        output="screen",
        remappings=[
            ("/image_left", image_topic_left),
            ("/image_right", image_topic_right),
        ],
        parameters=[
            {"camera_enabled": camera_enabled},
        ],
    )

    return [
        zed_camera_launch,
        ik_control_launch,
        teleoperation_node,
    ]


def generate_launch_description():

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "camera_enabled",
                default_value="true",
                description="Run teleoperation with ot without camera.",
                choices=["true", "false"],
            ),
            OpaqueFunction(function=launch_setup),
        ]
    )
