import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node



def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='asitlorbot_three' #<--- CHANGE ME

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true', 'use_ros2_control':'true'}.items()
    )

    gazebo_params_file = os.path.join(get_package_share_directory(package_name),'config','gazebo_params.yaml')

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                    launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' +  gazebo_params_file}.items()
             )
    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_bot'],
                        output='screen')


    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    # # Add RTAB-Map node
    # rtabmap_node = Node(
    # package="rtabmap_ros",
    # executable="rtabmap",
    # output="screen",
    # parameters=[
    #     {"frame_id": "base_link"},
    #     {"database_path": os.path.join(get_package_share_directory(package_name), "path_to_database")},
    #     {"subscribe_depth": True},
    #     {"subscribe_stereo": False},
    #     {"approx_sync": False},
    #     {"rgbd_cameras": "camera/rgb/image_raw /camera/depth/image_raw"},  # Example camera topics
    #     {"odom_topic": "your_odom_topic"},  # Replace with your odometry topic
    #     {"delete_db_on_start": False},  # Change to True if you want to start with an empty database
    #     # Add more RTAB-Map parameters here as needed
    # ],
    # )



    # Launch them all!
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
        diff_drive_spawner,
        joint_broad_spawner
        # rtabmap_node
    ])