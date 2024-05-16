# ur3cranfield_execution: ROS 2 Package

<!--

HEADER IMAGE TO BE ADDED:

<br />
<div align="center">
  <a>
    <img src="../media/bringup.jpg" alt="header" width="800" height="600">
  </a>

  <br />
</div>
<br />

-->

<!-- INFORMATION -->
## ROS 2 Package Information

The ur3cranfield_execution ROS 2 package encompasses essential functionalities crucial for effective robot/gripper motion control, cube detection, classification, pose estimation, and pick-and-place tasks:
- Python: The "python" folder encompasses scripts tailored for various tasks within the robotic system. These include monitoring the real-time state of the robot, facilitating the dynamic spawning of objects within the Gazebo simulation environment, and orchestrating the execution of static programs using predefined robot movements encapsulated in the /Move and /RobMove actions. 
- Robot: The "robot" folder hosts the source code responsible for controlling the robot and gripper, facilitating seamless operation in both Gazebo simulation and real-world environments. Within this folder, Python classes are provided to interact with the robot and gripper, simplifying their operation through straightforward commands. These classes abstract the complexity of robot and gripper control, enabling users to easily command and manipulate them for various tasks. Whether in simulation or real-world scenarios, the functionalities provided in the "robot" folder streamline the process of operating the robot and gripper, enhancing the efficiency and ease of use of the robotic system.
- Programs: The "programs" folder houses text files (.txt) containing static sequences for program executions. These sequences represent predefined sets of actions or tasks to be executed in a specific order. The sequence.py script, located in the "python" folder, serves as the orchestrator for triggering these static program executions. By reading and interpreting the sequences stored in the text files, sequence.py coordinates the execution of tasks according to the specified order. 
- Detection: The "Detection" folder houses the source code responsible for executing cube detection and pose estimation tasks. At its core, the folder encapsulates algorithms and functionalities crucial for identifying and determining the position and orientation of cubes within the workspace. The cubePP.py script, situated within this folder, serves as the orchestrator for the entire use-case application execution. It coordinates the workflow, integrating the cube detection and pose estimation functionalities with other components such as robotic manipulation. 
- YOLOv8: This folder hosts the YOLOv8 model for the detection of the cubes within the robot's workspace.

## INSTRUCTIONS: Execute ROBOT MOVEMENTS

Robot movements can be executed in 2 different ways, which are defined in the ros2_SimRealRobotControl/ros2srrc_execution ROS2 Package:
- Using the /Move custom ROS2 action.
- Using the /Robmove custom ROS2 action.

### /Move ACTION

For /Move, the Robot Motion request consists of a simple ROS2 Action (/Move) call, where the following parameters must be specified:
- The ACTION that is going to be executed.
- The speed at which the robot will execute the action.
- The value of the action to be executed.

There are currently 9 different ACTION TYPES, which can be executed by running the following commands in the Ubuntu Terminal:

* MoveJ: The Robot moves to the specific waypoint, which is specified by Joint Pose values.
  ```sh
  ros2 action send_goal -f /Move ros2srrc_data/action/Move "{action: 'MoveJ', movej: {joint1: 0.00, joint2: 0.00, joint3: 0.00, joint4: 0.00, joint5: 0.00, joint6: 0.00}, speed: 1.0}"
  ```
* MoveG: The Gripper fingers move to the specific pose.
  ```sh
  ros2 action send_goal -f /Move ros2srrc_data/action/Move "{action: 'MoveG', moveg: 0.0, speed: 1.0}"
  ```
* MoveL: The Robot executes a CARTESIAN/LINEAR path. The End-Effector orientation is kept constant, and the position changes by +-(x,y,z).
  ```sh
  ros2 action send_goal -f /Move ros2srrc_data/action/Move "{action: 'MoveL', movel: {x: 0.00, y: 0.00, z: 0.00}, speed: 1.0}"
  ```
* MoveR: The Robot rotates the selected joint a specific amount of degrees.
  ```sh
  ros2 action send_goal -f /Move ros2srrc_data/action/Move "{action: 'MoveR', mover: {joint: '--', value: 0.00}, speed: 1.0}"
  ```
* MoveXYZW: The Robot moves to the specific waypoint, which is represented by the Position(x,y,z) + EulerAngles(yaw,pitch,roll) End-Effector coordinates.
  ```sh
  ros2 action send_goal -f /Move ros2srrc_data/action/Move "{action: 'MoveXYZW', movexyzw: {x: 0.00, y: 0.00, z: 0.00, yaw: 0.00, pitch: 0.00, roll: 0.00}, speed: 1.0}"
  ```
* MoveXYZ: The Robot moves to the specific waypoint -> Position(x,y,z) maintaining the End-Effector orientation.
  ```sh
  ros2 action send_goal -f /Move ros2srrc_data/action/Move "{action: 'MoveXYZ', movexyz: {x: 0.00, y: 0.00, z: 0.00}, speed: 1.0}"
  ```
* MoveYPR: The Robot rotates/orientates the End-Effector frame according to the input: EulerAngles(yaw,pitch,roll). The YPR(yaw,pitch,roll)determines the FINAL ROTATION of the End-Effector, which is related to the GLOBAL COORDINATE FRAME.
  ```sh
  ros2 action send_goal -f /Move ros2srrc_data/action/Move "{action: 'MoveYPR', moveypr: {yaw: 0.00, pitch: 0.00, roll: 0.00}, speed: 1.0}"
  ```
* MoveROT: The Robot rotates/orientates the End-Effector frame according to the input: EulerAngles(yaw,pitch,roll). THE ROT(yaw,pitch,roll) determines the ADDED ROTATION of the End-Effector, which is applied to the END-EFFECTOR COORDINATE FRAME.
  ```sh
  ros2 action send_goal -f /Move ros2srrc_data/action/Move "{action: 'MoveROT', moverot: {yaw: 0.00, pitch: 0.00, roll: 0.00}, speed: 1.0}"
  ```
* MoveRP: End-Effector rotation AROUND A POINT -> The Robot rotates/orientates + moves the End-Effector frame according to the input: EulerAngles(yaw,pitch,roll) + Point(x,y,z). THE ROT(yaw,pitch,roll) determines the ADDED ROTATION of the End-Effector, which is applied to the END-EFFECTOR COORDINATE FRAME, AROUND THE (x,y,z) POINT.
  ```sh
  ros2 action send_goal -f /Move ros2srrc_data/action/Move "{action: 'MoveRP', moverp: {x: 0.00, y: 0.00, z: 0.00, yaw: 0.00, pitch: 0.00, roll: 0.00}, speed: 1.0}"
  ```
* NOTE: The Robot JOINT SPEED is controlled by the "speed" parameter when executing the specific ROS2.0 action. The value must be (0,1]. being 1 the maximum velocity and 0 the null velocity (which is not valid -> A small value must be defined, e.g.: 0.01 represents a very slow movement).

### /Robmove ACTION

/Robmove allows the user to move the robot to a specific End-Effector pose (tool0 frame). It is executed after defining the parameters listed below:
- The TYPE of movement: It can be LINEAR ("LIN"), or Point-to-Point ("PTP").
- The speed at which the robot will execute the action.
- The POSE, (POSITION - x,y,z + ROTATION - qx,qy,qz,qw).

/Robmove can be executed by running the following command in the Ubuntu Terminal:
```sh
ros2 action send_goal -f /Robmove ros2srrc_data/action/Robmove "{type: '---', speed: 1.0, x: 0.0, y: 0.0, z: 0.0, qx: 0.0, qy: 0.0, qz: 0.0, qw: 0.0}"
```
It is recommended to combine /Robmove with /Robpose (ROS2 Topic, see below). This ROS2 topic publishes the current (real-time) pose of the Robot's end-effector, which helps the user to define the robot's next pose.

## INSTRUCTIONS: Execution of a PROGRAM/SEQUENCE

Programs can be executed by running the following command in the Ubuntu Terminal:
```sh
ros2 run ur3cranfield_execution sequence.py --ros-args -p PROGRAM_FILENAME:="---" -p ROBOT_MODEL:="ur3" -p EE_MODEL:="--" -p GzBr_ENV:="---"
```
* The PROGRAM_FILENAME parameter is the name of the file which contains the program. The program is saved in a .txt file, and the name must be inputted excluding the ".txt" extension.
* The ROBOT_MODEL parameter represents the model of the robot -> "ur3
* The EE_MODEL parameter represents the model of the end-effector -> "robotiq_hande" or "robotiq_2f85"
* The GzBr_ENV parameter defines whether the execution is being done in Gazebo or real robot. Options: "gazebo" or "bringup"

__Pre-defined sequence: Format__

The pre-defined programs are saved inside the /programs folder as .txt files. Every single line of the .txt file represents an execution step (being the 1st line: 1st step, 2nd line: 2nd step, ...), and it is represented as a python dictionary. The following list showcases how every single Robot Movement has to be inputted in the program.txt:
* For MoveJ ---> {'action': 'MoveJ', 'value': {'joint1': 0.0, 'joint2': 0.0, 'joint3': 0.0, 'joint4': 0.0, 'joint5': 0.0, 'joint6': 0.0}, 'speed': 1.0}
* For MoveL ---> {'action': 'MoveL', 'value': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'speed': 1.0}
* For MoveR ---> {'action': 'MoveR', 'value': {'joint': '---', 'value': 0.0}, 'speed': 1.0}
* For MoveXYZW ---> {'action': 'MoveXYZW', 'value': {'x': 0.0, 'y': 0.0, 'z': 0.0, 'yaw': 0.0, 'pitch': 0.0, 'roll': 0.0}, 'speed': 1.0}
* For MoveXYZ ---> {'action': 'MoveXYZ', 'value': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'speed': 1.0}
* For MoveYPR ---> {'action': 'MoveYPR', 'value': {'yaw': 0.0, 'pitch': 0.0, 'roll': 0.0}, 'speed': 1.0}
* For MoveROT ---> {'action': 'MoveROT', 'value': {'yaw': 0.0, 'pitch': 0.0, 'roll': 0.0}, 'speed': 1.0}
* For MoveRP ---> {'action': 'MoveRP', 'value': {'yaw': 0.0, 'pitch': 0.0, 'roll': 0.0, 'x': 0.0, 'y': 0.0, 'z': 0.0}, 'speed': 1.0}
* For MoveG (Gazebo) ---> {'action': 'MoveG', 'value': {'value': 0.0}, 'speed': 1.0}
* For MoveG (UR3 Robot): 
    * To Open Gripper ---> {'action': 'UR HandE - GripperOpen'}
    * To Close Gripper ---> {'action': 'UR HandE - GripperClose'}
* For the object manipulation (IFRA_LinkAttacher Gazebo Plugin):
    * To attach object to end-effector ---> {'action': 'Attach', 'value': {'model1': '---', 'link1': '---', 'model2': '---', 'link2': '---'}}
    * To detach object from end-effector ---> {'action': 'Attach', 'value': {'model1': '---', 'link1': '---', 'model2': '---', 'link2': '---'}}
    * Elements are defined as follows:
      * model1 -> Name of the model/robot (defined in the robot .urdf). 
      * link1 -> Name of the end-effector link that the object will be attached to.
      * model2 -> Name of the object to be attached (defined in the object .urdf). 
      * link2 -> Name of the object link.

## Obtaining ROBOT INFORMATION

The __RobotState.py__ script allows the user to get the state of the robot in __joint values__, by simply executing the following command:
```sh
ros2 run ros2ir_execution RobotState.py
# The script returns the robot's JointState values in the standard format presented above, in the sequence definition:
# {'joint1': 0.0, 'joint2': 0.0, 'joint3': 0.0, 'joint4': 0.0, 'joint5': 0.0, 'joint6': 0.0}
```

The __robpose.cpp__ script allows the user to get the pose of the robot's end-effector (tool0 flange) in __(POS + ROT)__, by simply subscribing to the /Robpose ROS2 topic:
```sh
ros2 topic echo /Robpose
```

## Spawn any object (CAD file) into the Simulation Environment

The __SpawnObject.py__ script allows the user to spawn any object (defined in a .__urdf__ file) to a Gazebo simulation, by simply executing the following command:
```sh
ros2 run ur3cranfield_execution SpawnObject.py --package "{}" --urdf "{}.urdf" --name "{}" --x {} --y {} --z {}
# NOTE: It is assumed that the .urdf file of the object to be spawned is stored in the /urdf folder of the selected package.
```

## Execute -> Static Program: UR3 Demo (simple robot movements)

In Gazebo Simulation environment:
```sh
# 1. Launch the Gazebo+MoveIt!2 Simulation Environment:
ros2 launch ur3cranfield_moveit2 moveit2_hande.launch.py

# 2. Execute sequence:
ros2 run ur3cranfield_execution sequence.py --ros-args -p PROGRAM_FILENAME:="ur3_demo" -p ROBOT_MODEL:="ur3" -p EE_MODEL:="robotiq_hande" -p GzBr_ENV:="gazebo"
```

For the Real UR3 Robot:
```sh
# 1. Launch the ROS 2-UR3 Bringup Environment:
ros2 launch ur3cranfield_bringup bringup_hande.launch.py ip_address:=0.0.0.0

# 2. Execute sequence:
ros2 run ur3cranfield_execution sequence.py --ros-args -p PROGRAM_FILENAME:="ur3_demo" -p ROBOT_MODEL:="ur3" -p EE_MODEL:="robotiq_hande" -p GzBr_ENV:="bringup"
```

## Execute -> Static Program: Pick-and-Place of 4 cubes (UR3 + RobotiQ HandE)

In Gazebo Simulation environment:
```sh
# 1. Launch the Gazebo+MoveIt!2 Simulation Environment:
ros2 launch ur3cranfield_moveit2 moveit2_hande.launch.py

# 2. Spawn 4 different boxes into the cell:
ros2 run ur3cranfield_execution SpawnObject.py --package "ur3cranfield_gazebo" --urdf "BlackCube.urdf" --name "BlackCube" --x -0.255 --y 0.12 --z 0.9 
ros2 run ur3cranfield_execution SpawnObject.py --package "ur3cranfield_gazebo" --urdf "BlueCube.urdf" --name "BlueCube" --x -0.255 --y 0.36 --z 0.9 
ros2 run ur3cranfield_execution SpawnObject.py --package "ur3cranfield_gazebo" --urdf "WhiteCube.urdf" --name "WhiteCube" --x 0.255 --y 0.12 --z 0.9 
ros2 run ur3cranfield_execution SpawnObject.py --package "ur3cranfield_gazebo" --urdf "Cube.urdf" --name "Cube" --x 0.255 --y 0.36 --z 0.9

# 3. Execute sequence:
ros2 run ur3cranfield_execution sequence.py --ros-args -p PROGRAM_FILENAME:="cubePP_handE" -p ROBOT_MODEL:="ur3" -p EE_MODEL:="robotiq_hande" -p GzBr_ENV:="gazebo"
```

For the Real UR3 Robot:
```sh
# 1. Launch the ROS 2-UR3 Bringup Environment:
ros2 launch ur3cranfield_bringup bringup_hande.launch.py ip_address:=0.0.0.0

# 2. Execute sequence:
ros2 run ur3cranfield_execution sequence.py --ros-args -p PROGRAM_FILENAME:="cubePP_handE_ROB" -p ROBOT_MODEL:="ur3" -p EE_MODEL:="robotiq_hande" -p GzBr_ENV:="bringup"
```

## Execute -> Detection, Classification, Pose Estimaton and Cube Pick-and-Place (UR3 + RobotiQ HandE)

SIMULATION:
```sh
# 1. Launch the Gazebo+MoveIt!2 Simulation Environment:
ros2 launch ur3cranfield_moveit2 moveit2_hande.launch.py

# 2. Spawn any of the cubes into the cell (only 1 at a time):
# (x,y) -> -0.15 < x < 0.15, 0.20 < y < 0.30 ; z = 0.90
ros2 run ur3cranfield_execution SpawnObject.py --package "ur3cranfield_gazebo" --urdf "BlackCube.urdf" --name "BlackCube" --x 0.0 --y 0.2 --z 0.9 
ros2 run ur3cranfield_execution SpawnObject.py --package "ur3cranfield_gazebo" --urdf "BlueCube.urdf" --name "BlueCube" --x 0.0 --y 0.2 --z 0.9 
ros2 run ur3cranfield_execution SpawnObject.py --package "ur3cranfield_gazebo" --urdf "WhiteCube.urdf" --name "WhiteCube" --x 0.0 --y 0.2 --z 0.9
ros2 run ur3cranfield_execution SpawnObject.py --package "ur3cranfield_gazebo" --urdf "Cube.urdf" --name "Cube" --x 0.0 --y 0.15 --z 0.9

# 3. Move the Robot to HomePosition:
ros2 action send_goal -f /Move ros2srrc_data/action/Move "{action: 'MoveJ', movej: {joint1: 90.00, joint2: -135.00, joint3: 45.00, joint4: -90.00, joint5: -90.00, joint6: 0.00}, speed: 1.0}"

# 4. Visualize YOLOv8 detection model output:
ros2 run ur3cranfield_execution visualize.py environment:=GAZEBO img:=CAMERA # For direct camera output.
ros2 run ur3cranfield_execution visualize.py environment:=GAZEBO img:=PERSPECTIVE # For improved (calibrated) camera output.
# NOTE: Press "E" on keyboard to exit after execution.

# 5. Calculate the Cube Coordinates after detection:
ros2 run ur3cranfield_execution coordinates.py environment:=GAZEBO
# NOTE: Press "Q" on keyboard once you see the transformed image to continue with the execution and get the COORDINATE values.

# 6.1 Launch an infinite loop that PUBLISHES THE OBJECT COORDINATES to a ROS 2 Topic:
ros2 run ur3cranfield_execution coordinates2Topic.py environment:=GAZEBO
# 6.2 SUBSCRIBE to the ROS 2 Topic to GET the value of the OBJECT COORDINATES:
ros2 topic list # To check the ROS 2 Topics available.
ros2 topic echo /CubeCoordinates # To access the CUBE COORDINATE VALUES.

# 7. CUBE PICK-AND-PLACE APPLICATION:
ros2 run ur3cranfield_execution cubePP.py environment:=GAZEBO
# NOTE: Press "Q" on keyboard once you see the transformed image to continue with the execution and get the COORDINATE values.

# NOTE: To delete a cube from the workspace in Gazebo, simply double click on it and click "delete", or select it and press the "Delete" button in your keyboard.
```

REAL UR3 Robot:
```sh
# 1. Launch the ROS 2-UR3 Bringup Environment:
ros2 launch ur3cranfield_bringup bringup_hande.launch.py ip_address:=0.0.0.0

# 2. Locate any of the cubes (with the colored feature facing upwards) within the workspace.

# 3. Move the Robot to HomePosition:
ros2 action send_goal -f /Move ros2srrc_data/action/Move "{action: 'MoveJ', movej: {joint1: 90.00, joint2: -135.00, joint3: 45.00, joint4: -90.00, joint5: -90.00, joint6: 0.00}, speed: 1.0}"

# 4. Visualize YOLOv8 detection model output:
ros2 run ur3cranfield_execution visualize.py environment:=ROBOT img:=CAMERA # For direct camera output.
ros2 run ur3cranfield_execution visualize.py environment:=ROBOT img:=PERSPECTIVE # For improved (calibrated) camera output.
# NOTE: Press "E" on keyboard to exit after execution.

# 5. Calculate the Cube Coordinates after detection:
ros2 run ur3cranfield_execution coordinates.py environment:=ROBOT
# NOTE: Press "Q" on keyboard once you see the transformed image to continue with the execution and get the COORDINATE values.

# 6.1 Launch an infinite loop that PUBLISHES THE OBJECT COORDINATES to a ROS 2 Topic:
ros2 run ur3cranfield_execution coordinates2Topic.py environment:=ROBOT
# 6.2 SUBSCRIBE to the ROS 2 Topic to GET the value of the OBJECT COORDINATES:
ros2 topic list # To check the ROS 2 Topics available.
ros2 topic echo /CubeCoordinates # To access the CUBE COORDINATE VALUES.

# 7. CUBE PICK-AND-PLACE APPLICATION:
ros2 run ur3cranfield_execution cubePP.py environment:=ROBOT
# NOTE: Press "Q" on keyboard once you see the transformed image to continue with the execution and get the COORDINATE values.
```