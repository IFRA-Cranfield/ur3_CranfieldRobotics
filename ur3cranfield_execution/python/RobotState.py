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

# RobotState.py:

# Generic ROS2 Python library:
import rclpy
from rclpy.node import Node

# For /joint_states:
from sensor_msgs.msg import JointState
k = 180.0/3.14159265359 

######################################################################################################

# Create NODE + SUBSCRIBER for /joint_states:
class CreateSubscriber(Node):
    
    def __init__(self):

        # Declare NODE:
        super().__init__("ros2ir_JointStates_SUB")

        # Declare SUBSCRIBER:
        self.subscription = self.create_subscription(
            JointState,                                                                                                           
            "joint_states",                                                            
            self.listener_callback,                                                   
            10)                                                             
        self.subscription # Prevent unused variable warning.

    def listener_callback(self, MSG):

        l = len(MSG.name)
        for j in range(l):

            if (MSG.name[j] == "shoulder_pan_joint" or MSG.name[j] == "joint_1"):
                J1 = MSG.position[j] * k
            if (MSG.name[j] == "shoulder_lift_joint" or MSG.name[j] == "joint_2"):
                J2 = MSG.position[j] * k
            if (MSG.name[j] == "elbow_joint" or MSG.name[j] == "joint_3"):
                J3 = MSG.position[j] * k
            if (MSG.name[j] == "wrist_1_joint" or MSG.name[j] == "joint_4"):
                J4 = MSG.position[j] * k
            if (MSG.name[j] == "wrist_2_joint" or MSG.name[j] == "joint_5"):
                J5 = MSG.position[j] * k
            if (MSG.name[j] == "wrist_3_joint" or MSG.name[j] == "joint_6"):
                J6 = MSG.position[j] * k
        
        RESULT = "JointValues are -> 'joint1': " + str(round(J1, 4)) + ", 'joint2': " + str(round(J2, 4)) + ", 'joint3': " + str(round(J3, 4)) + ", 'joint4': " + str(round(J4, 4)) + ", 'joint5': " + str(round(J5, 4)) + ", 'joint6': " + str(round(J6, 4))
        print(RESULT)

# ==================================================================================================================================== #
# ==================================================================================================================================== #
# =============================================================== MAIN =============================================================== #
# ==================================================================================================================================== #
# ==================================================================================================================================== #

def main(args=None):

    rclpy.init(args=args)

    print (" ========== UR3 Robot: Cranfield University Cell =========")
    print ("(c) Centre for Robotics and Assembly, Cranfield University")
    print ("")

    print("Python script -> RobotState.py")
    print("")
 
    JointValues_node = CreateSubscriber()
    rclpy.spin_once(JointValues_node)
    
    JointValues_node.destroy_node
    rclpy.shutdown()

if __name__ == "__main__":
    main()