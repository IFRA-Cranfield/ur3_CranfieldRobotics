# IFRA-Cranfield: ur3_CranfieldRobotics

## Installation Steps

The steps below must be followed in order to properly set up a ROS 2 Jazzy machine which is needed for the usage of the ROS 2 packages in the ur3_CranfieldRobotics repository. It is recommended to install Ubuntu 24.04 Desktop on your PC for optimal performance, but a VM could be used for simple simulations and executions.

__REQUIRED: Install the ros2_SimRealRobotControl GitHub repository__

The ROS 2 packages developed in UR3-CranfieldRobotics are based on IFRA-Cranfield's [ros2_SimRealRobotControl](https://github.com/IFRA-Cranfield/ros2_SimRealRobotControl/tree/jazzy) GitHub repository. Therefore, ros2_SimRealRobotControl must be installed in order to set up UR3-CR in any Ubuntu 24.04 + ROS 2 Jazzy machine.

Installation steps can be found at: https://github.com/IFRA-Cranfield/ros2_SimRealRobotControl/blob/jazzy/instructions/Installation.md

__Download and install ur3_CranfieldRobotics__

```sh
cd ~/dev_ws/src
git clone -b jazzy https://github.com/IFRA-Cranfield/ur3_CranfieldRobotics
cd ~/dev_ws
colcon build
```

__Install OpenCV and YOLO: Required for the Object Pose Estimation (ope) ROS 2 Package__

The object pose estimation nodes require a dedicated Python environment in Ubuntu 24.04 and ROS 2 Jazzy:

```sh
python3 -m venv ~/venvs/ifra_ope
source ~/venvs/ifra_ope/bin/activate

python3 -m pip install --upgrade pip
python3 -m pip install "numpy<2" "opencv-contrib-python==4.10.0.84" "ultralytics==8.4.137"
```

Important: do not use `ros2 run` for the perception node. Use the source script directly after activating the venv:

```sh
source /opt/ros/jazzy/setup.bash
source "$HOME/dev_ws/install/setup.bash"
source ~/venvs/ifra_ope/bin/activate

python3 "$HOME/dev_ws/src/ur3_CranfieldRobotics/ur3cranfield_ope/python/PositionEstimation.py" environment:=gazebo model:=ColouredCubes_ur3 visualize:=true
```

This is the supported workflow for the `ur3cranfield_ope` perception node in Ubuntu 24.04 + ROS 2 Jazzy.
