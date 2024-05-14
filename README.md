<div id="top"></div>

<!-- 

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

-->

<!--

  README.md TEMPLATE obtined from:
      https://github.com/othneildrew/Best-README-Template
      AUTHOR: OTHNEIL DREW 

-->

<!-- HEADER -->
<br />
<div align="center">
  <a>
    <img src="media/header.jpg" alt="header" width="680" height="190">
  </a>

  <br />

  <h2 align="center">UR3 Robot ROS 2 Packages - Cranfield Robotics</h2>

  <h3 align="center">Universal Robots: UR3 Robot - ROS2 Humble</h3>

  <p align="center">
    IFRA (Intelligent Flexible Robotics and Assembly) Group
    <br />
    Centre for Robotics and Assembly
    <br />
    Cranfield University
  </p>
</div>

<br />
<br />

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about">About</a>
      <ul>
        <li><a href="#intelligent-flexible-robotics-and-assembly-group">IFRA Group</a></li>
        <li><a href="#ur3_cranfieldrobotics-repository">ur3_CranfieldRobotics Repository</a></li>
      </ul>
    </li>
    <li>
      <a href="#installation">Installation</a>
      <ul>
        <li><a href="#ros2-humble-setup">ROS2 Humble Setup</a></li>
        <li><a href="#yolov8-and-opencv">YOLOv8 and OpenCV</a></li>
        <li><a href="#ur3_cranfieldrobotics">ur3_CranfieldRobotics</a></li>
      </ul>
    </li>
    <li>
      <a href="#ros2-packages">ROS2 Packages</a>
      <ul>
        <li><a href="#ur3cranfield_gazebo">ur3cranfield_gazebo</a></li>
        <li><a href="#ur3cranfield_moveit2">ur3cranfield_moveit2</a></li>
        <li><a href="#ur3cranfield_bringup">ur3cranfield_bringup</a></li>
        <li><a href="#ur3cranfield_data">ur3cranfield_data</a></li>
        <li><a href="#ur3cranfield_execution">ur3cranfield_execution</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#cite-our-work">Cite our work</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<br />

<!-- ABOUT THE PROJECT -->
## About

### Intelligent Flexible Robotics and Assembly Group

The IFRA (Intelligent Flexible Robotics and Assembly) Group is part of the Centre for Robotics and Assembly at Cranfield University.

IFRA Group pushes technical boundaries. At IFRA we provide high tech automation & assembly solutions, and we support smart manufacturing with Smart Industry technologies and solutions. Flexible Manufacturing Systems (FMS) are a clear example. They can improve overall operations and throughput quality by adapting to real-time changes and situations, supporting and pushing the transition towards flexible, intelligent and responsive automation, which we continuously seek and support.

The IFRA Group undertakes innovative research to design, create and improve Intelligent, Responsive and Flexible automation & assembly solutions, and this series of GitHub repositories provide background information and resources of how these developments are supported.

__SOCIAL MEDIA__:

IFRA-Cranfield:
- YouTube: https://www.youtube.com/@IFRACranfield
- LinkedIn: https://www.linkedin.com/in/ifra-cranfield/

Centre for Robotics and Assembly:
- Instagram: https://www.instagram.com/cranfieldrobotics/
- Facebook: https://www.facebook.com/cranfieldrobotics/
- YouTube: https://www.youtube.com/@CranfieldRobotics
- LinkedIn: https://www.linkedin.com/company/cranfieldrobotics/
- Website: https://www.cranfield.ac.uk/centres/centre-for-robotics-and-assembly 

### ur3_CranfieldRobotics Repository

Welcome to the ur3_CranfieldRobotics repository! This repository contains a comprehensive solution for simulating and controlling the UR3 Robot using ROS 2 Humble. The ROS 2 packages provided here enable seamless execution in both simulated and real environments. Leveraging ROS 2 Humble on an Ubuntu 22.04 PC, this repository furnishes all necessary source code, ensuring compatibility and ease of deployment. 

__Robotiq Grippers__

Our ROS 2 packages for the UR3 Robot include comprehensive support for two popular Robotiq grippers: the Robotiq HandE gripper and the Robotiq 2f-85 gripper. These grippers are seamlessly integrated into our simulation and control packages, allowing users to easily attach and control them alongside the UR3 Robot. With dedicated drivers and accompanying documentation, users can efficiently configure and utilize the Robotiq grippers for a wide range of robotic applications, enhancing the versatility and capabilities of the UR3 system.

At IFRA-Cranfield, we have developed a simple ROS 2 Driver to control the Robotiq grippers through TCP-IP socket connection. For more information, please visit the [IFRA-Cranfield/ros2_robotiqgripper](https://github.com/IFRA-Cranfield/ros2_RobotiqGripper) repository.

__Use-Case: Cube Detection, Classification and Pick-and-Place Task__

In this repository, a combination of YOLOv8, OpenCV, and Robot Motion Control has been employed in ROS 2. This integration empowers the system with advanced object detection and recognition capabilities, allowing for efficient and reliable execution of perception-enabled object handling using a ROS 2-controlled UR3 robot.

The system, equipped with a standard web camera, adeptly detects the randomly spawned cube within the workspace and proceeds to classify it based on its distinct colored feature. The intricate task of manipulating the cube involves precise pose estimation, ensuring its placement within the designated tray and alignment with the corresponding slot, with the identified feature positioned upwards.

Explore the packages and get started with your UR3 Robot Simulation and Control today!

__Video Demonstration: Program Execution (Simulation + Real Robot)__

Video demonstration coming soon.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- INSTALLATION -->
## Installation

The installation and execution of the ur3_CranfieldRobotics ROS2 packages requires the previous installation and set-up of the following components:
- Ubuntu 22.04 machine with ROS2 Humble.
- ROS2 Packages for the Simulation and Control of Robots using Gazebo and MoveIt!2.
- YOLOv8 for the object detection feature.
- OpenCV for the Image Processing feature.

### ROS2 Humble Setup

The packages used to run the Simulation and Control of the UR3 Robot in ur3_CranfieldRobotics are based on the [IFRA-Cranfield/ros2_SimRealRobotControl](https://github.com/IFRA-Cranfield/ros2_SimRealRobotControl) repository. Therefore, it is recommended to follow the installation steps defined in that repository in order to properly set-up a ROS2 Humble machine for Robot Simulation and Control. To facilitate your work, those steps have been summarized and outlined in the INSTALLATION.md document [here](https://github.com/IFRA-Cranfield/ur3_CranfieldRobotics/blob/main/INSTALLATION.md).

### YOLOv8 and OpenCV

The latest version (v8) of [YOLO (You-Only-Look-Once)](https://github.com/ultralytics/ultralytics) can be installed using the following pip command, which installs YOLOv8 along with the requirements for a Python>=3.8 environment with PyTorch>=1.8:
```sh
pip install ultralytics
```

OpenCV-Python is needed for this repo, and it can be installed with the following command:
```sh
pip install opencv-contrib-python
```

### ur3_CranfieldRobotics

Once the ROS2 Humble environment has been properly set up, and all the required packages have been installed, the ROS2 Packages of the ur3_CranfieldRobotics repository can be installed by executing the following commands in the terminal:
```sh
cd ~/dev_ws/src
git clone https://github.com/IFRA-Cranfield/ur3_CranfieldRobotics.git
cd ~/dev_ws
colcon build
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROS 2 Packages: Explanation -->
## ROS2 Packages 

Within this repository, you'll find a comprehensive integration of ROS 2 Robot Simulation and Control packages, including Gazebo, MoveIt!2, and Robot Bringup packages, meticulously combined with a custom ROS 2 package housing the Robot/Gripper Control, YOLOv8 and OpenCV modules, aptly named the execution package. This amalgamation provides a robust foundation for executing the cube pick-and-place task seamlessly across both simulated and real environments. The ROS 2 Robot Simulation and Control packages facilitate simulation and control of the UR3 collaborative robot, while the custom execution package empowers the system with advanced robot motion control, object detection and recognition capabilities, essential for precise manipulation and pose estimation of the target cube. Explore these packages to delve into the intricacies of robotic perception and control, accelerating the development and deployment of robotic applications.

### ur3cranfield_gazebo

The Gazebo package within this repository is a pivotal component, encompassing crucial data related to the robot's representation in the Unified Robot Description Format (.urdf). Beyond merely describing the robot's physical structure, this package also houses essential parameters necessary for fine-tuning ROS 2 controllers, ensuring precise control over the UR3 robot's movements. Furthermore, it includes detailed CAD files offering insight into the robot's design, alongside pertinent information concerning the Gazebo environment. This comprehensive package serves as the cornerstone for simulating and accurately replicating the robot's behavior within the simulated environment, facilitating seamless development and testing of robotic applications.

You can access all the Gazebo ROS 2 Package source code [here](https://github.com/IFRA-Cranfield/ur3_CranfieldRobotics/tree/main/ur3cranfield_gazebo).

### ur3cranfield_moveit2

The MoveIt!2 package within this repository is essential for motion control of the UR3 collaborative robot. It serves as a foundational element for motion planning and execution, offering comprehensive information required by the MoveIt!2 tool. This package includes crucial data such as robot specifications, obtained from the Gazebo package, ensuring consistency and accuracy in robot representation. Moreover, it encapsulates controller parameters necessary for fine-tuning and optimizing the robot's movements, enhancing its precision and efficiency. Additionally, the package provides a seamless Motion Planning interface, empowering users to effortlessly generate and execute motion plans, thereby streamlining the development and deployment of complex robotic applications.

You can access all the MoveIt!2 ROS 2 Package source code [here](https://github.com/IFRA-Cranfield/ur3_CranfieldRobotics/tree/main/ur3cranfield_moveit2).

### ur3cranfield_bringup

The Robot Bringup package within this repository acts as the main link between the ROS 2 system and the real robot arm. It facilitates seamless integration of the robot arm control with ROS 2, requiring the presence of a robust ROS 2 driver. This driver operates concurrently within both the robot controller and ROS 2 environment, enabling comprehensive control over the robot's motion and state through various ROS 2 nodes. By establishing this vital connection, the Robot Bringup package enables seamless communication and coordination between the ROS 2 system and the real robot arm, laying the groundwork for efficient and reliable execution of robotic tasks in real-world environments.

You can access all the Robot Bringup ROS 2 Package source code [here](https://github.com/IFRA-Cranfield/ur3_CranfieldRobotics/tree/main/ur3cranfield_bringup).

### ur3cranfield_data

The ur3cranfield_data ROS 2 package serves as a foundational component within our robotics ecosystem, housing custom ROS 2 data structures pivotal for seamless data exchange across various modules. Specifically tailored to our needs, these data structures facilitate efficient communication between the UR3 Robot, YOLOv8 object detection system, and OpenCV modules.

You can access all the ur3cranfield_data ROS 2 Package source code [here](https://github.com/IFRA-Cranfield/ur3_CranfieldRobotics/tree/main/ur3cranfield_data).

### ur3cranfield_execution

The execution package within this repository encompasses essential functionalities crucial for effective robot/gripper motion control, cube detection, classification, pose estimation, and pick-and-place tasks. It incorporates the YOLOv8 module for robust cube detection and classification, enabling the system to accurately identify the target object within the workspace. Additionally, the package integrates the OpenCV module for precise 6DoF Pose Estimation of the cube, ensuring accurate placement and alignment during manipulation tasks. Furthermore, the robot and gripper modules housed within this package contain ROS 2 Action Clients responsible for communicating with MoveIt!2, facilitating seamless operation of the robot movements. Lastly, the package encompasses the entire program logic for the application, orchestrating the coordination and interaction of various modules for efficient cube detection, pose estimation, and pick-and-place tasks, thereby enhancing the overall functionality and performance of the system.

You can access all the UR3-Execution Package source code [here](https://github.com/IFRA-Cranfield/ur3_CranfieldRobotics/tree/main/ur3cranfield_execution).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. If you have a suggestion that would make this better, or you find a solution to any of the issues/improvements presented above, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks you very much!

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

<p>
  Intelligent Flexible Robotics and Assembly Group
  <br />
  Created on behalf of the IFRA Group at Cranfield University, United Kingdom
  <br />
  E-mail: IFRA@cranfield.ac.uk 
  <br />
  <br />
  Licensed under the Apache-2.0 License.
  <br />
  You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
  <br />
  <br />
  <a href="https://www.cranfield.ac.uk/">Cranfield University</a>
  <br />
  School of Aerospace, Transport and Manufacturing (SATM)
  <br />
    <a href="https://www.cranfield.ac.uk/centres/centre-for-robotics-and-assembly">Centre for Robotics and Assembly</a>
  <br />
  College Road, Cranfield
  <br />
  MK43 0AL, Bedfordshire, UK
  <br />
</p>

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CITE OUR WORK -->
## Cite our work

<p>
  You can cite our work with the following statement:
  <br />
  IFRA-Cranfield (2024). UR3 Cranfield Robotics Cell. URL: https://github.com/IFRA-Cranfield/ur3_CranfieldRobotics
</p>

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

<p>
  Mikel Bueno Viso - Research Assistant in Intelligent Automation at Cranfield University
  <br />
  E-mail: Mikel.Bueno-Viso@cranfield.ac.uk
  <br />
  LinkedIn: https://www.linkedin.com/in/mikel-bueno-viso/
  <br />
  Profile: https://www.cranfield.ac.uk/people/mikel-bueno-viso-32884399
  <br />
  <br />
  Jamie Rice - Intelligent Automation Lab, Robotics Engineering Technician at Cranfield University
  <br />
  E-mail: jamie.rice@cranfield.ac.uk 
  <br />
  LinkedIn: https://www.linkedin.com/in/jamie-rice-b379562a0/
  <br />
  <br />
  Daniel Oakley - Intelligent Automation Lab, Robotics Engineering Technician at Cranfield University
  <br />
  E-mail: daniel.oakley@cranfield.ac.uk 
  <br />
  LinkedIn: https://www.linkedin.com/in/daniel-oakley-074746198/
  <br />
  <br />
  James Fowler - Intelligent Automation Lab, Senior Technical Officer at Cranfield University
  <br />
  E-mail: j.fowler@cranfield.ac.uk 
  <br />
  LinkedIn: https://www.linkedin.com/in/james-fowler-engtech-mimeche-2923953b/
  <br />
  <br />
  Dr. Seemal Asif - Lecturer in Artificial Intelligence and Robotics at Cranfield University
  <br />
  E-mail: s.asif@cranfield.ac.uk
  <br />
  LinkedIn: https://www.linkedin.com/in/dr-seemal-asif-ceng-fhea-miet-9370515a/
  <br />
  Profile: https://www.cranfield.ac.uk/people/dr-seemal-asif-695915
  <br />
  <br />
  Professor Phil Webb - Professor of Aero-Structure Design and Assembly at Cranfield University
  <br />
  E-mail: p.f.webb@cranfield.ac.uk
  <br />
  LinkedIn: https://www.linkedin.com/in/phil-webb-64283223/
  <br />
  Profile: https://www.cranfield.ac.uk/people/professor-phil-webb-746415 
  <br />
</p>

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [README.md template - Othneil Drew](https://github.com/othneildrew/Best-README-Template).
* [ROS 2 Documentation - Humble](https://docs.ros.org/en/humble/index.html).
* [PicNik Robotics - MoveIt!2 Documentation](https://moveit.picknik.ai/humble/index.html).
* [Universal Robots - ROS /ROS 2 Support](https://www.universal-robots.com/developer/develop-with-ros/).
* [UR3 - ROS 2 Driver](https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver).
* [Robotiq - Control through TCP-IP Socket Connection](https://dof.robotiq.com/discussion/2420/control-robotiq-gripper-mounted-on-ur-robot-via-socket-communication-python)
* [YOLOv8 - GitHub Repository](https://github.com/ultralytics/ultralytics)
* [OpenCV - Computer Vision Library](https://opencv.org/)

<p align="right">(<a href="#top">back to top</a>)</p>