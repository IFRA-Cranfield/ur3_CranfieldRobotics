# ur3cranfield_bringup: Robot Bringup Package

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

The Robot Bringup package establishes seamless communication between the ROS 2 system and the real robot arm, enabling comprehensive control over its motion and state:
- Config: This folder contains the parameters and specifications of the ROS 2 controllers that manage the UR3 Robot and interface with the UR ROS 2 driver. 
- Launch: This folder contains the .launch.py script that launches all the ROS 2 nodes required to execute the ROS 2 - UR3 Robot connection + MoveIt!2 Control pipeline. In addition, it executes the custom /Move, /RobMove and /RobPose ROS 2 nodes required to manipulate the robot. For more information about these custom robot movements, please do visit the [ros2_SimRealRobotControl](https://github.com/IFRA-Cranfield/ros2_SimRealRobotControl/tree/humble/ros2srrc_execution) repository.

<!-- Execution -->
## Execution

The Robot Bringup + MoveIt!2 control pipeline of the Cranfield Robotics UR3 robot can be executed with the following command:
```sh
# UR3 Robot + Robotiq HandE Gripper:
ros2 launch ur3cranfield_bringup bringup_hande.launch.py ip_address:=0.0.0.0

# UR3 Robot + Robotiq 2f-85 Gripper:
ros2 launch ur3cranfield_bringup bringup_2f85.launch.py ip_address:=0.0.0.0 # GRIPPER CONTROL has not been tested for the 2f-85 gripper yet.
```

__NOTE__: Straight after launching the ROS 2 Node for the control of the UR3 Robot in ROS 2, __the external control script must be executed in the UR3's teach pendant__ to enable direct motion control of the UR3 though our ROS 2 Bringup package.