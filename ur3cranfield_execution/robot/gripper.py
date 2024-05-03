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

# robot.py
# This CLASSES execute Robot Movements, by calling the following ROS2 Actions:
#   - /Robmove allows the user to move the robot to a specific End-Effector pose. 
#   - /Move allows the user to execute a specific robot movement: Cartesian-Space, Joint-Space, Single Joint, Rotation... 

# gripper.py
# This function opens/closes the Robotiq HandE Gripper.

# ===== IMPORT REQUIRED COMPONENTS ===== #
# Required to include ROS2 and its components:
import rclpy
from rclpy.node import Node
# Import ROS2 Services:
from ros2_robotiqgripper.srv import RobotiqGripper

# =============================================================================== #
# Robotiq Gripper - ROS2 Service Client:

class ServiceClient(Node):

    def __init__(self):

        super().__init__('RobotiqHandE_client')

        print("(RobotiqHandE): Initialising ROS2 Service Client!")
        self.cli = self.create_client(RobotiqGripper, '/Robotiq_Gripper')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            print('(RobotiqHandE): Waiting for RobotiqHandE Service Server to be available...')

        print('(RobotiqHandE): RobotiqHandE Service Server detected.')
        self.req = RobotiqGripper.Request()

    def send_request(self, ACTION):
        self.req.action = ACTION
        self.future = self.cli.call_async(self.req)

    def OPEN_SRV(self):
        action = "OPEN"
        self.send_request(action)

    def CLOSE_SRV(self):
        action = "CLOSE"
        self.send_request(action)

# =============================================================================== #
# Robotiq Gripper CLASS:

class RobotiqHandE():

    def __init__(self):
        self.CLIENT = ServiceClient()

    def OPEN(self):

        self.CLIENT.OPEN_SRV()

        while rclpy.ok():
            rclpy.spin_once(self.CLIENT)

            if self.CLIENT.future.done():
                
                try:
                    OpenRES = self.CLIENT.future.result()

                except Exception as exc:
                    print("(RobotiqHandE): /Robotiq_Gripper Service call failed -> " + str(exc))
                    rclpy.shutdown()
                    print("CLOSING PROGRAM...")
                    exit()

                else:
                    if (OpenRES.success):
                        print("(RobotiqHandE): -> " + str(OpenRES.message))
                        return(True)
                    
                    else:
                        print("(RobotiqHandE): /Robotiq_Gripper Service call failed -> " + str(OpenRES.message))
                        rclpy.shutdown()
                        print("CLOSING PROGRAM...")
                        exit()

    def CLOSE(self):

        self.CLIENT.CLOSE_SRV()

        while rclpy.ok():
            rclpy.spin_once(self.CLIENT)

            if self.CLIENT.future.done():
                
                try:
                    CloseRES = self.CLIENT.future.result()

                except Exception as exc:
                    print("(RobotiqHandE): /Robotiq_Gripper Service call failed -> " + str(exc))
                    rclpy.shutdown()
                    print("CLOSING PROGRAM...")
                    exit()

                else:
                    if (CloseRES.success):
                        print("(RobotiqHandE): -> " + str(CloseRES.message))
                        return(True)
                    
                    else:
                        print("(RobotiqHandE): /Robotiq_Gripper Service call failed -> " + str(CloseRES.message))
                        rclpy.shutdown()
                        print("CLOSING PROGRAM...")
                        exit()