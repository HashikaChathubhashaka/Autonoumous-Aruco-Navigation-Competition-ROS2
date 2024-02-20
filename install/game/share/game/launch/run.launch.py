from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    aruco_detection_node = Node( #To run aruco marks detection node
        package="game",
        executable="aruco_detection",
        name="aruco_detection"
    )

    movements_node = Node( #To run movement of the robot node
        package="game",
        executable="movements",
        name= "movements"
    )


    return LaunchDescription([
        aruco_detection_node,
        movements_node
    ])
