# IFRA-Cranfield: ur3_CranfieldRobotics

## UR3 Robot Simulation and Control using ROS 2: Practical Examples

### Gazebo Harmonic / GZ Sim

This environment does not have any particular use/application, but simply visualizing the UR3 robot and its end-effectors and stand in the simulation environment. Execute the following command to launch a Gazebo Harmonic / GZ Sim environment of the UR3-Cranfield Robot:

```sh
# UR3 Robot alone on Cranfield University (IA Lab) Stand:
ros2 launch ros2srrc_launch simulation.launch.py package:=ur3cranfield config:=ur3cranfield_1
# UR3 Robot + Robotiq HandE Gripper on Cranfield University (IA Lab) Stand: CubeTray Pick&Place use-case.
ros2 launch ros2srrc_launch simulation.launch.py package:=ur3cranfield config:=ur3cranfield_2
```

### Gazebo Harmonic / GZ Sim + MoveIt!2-based Robot Control

Execute the following command to launch the Gazebo Harmonic / GZ Sim environment along with the MoveIt!2 Framework, enabling the robot to be controlled, monitored, and operated through MoveIt!2. It also loads RViz for visualization and gives access to the custom ROS 2 tools (/Move, /Robmove, /Robpose) for robot manipulation and monitoring.

```sh
# UR3 Robot alone on Cranfield University (IA Lab) Stand:
ros2 launch ros2srrc_launch moveit2.launch.py package:=ur3cranfield config:=ur3cranfield_1
# UR3 Robot + Robotiq HandE Gripper on Cranfield University (IA Lab) Stand: CubeTray Pick&Place use-case.
ros2 launch ros2srrc_launch moveit2.launch.py package:=ur3cranfield config:=ur3cranfield_2
```

Once the environment has been launched, there are few operations that can be done to interact with the robot. For more information, please have a look at this [link](https://github.com/IFRA-Cranfield/ros2_SimRealRobotControl/blob/jazzy/instructions/RobotOperation.md).

- Robot movement:

    ```sh
    # MoveJ:
    ros2 action send_goal -f /Move ros2srrc_data/action/Move "{action: 'MoveJ', movej: {joint1: 0.00, joint2: 0.00, joint3: 0.00, joint4: 0.00, joint5: 0.00, joint6: 0.00}, speed: 1.0}"
    # MoveL:
    ros2 action send_goal -f /Move ros2srrc_data/action/Move "{action: 'MoveL', movel: {x: 0.00, y: 0.00, z: 0.00}, speed: 1.0}"
    # MoveR:
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
    ros2 topic echo /joint_states

    # To check the end-effector pose:
    ros2 topic echo /Robpose
    ```

- Execute a robot program: The programs for the UR3-Cranfield Robot are stored inside the ur3cranfield ROS 2 package, /programs folder. The following command is used to execute the programs (for more information, access this [link](https://github.com/IFRA-Cranfield/ros2_SimRealRobotControl/blob/jazzy/instructions/ProgramExecution.md)):

    ```sh
    # Example for the ur3_demo.yaml program:
    ros2 run ros2srrc_execution ExecuteProgram.py package:=ur3cranfield program:=ur3_demo
    ```

- Spawn objects into the GZ Sim environment: The CAD and SDF files of the objects that are manipulated in our UR3-Cranfield Robot's use-cases are stored in the ur3cranfield package. The objects can be spawned to the simulation environment using this command (more info [here](https://github.com/IFRA-Cranfield/ros2_SimRealRobotControl/blob/jazzy/instructions/RobotOperation.md#extra-spawn-object-to-a-gazebo-environment)):

    ```sh
    # Generic command:
    ros2 run ros2srrc_execution SpawnObject.py --package "{}" --sdf "{}.sdf" --name "{}" --x {} --y {} --z {}

    # Command to spawn the WHITE CUBE on top of the table:
    ros2 run ros2srrc_execution SpawnObject.py --package "ur3cranfield" --sdf "WhiteCube.sdf" --name "WhiteCube" --x 0.0 --y 0.3 --z 1.0
    ```

    Once the object has been spawned to the simulation environment, its pose can be checked with the following command (for more information, please visit [IFRA-Cranfield/IFRA_ObjectPose](https://github.com/IFRA-Cranfield/IFRA_ObjectPose/tree/jazzy)):
    ```sh
    ros2 topic echo /ObjectName/ObjectPose
    ros2 topic echo /WhiteCube/ObjectPose # For the white cube.
    ```

### MoveIt!2-based Control of the Real Robot

For more detailed instructions on how to properly set up any UR Robot for ROS 2 and to connect to the UR3 robot, please visit the ros2_SimRealRobotControl documentation. Once that is ready, you can execute the following command to launch the UR's ROS 2 driver along with MoveIt!2, and our custom ROS 2 tools for robot operation:

```sh
# In this setup, we consider:
#   - Ubuntu PC's IP Address is -> 192.168.1.2, manually set in the PC.
#   - UR3's IP Address is -> 192.168.1.10, manually set in the teach pendant.

# UR3 Robot alone on Cranfield University (IA Lab) Stand:
ros2 launch ros2srrc_launch bringup_ur.launch.py package:=ur3cranfield config:=ur3cranfield_1 robot_ip:=192.168.1.10
# UR3 Robot + Robotiq HandE Gripper on Cranfield University (IA Lab) Stand: CubeTray Pick&Place use-case.
ros2 launch ros2srrc_launch bringup_ur.launch.py package:=ur3cranfield config:=ur3cranfield_2 robot_ip:=192.168.1.10
```

Once the _robot bringup_ environment has been launched, the variety of tasks that can be done with the real robot are exactly the same as in simulation, with a few exceptions:

- Robot movements are exactly the same, but MoveG won't be available (this is only for Gazebo Harmonic / GZ Sim). In order to operate the Robotiq gripper in the real UR3 robot, IFRA-Cranfield's [ros2_RobotiqGripper](https://github.com/IFRA-Cranfield/ros2_RobotiqGripper) driver is used:

    ```sh
    # The ROS 2 server that operates the gripper is automatically launched within the bringup_ur.launch.py file.

    # To operate the gripper:
    ros2 service call /Robotiq_Gripper ros2_robotiqgripper/srv/RobotiqGripper "{action: 'CLOSE'}"
    ros2 service call /Robotiq_Gripper ros2_robotiqgripper/srv/RobotiqGripper "{action: 'OPEN'}"
    ```

- Robot state monitoring ROS 2 nodes are available as for simulation.

- Robot programs can be executed as for simulation:

    ```sh
    # Example for the ur3_demo.yaml program:
    ros2 run ros2srrc_execution ExecuteProgram.py package:=ur3cranfield program:=ur3_demo
    ```

- Object spawn feature is not available (this feature is only for Gazebo Harmonic / GZ Sim).

### Use-Case Application: Cube Pick and Place Task

__Gazebo Harmonic / GZ Sim environment__

```sh
# 1. Launch the Sim Environment for the P&P Task:
ros2 launch ros2srrc_launch moveit2.launch.py package:=ur3cranfield config:=ur3cranfield_2

# 2. Spawn the cube (WhiteCube, RedCube, GreenCube, BlackCube or BlueCube) on top of the UR3 Table:
ros2 run ros2srrc_execution SpawnObject.py --package "ur3cranfield" --sdf "WhiteCube.sdf" --name "WhiteCube" --x 0.257 --y 0.363 --z 0.92

# 3. Execute the Cube Pick&Place robot program:
ros2 run ros2srrc_execution ExecuteProgram.py package:=ur3cranfield program:=CubePP_ur3_sim
```

__Real UR3 Robot__

```sh
# 1. Launch the UR3 Robot's robot bringup ROS 2 Node, for the Cube P&P Task:
ros2 launch ros2srrc_launch bringup_ur.launch.py package:=ur3cranfield config:=ur3cranfield_2 robot_ip:=192.168.1.10

# 2. Place any cube inside the bottom-left slot of the left-tray on top of the UR3 Table.

# 3. Execute the Cube Pick&Place robot program:
ros2 run ros2srrc_execution ExecuteProgram.py package:=ur3cranfield program:=CubePP_ur3
```

### Object Pose Estimation using YOLO and OpenCV

The ur3cranfield_ope ROS 2 package performs real-time object pose estimation within the robot's workspace using a combination of YOLO and OpenCV.

- A trained YOLO model detects colored cubes placed in the workspace, providing their pixel coordinates from the camera feed.

- OpenCV techniques are then applied to convert these pixel coordinates into position coordinates relative to the camera. To align these coordinates with the robot's frame of reference, a camera-to-robot transformation is performed using an ArUco tag grid.

- Finally, the estimated object poses are live published to a dedicated ROS 2 topic, allowing seamless communication and integration with the robot's control system.

__Coloured Cube Pose Estimation: Gazebo Harmonic / GZ Sim__

Follow these steps to replicate the coloured cube pose estimation and pick & place task in simulation:

1. Launch the Gazebo Harmonic / GZ Sim environment + MoveIt!2 Framework for the task:

    ```sh
    ros2 launch ros2srrc_launch moveit2.launch.py package:=ur3cranfield config:=ur3cranfield_3
    ```

2. Run the Cube Pose Estimation ROS 2 node using the dedicated `ifra_ope` environment:

    ```sh
    source ~/venvs/ifra_ope/bin/activate
    python3 "$HOME/dev_ws/src/ur3_CranfieldRobotics/ur3cranfield_ope/python/PositionEstimation.py" environment:=gazebo model:=ColouredCubes_ur3 visualize:=true

    # This script has the following input parameters:
    #   - environment: gazebo/robot -> To select between the simulation or real camera.
    #   - model -> To select the trained YOLO model, located in ur3cranfield_ope/yolo/models folder.
    #   - visualize: True/False -> To show the YOLO prediction output in the screen.

    # Please note that, for the PositionEstimation node to work properly, the ArUco grid must be completely visible!
    # For the UR3-Cranfield robot, this is done by moving the robot to this JointPose:
    ros2 action send_goal -f /Move ros2srrc_data/action/Move "{action: 'MoveJ', movej: {joint1: 180.00, joint2: -90.00, joint3: 90.00, joint4: -90.00, joint5: -90.00, joint6: 0.00}, speed: 1.0}"
    ```

3. Spawn any cube to the robot workspace:

    ```sh
    ros2 run ros2srrc_execution SpawnObject.py --package "ur3cranfield" --sdf "BlueCube.sdf" --name "BlueCube" --x 0.0 --y 0.3 --z 1.0
    ros2 run ros2srrc_execution SpawnObject.py --package "ur3cranfield" --sdf "GreenCube.sdf" --name "GreenCube" --x 0.0 --y 0.3 --z 1.0
    ros2 run ros2srrc_execution SpawnObject.py --package "ur3cranfield" --sdf "RedCube.sdf" --name "RedCube" --x 0.0 --y 0.3 --z 1.0
    ros2 run ros2srrc_execution SpawnObject.py --package "ur3cranfield" --sdf "WhiteCube.sdf" --name "WhiteCube" --x 0.0 --y 0.3 --z 1.0

    # The ColouredCubes.pt detection models have been trained to detect blue, green, red and white cubes.
    # Feel free to manually move the cubes around in the simulation environment, the PositionEstimation node will detect them!

    # Once the cubes have been spawned, you will be able to monitor their estimated position using:
    ros2 topic list
    ros2 topic echo /BlueCube/ObjectPoseEstimation
    ros2 topic echo /GreenCube/ObjectPoseEstimation
    ros2 topic echo /RedCube/ObjectPoseEstimation
    ros2 topic echo /WhiteCube/ObjectPoseEstimation
    ```

4. Run the Cube Pick & Place program:

    ```sh
    # Execute the PositionEstimation.py script:
    ros2 run ur3cranfield_ope CubePP.py environment:=gazebo cube:=BlueCube

    # This script has the following input parameters:
    #   - environment: gazebo/robot -> To select between the simulation or real camera.
    #   - cube: RedCube/WhiteCube/GreenCube/BlueCube -> To select the cube to be picked.
    ```

__Coloured Cube Pose Estimation: UR3 Real Robot__

Follow these steps to replicate the coloured cube pose estimation and pick & place task in the real UR3 robot:

1. Launch the robot bringup environment + MoveIt!2 Framework for the task:

    ```sh
    ros2 launch ros2srrc_launch bringup_ur.launch.py package:=ur3cranfield config:=ur3cranfield_3 robot_ip:=192.168.1.10
    ```

2. Run the Cube Pose Estimation ROS 2 node using the dedicated `ifra_ope` environment:

    ```sh
    source ~/venvs/ifra_ope/bin/activate
    python3 "$HOME/dev_ws/src/ur3_CranfieldRobotics/ur3cranfield_ope/python/PositionEstimation.py" environment:=robot model:=ColouredCubes_ur3 visualize:=true

    # This script has the following input parameters:
    #   - environment: gazebo/robot -> To select between the simulation or real camera.
    #   - model -> To select the trained YOLO model, located in ur3cranfield_ope/yolo/models folder.
    #   - visualize: True/False -> To show the YOLO prediction output in the screen.

    # Please note that, for the PositionEstimation node to work properly, the ArUco grid must be completely visible!
    # For the UR3-Cranfield robot, this is done by moving the robot to this JointPose:
    ros2 action send_goal -f /Move ros2srrc_data/action/Move "{action: 'MoveJ', movej: {joint1: 180.00, joint2: -90.00, joint3: 90.00, joint4: -90.00, joint5: -90.00, joint6: 0.00}, speed: 1.0}"
    ```

3. Spawn any cube to the robot workspace:

    ```sh
    # Manually locate the coloured cubes on top of the robot workspace.

    # The ColouredCubes.pt detection models have been trained to detect blue, green, red and white cubes.
    # Feel free to manually move the cubes around in the robot workspace, the PositionEstimation node will detect them!

    # Once the cubes have been placed, you will be able to monitor their estimated position using:
    ros2 topic list
    ros2 topic echo /BlueCube/ObjectPoseEstimation
    ros2 topic echo /GreenCube/ObjectPoseEstimation
    ros2 topic echo /RedCube/ObjectPoseEstimation
    ros2 topic echo /WhiteCube/ObjectPoseEstimation
    ```

4. Run the Cube Pick & Place program:

    ```sh
    # Execute the PositionEstimation.py script:
    ros2 run ur3cranfield_ope CubePP.py environment:=robot cube:=BlueCube

    # This script has the following input parameters:
    #   - environment: gazebo/robot -> To select between the simulation or real camera.
    #   - cube: RedCube/WhiteCube/GreenCube/BlueCube -> To select the cube to be picked.
    ```
