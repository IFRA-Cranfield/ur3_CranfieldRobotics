# ur3cranfield_gazebo: Gazebo Simulation Package

<!--

HEADER IMAGE TO BE ADDED:

<br />
<div align="center">
  <a>
    <img src="../media/gazebo.png" alt="header" width="1000" height="800">
  </a>

  <br />
</div>
<br />

-->

<!-- INFORMATION -->
## ROS 2 Package Information

The Gazebo package provides essential resources for simulating and testing the behavior of the UR3 collaborative robot within the Gazebo environment:
- Config: This folder contains the parameters and specifications of the ROS 2 controllers that manage the UR3 Robot.
- Launch: This folder contains the .launch.py script that launches all the ROS 2 nodes required to execute the simulation.
- Meshes: CAD files (UR3 Robot, Robotiq Grippers, UR3-Stand, Cubes, Tray...).
- Urdf: Robot specifications, formatted on the URDF format (ROS 2 standard).
- Worlds: Gazebo .world file, containing information about the simulation environment.

<!-- Execution -->
## Execution

The Simulation Environment of the Cranfield Robotics UR3 Robot (visualization, without ROS 2 nodes for the control of the robot) can be executed with the following command:
```sh
# UR3 Robot + Robotiq HandE Gripper:
ros2 launch ur3cranfield_gazebo simulation_hande.launch.py

# UR3 Robot + Robotiq 2f-85 Gripper:
ros2 launch ur3cranfield_gazebo simulation_2f85.launch.py
```