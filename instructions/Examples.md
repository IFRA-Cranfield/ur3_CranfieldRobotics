# IFRA-Cranfield: ur3_CranfieldRobotics

## UR3 Robot Simulation and Control using ROS 2: Practical Examples

### Gazebo Simulation

This environment does not have any particular use/application, but simply visualizing the UR3 robot and it's end-effectors and stand in the Simulation Environment. Execute the following command to launch a ROS 2-Gazebo Simulation Environment of the UR3-Cranfield Robot:

```sh
# UR3 Robot alone on Cranfield University (IA Lab) Stand:
ros2 launch ros2srrc_launch simulation.launch.py package:=ur3cranfield config:=ur3cranfield_1
# UR3 Robot + Robotiq HandE Gripper on Cranfield University (IA Lab) Stand: CubeTray Pick&Place use-case.
ros2 launch ros2srrc_launch simulation.launch.py package:=ur3cranfield config:=ur3cranfield_2
```

### Gazebo Simulation + MoveIt!2-based Robot Control

Execute the following command to launch the ROS 2-Gazebo Simulation Environment along with the MoveIt!2 Framework, enabling the robot to be controlled, monitored, and operated through MoveIt!2. It also loads RVIZ for visualization and gives access to the custom ROS 2 tools (/Move, /RobMove, /RobPose) for robot manipulation and monitoring.

```sh
# UR3 Robot alone on Cranfield University (IA Lab) Stand:
ros2 launch ros2srrc_launch moveit2.launch.py package:=ur3cranfield config:=ur3cranfield_1
# UR3 Robot + Robotiq HandE Gripper on Cranfield University (IA Lab) Stand: CubeTray Pick&Place use-case.
ros2 launch ros2srrc_launch moveit2.launch.py package:=ur3cranfield config:=ur3cranfield_2
```

Once the environment has been launched, there are few operations that can be done to interact with the robot. For more information, please have a look at this [link](https://github.com/IFRA-Cranfield/ros2_SimRealRobotControl/blob/humble/instructions/RobotOperation.md).

- Robot Movement: 

    ```sh
    # MoveJ:
    ros2 action send_goal -f /Move ros2srrc_data/action/Move "{action: 'MoveJ', movej: {joint1: 0.00, joint2: 0.00, joint3: 0.00, joint4: 0.00, joint5: 0.00, joint6: 0.00}, speed: 1.0}"
    # MoveL:
    ros2 action send_goal -f /Move ros2srrc_data/action/Move "{action: 'MoveL', movel: {x: 0.00, y: 0.00, z: 0.00}, speed: 1.0}"
    # MOveR:
    ros2 action send_goal -f /Move ros2srrc_data/action/Move "{action: 'MoveR', mover: {joint: '--', value: 0.00}, speed: 1.0}"
    # MoveROT:
    ros2 action send_goal -f /Move ros2srrc_data/action/Move "{action: 'MoveROT', moverot: {yaw: 0.00, pitch: 0.00, roll: 0.00}, speed: 1.0}"
    # MoveRP:
    ros2 action send_goal -f /Move ros2srrc_data/action/Move "{action: 'MoveRP', moverp: {x: 0.00, y: 0.00, z: 0.00, yaw: 0.00, pitch: 0.00, roll: 0.00}, speed: 1.0}"
    # MoveG (for the gripper):
    ros2 action send_goal -f /Move ros2srrc_data/action/Move "{action: 'MoveG', moveg: 0.0, speed: 1.0}"

    # RobMove:
    ros2 action send_goal -f /Robmove ros2srrc_data/action/Robmove "{type: '---', speed: 1.0, x: 0.0, y: 0.0, z: 0.0, qx: 0.0, qy: 0.0, qz: 0.0, qw: 0.0}"
    ```

- Monitor the state of the robot:

    ```sh
    # To check the state of the joints:
    ros2 run ros2srrc_execution RobotState.py
    ros 2 topic echo /joint_states

    # To check the end-effector pose:
    ros2 topic echo /Robpose
    ```

- Execute a Robot Program: The programs for the UR3-Cranfield Robot are stored inside the ur3cranfield_execution ROS 2 Package. The following command is used to execute the programs (for more information, access this [link](https://github.com/IFRA-Cranfield/ros2_SimRealRobotControl/blob/humble/instructions/ProgramExecution.md)):

    ```sh
    # Example for the ur3_demo.yaml program:
    ros2 run ros2srrc_execution ExecuteProgram.py package:=ur3cranfield_execution program:=ur3_demo
    ```

- Spawn objects into the GzSim Environment: The CAD and URDF files of the objects that are manipulated in our UR3-Cranfield Robot's use-cases are stored in the ur3cranfield_gazebo package. The objects can be spawned to the Simulation Environment using this command:

    ```sh
    # Generic command:
    ros2 launch ros2srrc_launch simulation.launch.py package:=ur3cranfield config:=ur3cranfield_1

    # Command to spawn the WHITE CUBE on top of the table:
    ros2 run ros2srrc_execution SpawnObject.py --package "ur3cranfield_gazebo" --urdf "WhiteCube.urdf" --name "WhiteCube" --x 0.0 --y 0.3 --z 1.0
    ```

    Once the object has been spawned to the simulation environment, its pose can be checked with the following command (for more information, please visit [IFRA-Cranfield/IFRA_ObjectPose](https://github.com/IFRA-Cranfield/IFRA_ObjectPose)):
    ```sh
    ros2 topic echo /ObjectName/ObjectPose
    ros2 topic echo /WhiteCube/ObjectPose # For the white cube.
    ```

### MoveIt!2-based Control of the Real Robot

TBD.

### Use-Case Applications: Cube Pick and Place Tasks

TBD.