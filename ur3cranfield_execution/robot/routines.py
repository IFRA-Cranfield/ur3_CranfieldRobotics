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

# routines.py
# Python script containing the routines(executions) of the ROBOT:

# ===== IMPORT REQUIRED COMPONENTS ===== #
# Extra required libraries:
import time, math
# Pose:
from geometry_msgs.msg import Pose

# ===== IMPORT FUNCTIONS ===== #
# Robot and Gripper classes:
from robot import RBT
from gripper_Gz import GzGripper
from gripper import RobotiqHandE

# ================================================================================= #
# Function to compute the Robot Pose (EE Vector in quaternions, getting the cube angle as the input):     
def EEQuaternion(yaw):

    RESULT = Pose()

    # 1. Initial pose:
    Ax = 1.0
    Ay = 0.0
    Az = 0.0
    Aw = 0.0

    # 2. Get desired RELATIVE ROTATION:
    pitch = 0.0
    roll = 0.0
    yaw = -yaw
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)
    Bx = sr * cp * cy - cr * sp * sy
    By = cr * sp * cy + sr * cp * sy
    Bz = cr * cp * sy - sr * sp * cy
    Bw = cr * cp * cy + sr * sp * sy

    # 3. Quaternion MULTIPLICATION:
    RESULT.orientation.x = Aw*Bx + Ax*Bw + Ay*Bz - Az*By
    RESULT.orientation.y = Aw*By - Ax*Bz + Ay*Bw + Az*Bx
    RESULT.orientation.z = Aw*Bz + Ax*By - Ay*Bx + Az*Bw
    RESULT.orientation.w = Aw*Bw - Ax*Bx - Ay*By - Az*Bz

    return(RESULT)

# ===================================================================================== #
# ======================================= MAIN ======================================== #
# ===================================================================================== #

class RoutineList():

    def __init__(self, ENVIRONMENT):
        
        # ROBOT:
        self.ROBOT = RBT()
        
        # GRIPPER:
        if (ENVIRONMENT == "GAZEBO"):
            self.GRIPPER = GzGripper()
        else: 
            self.GRIPPER = RobotiqHandE()   

    def HomePos_andOPEN(self):
        print("(Robot Movement -> /Move): HomePos")
        self.ROBOT.Move_EXECUTE("HomePos")
        time.sleep(0.2)
        self.GRIPPER.OPEN()
        time.sleep(0.2)
    
    def HomePos(self):
        print("(Robot Movement -> /Move): HomePos")
        self.ROBOT.Move_EXECUTE("HomePos")

    def InterPos(self):
        print("(Robot Movement -> /Move): InterPos")
        self.ROBOT.Move_EXECUTE("InterPos")

    def PrePlace(self):
        print("(Robot Movement -> /Move): PrePlace")
        self.ROBOT.Move_EXECUTE("PrePlace")

    def PickCube(self, x, y, yaw):

        print("===== ROUTINE EXECUTION =====")
        print(" - Picking cube from workspace...")
        print("")
        
        # Calculate EE ROTATION:
        EEPose = EEQuaternion(yaw)

        # Move to InterPos:
        self.InterPos()

        # Move to PickApproach:
        print("(Robot Movement -> /RobMove): PickCube_App")
        TARGET_POSE = Pose()
        TARGET_POSE.position.x = x
        TARGET_POSE.position.y = y
        TARGET_POSE.position.z = 1.08
        TARGET_POSE.orientation = EEPose.orientation
        self.ROBOT.RobMove_EXECUTE_cstm("PTP",1.0,TARGET_POSE)

        # Move to Pick:
        print("(Robot Movement -> /RobMove): PickCube")
        TARGET_POSE = Pose()
        TARGET_POSE.position.x = x
        TARGET_POSE.position.y = y
        TARGET_POSE.position.z = 1.02
        TARGET_POSE.orientation = EEPose.orientation
        self.ROBOT.RobMove_EXECUTE_cstm("LIN",0.1,TARGET_POSE)

        # CLOSE GRIPPER:
        time.sleep(0.2)
        self.GRIPPER.CLOSE()
        time.sleep(0.2)

        # Move to PickApproach:s
        print("(Robot Movement -> /RobMove): PickCube_App")
        TARGET_POSE = Pose()
        TARGET_POSE.position.x = x
        TARGET_POSE.position.y = y
        TARGET_POSE.position.z = 1.08
        TARGET_POSE.orientation = EEPose.orientation
        self.ROBOT.RobMove_EXECUTE_cstm("LIN",0.1,TARGET_POSE)

        # Move to InterPos:
        self.InterPos()

    def PlaceCube(self, CUBE):

        # Move to PrePlace:
        self.PrePlace()

        if CUBE == "WhiteCube":

            print("(Robot Movement -> /RobMove): PlaceWHITE_app")
            self.ROBOT.RobMove_EXECUTE("PlaceWHITE_app", "PTP", 1.0)

            print("(Robot Movement -> /RobMove): PlaceWHITE")
            self.ROBOT.RobMove_EXECUTE("PlaceWHITE", "LIN", 0.1)

            # OPEN GRIPPER:
            time.sleep(0.2)
            self.GRIPPER.OPEN()
            time.sleep(0.2)

            print("(Robot Movement -> /RobMove): PlaceWHITE_app")
            self.ROBOT.RobMove_EXECUTE("PlaceWHITE_app", "LIN", 0.1)
            

        elif CUBE == "BlackCube":

            print("(Robot Movement -> /RobMove): PlaceBLACK_app")
            self.ROBOT.RobMove_EXECUTE("PlaceBLACK_app", "PTP", 1.0)

            print("(Robot Movement -> /RobMove): PlaceBLACK")
            self.ROBOT.RobMove_EXECUTE("PlaceBLACK", "LIN", 0.1)

            # OPEN GRIPPER:
            time.sleep(0.2)
            self.GRIPPER.OPEN()
            time.sleep(0.2)

            print("(Robot Movement -> /RobMove): PlaceBLACK_app")
            self.ROBOT.RobMove_EXECUTE("PlaceBLACK_app", "LIN", 0.1)

        elif CUBE == "BlueCube":

            print("(Robot Movement -> /RobMove): PlaceBLUE_app")
            self.ROBOT.RobMove_EXECUTE("PlaceBLUE_app", "PTP", 1.0)

            print("(Robot Movement -> /RobMove): PlaceBLUE")
            self.ROBOT.RobMove_EXECUTE("PlaceBLUE", "LIN", 0.1)

            # OPEN GRIPPER:
            time.sleep(0.2)
            self.GRIPPER.OPEN()
            time.sleep(0.2)

            print("(Robot Movement -> /RobMove): PlaceBLUE_app")
            self.ROBOT.RobMove_EXECUTE("PlaceBLUE_app", "LIN", 0.1)

        elif CUBE == "Cube" or CUBE == "Sticker":
            
            print("(Robot Movement -> /RobMove): PlaceCUBE_app")
            self.ROBOT.RobMove_EXECUTE("PlaceCUBE_app", "PTP", 1.0)

            print("(Robot Movement -> /RobMove): PlaceCUBE")
            self.ROBOT.RobMove_EXECUTE("PlaceCUBE", "LIN", 0.1)

            # OPEN GRIPPER:
            time.sleep(0.2)
            self.GRIPPER.OPEN()
            time.sleep(0.2)

            print("(Robot Movement -> /RobMove): PlaceCUBE_app")
            self.ROBOT.RobMove_EXECUTE("PlaceCUBE_app", "LIN", 0.1)

        # Move to PrePlace:
        self.PrePlace()