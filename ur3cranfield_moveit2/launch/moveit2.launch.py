#!/usr/bin/python3

# ===================================== COPYRIGHT ===================================== #
#                                                                                       #
#  IFRA (Intelligent Flexible Robotics and Assembly) Group, CRANFIELD UNIVERSITY        #
#  Created on behalf of the IFRA Group at Cranfield University, United Kingdom          #
#  E-mail: IFRA@cranfield.ac.uk                                                         #
#                                                                                       #
#  Licensed under the Apache-2.0 License.                                               #
#  You may not use this file except in compliance with the License.                     #
#  You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0  #
#                                                                                       #
#  Unless required by applicable law or agreed to in writing, software distributed      #
#  under the License is distributed on an "as-is" basis, without warranties or          #
#  conditions of any kind, either express or implied. See the License for the specific  #
#  language governing permissions and limitations under the License.                    #
#                                                                                       #
#  IFRA Group - Cranfield University                                                    #
#  AUTHORS: Mikel Bueno Viso - Mikel.Bueno-Viso@cranfield.ac.uk     (ROS 2 Packages)    #
#           James Fowler     - j.fowler@cranfield.ac.uk             (UR3 Cell Design)   #
#           Daniel Oakley    - daniel.oakley@cranfield.ac.uk        (UR3 Cell Design)   #
#           Jamie Rice       - jamie.rice@cranfield.ac.uk           (UR3 Cell Design)   #
#                                                                                       #
#  Date: April, 2024.                                                                   #
#                                                                                       #
# ===================================== COPYRIGHT ===================================== #

# ======= CITE OUR WORK ======= #
# You can cite our work with the following statement:
# IFRA-Cranfield (2023) ROS 2 Sim-to-Real Robot Control. URL: https://github.com/IFRA-Cranfield/ros2_SimRealRobotControl.
# IFRA-Cranfield (2024) UR3 Cranfield Robotics Cell. URL: https://github.com/IFRA-Cranfield/ur3_CranfieldRobotics.

# moveit2.launch.py:
# Launch file for the UR3 Robot GAZEBO + MoveIt!2 SIMULATION (+ Robot/Gripper triggers) in ROS2 Humble:

# Import libraries:
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler, DeclareLaunchArgument, TimerAction
from launch.conditions import IfCondition, UnlessCondition
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
import xacro
import yaml

# LOAD FILE:
def load_file(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)
    try:
        with open(absolute_file_path, 'r') as file:
            return file.read()
    except EnvironmentError:
        # parent of IOError, OSError *and* WindowsError where available.
        return None
# LOAD YAML:
def load_yaml(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)
    try:
        with open(absolute_file_path, 'r') as file:
            return yaml.safe_load(file)
    except EnvironmentError:
        # parent of IOError, OSError *and* WindowsError where available.
        return None

# ========== **GENERATE LAUNCH DESCRIPTION** ========== #
def generate_launch_description():
    
    # ***** GAZEBO ***** #   
    # DECLARE Gazebo WORLD file:
    ur3cranfield_gazebo = os.path.join(
        get_package_share_directory('ur3cranfield_gazebo'),
        'worlds',
        'ur3.world')
    # DECLARE Gazebo LAUNCH file:
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
                launch_arguments={'world': ur3cranfield_gazebo}.items(),
             )


    # ========== COMMAND LINE ARGUMENTS ========== #
    print("")
    print("===== UR3 Robot: Cranfield Robotics =====")
    print("Robot configuration:")
    print("")
    # Cell Layout:
    print("- Cell layout: Cranfield University - IA Lab stand.")
    # End-Effector:
    print("- End-effector: Robotiq 2f-85 Parallel Gripper.")
    print("")

    # ***** ROBOT DESCRIPTION ***** #
    # UR3 Description file package:
    ur3_description_path = os.path.join(
        get_package_share_directory('ur3cranfield_gazebo'))
    # UR3 ROBOT urdf file path:
    xacro_file = os.path.join(ur3_description_path,
                              'urdf',
                              'ur3.urdf.xacro')
    # Generate ROBOT_DESCRIPTION for UR3:
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc, mappings={})
    robot_description_config = doc.toxml()
    robot_description = {'robot_description': robot_description_config}

    # SPAWN ROBOT TO GAZEBO:
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'ur3'],
                        output='both')
    
    # ***** STATIC TRANSFORM ***** #
    # Static TF:
    static_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_transform_publisher",
        output="log",
        arguments=["0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "world", "base_link"],
    )
    # Robot State Publisher:
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[
            robot_description,
            {"use_sim_time": True}
        ]
    )

    # ***** ROS2_CONTROL -> LOAD CONTROLLERS ***** #

    # Joint STATE BROADCASTER:
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )
    # Joint TRAJECTORY Controller:
    joint_trajectory_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["ur_controller", "-c", "/controller_manager"],
    )
    # === ROBOTIQ 2f-85 CONTROLLER === #
    robotiq_controller_spawner_LKJ = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["robotiq_controller_LKJ", "-c", "/controller_manager"],
    )
    robotiq_controller_spawner_RKJ = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["robotiq_controller_RKJ", "-c", "/controller_manager"],
    )
    robotiq_controller_spawner_LIKJ = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["robotiq_controller_LIKJ", "-c", "/controller_manager"],
    )
    robotiq_controller_spawner_RIKJ = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["robotiq_controller_RIKJ", "-c", "/controller_manager"],
    )
    robotiq_controller_spawner_LFTJ = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["robotiq_controller_LFTJ", "-c", "/controller_manager"],
    )
    robotiq_controller_spawner_RFTJ = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["robotiq_controller_RFTJ", "-c", "/controller_manager"],
    )


    # *********************** MoveIt!2 *********************** #   
    
    # Command-line argument: RVIZ file?
    rviz_arg = DeclareLaunchArgument(
        "rviz_file", default_value="False", description="Load RVIZ file."
    )

    # *** PLANNING CONTEXT *** #
    # Robot description, SRDF:
    robot_description_semantic_config = load_file("ur3cranfield_moveit2", "config/ur3robotiq.srdf")
    robot_description_semantic = {"robot_description_semantic": robot_description_semantic_config}

    # Kinematics.yaml file:
    kinematics_yaml = load_yaml("ur3cranfield_moveit2", "config/kinematics.yaml")
    robot_description_kinematics = {"robot_description_kinematics": kinematics_yaml}

    # joint_limits.yaml file:
    joint_limits_yaml = load_yaml("ur3cranfield_moveit2", "config/joint_limits.yaml")
    joint_limits = {'robot_description_planning': joint_limits_yaml}

    # pilz_planning_pipeline_config.yaml file:
    pilz_planning_pipeline_config = {
        "move_group": {
            "planning_plugin": "pilz_industrial_motion_planner/CommandPlanner",
            "request_adapters": """ """,
            "start_state_max_bounds_error": 0.1,
            "default_planner_config": "PTP",
        }
    }
    pilz_cartesian_limits_yaml = load_yaml("ur3cranfield_moveit2", "config/pilz_cartesian_limits.yaml")
    pilz_cartesian_limits = {'robot_description_planning': pilz_cartesian_limits_yaml}

    # MoveIt!2 Controllers:
    moveit_simple_controllers_yaml = load_yaml("ur3cranfield_moveit2", "config/urrobotiq_controllers.yaml")
    moveit_controllers = {
        "moveit_simple_controller_manager": moveit_simple_controllers_yaml,
        "moveit_controller_manager": "moveit_simple_controller_manager/MoveItSimpleControllerManager",
    }
    trajectory_execution = {
        "moveit_manage_controllers": True,
        "trajectory_execution.allowed_execution_duration_scaling": 1.2,
        "trajectory_execution.allowed_goal_duration_margin": 0.5,
        "trajectory_execution.allowed_start_tolerance": 0.01,
    }
    planning_scene_monitor_parameters = {
        "publish_planning_scene": True,
        "publish_geometry_updates": True,
        "publish_state_updates": True,
        "publish_transforms_updates": True,
    }
    move_group_capabilities = {
        "capabilities": """pilz_industrial_motion_planner/MoveGroupSequenceAction \
            pilz_industrial_motion_planner/MoveGroupSequenceService"""
    }

    # START NODE -> MOVE GROUP:
    run_move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            robot_description,
            robot_description_semantic,
            kinematics_yaml,
            
            pilz_planning_pipeline_config,

            joint_limits,
            pilz_cartesian_limits,

            trajectory_execution,
            moveit_controllers,
            planning_scene_monitor_parameters,
            move_group_capabilities,
            {"use_sim_time": True},
        ],
    )

    # RVIZ:
    load_RVIZfile = LaunchConfiguration("rviz_file")
    rviz_base = os.path.join(get_package_share_directory("ur3cranfield_moveit2"), "config")
    rviz_full_config = os.path.join(rviz_base, "ur3robotiq_moveit2.rviz")

    rviz_node_full = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_full_config],
        parameters=[
            robot_description,
            robot_description_semantic,
            kinematics_yaml,
            
            pilz_planning_pipeline_config,

            joint_limits,
            pilz_cartesian_limits,

            trajectory_execution,
            moveit_controllers,
            planning_scene_monitor_parameters,
            move_group_capabilities,
            {"use_sim_time": True},
        ],
        condition=UnlessCondition(load_RVIZfile),
    )

    MoveInterface = Node(
        name="move",
        package="ros2srrc_execution",
        executable="move",
        output="screen",
        parameters=[robot_description, robot_description_semantic, kinematics_yaml, {"use_sim_time": True}, {"ROB_PARAM": "ur3"}, {"EE_PARAM": "robotiq_2f85"}, {"ENV_PARAM": "gazebo"}],
    )
    RobMoveInterface = Node(
        name="robmove",
        package="ros2srrc_execution",
        executable="robmove",
        output="screen",
        parameters=[robot_description, robot_description_semantic, kinematics_yaml, {"use_sim_time": True}, {"ROB_PARAM": "ur3"}],
    )
    RobPoseInterface = Node(
        name="robpose",
        package="ros2srrc_execution",
        executable="robpose",
        output="screen",
        parameters=[robot_description, robot_description_semantic, kinematics_yaml, {"use_sim_time": True}, {"ROB_PARAM": "ur3"}],
    )
    SequenceInterface = Node(
        name="sequence",
        package="ros2srrc_execution",
        executable="sequence",
        output="screen",
        parameters=[robot_description, robot_description_semantic, kinematics_yaml, {"use_sim_time": True}, {"ROB_PARAM": "ur3"}, {"EE_PARAM": "robotiq_2f85"}, {"ENV_PARAM": "gazebo"}],
    )

    return LaunchDescription(
        [
            # Gazebo nodes:
            gazebo, 
            spawn_entity,
            # ROS2_CONTROL:
            static_tf,
            node_robot_state_publisher,
            
            # ROS2 Controllers:
            RegisterEventHandler(
                OnProcessExit(
                    target_action = spawn_entity,
                    on_exit = [
                        joint_state_broadcaster_spawner,
                    ]
                )
            ),
            RegisterEventHandler(
                OnProcessExit(
                    target_action = joint_state_broadcaster_spawner,
                    on_exit = [
                        joint_trajectory_controller_spawner,
                    ]
                )
            ),
            RegisterEventHandler(
                OnProcessExit(
                    target_action = joint_trajectory_controller_spawner,
                    on_exit = [
                        robotiq_controller_spawner_LKJ,
                        robotiq_controller_spawner_RKJ,
                        robotiq_controller_spawner_LIKJ,
                        robotiq_controller_spawner_RIKJ,
                        robotiq_controller_spawner_LFTJ,
                        robotiq_controller_spawner_RFTJ,
                    ]
                )
            ),

            RegisterEventHandler(
                OnProcessExit(
                    target_action = robotiq_controller_spawner_RFTJ,
                    on_exit = [

                        # MoveIt!2:
                        TimerAction(
                            period=2.0,
                            actions=[
                                rviz_arg,
                                rviz_node_full,
                                run_move_group_node
                            ]
                        ),

                        # ROS2.0 Actions:
                        TimerAction(
                            period=5.0,
                            actions=[
                                MoveInterface,
                                SequenceInterface,
                                RobMoveInterface,
                                RobPoseInterface,
                            ]
                        ),

                    ]
                )
            )
        ]
    )