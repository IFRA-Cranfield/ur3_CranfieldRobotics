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

# waypoints.py
# This function returns the Robot Movement TYPE (Pose: /RobMove - Action: /Move) and the movement parameters.

# ===== IMPORT REQUIRED COMPONENTS ===== #
# Import ROS2 messages:
from geometry_msgs.msg import Pose
from ros2srrc_data.msg import Action

# =============================================================================== #
# CLASS -> waypoints:

class waypoints():

    def __init__(self):

        self.RobotPoseDict = {}

        # ========== HOME ========== #
        self.RobotPoseDict["HomePos"] = Action()
        self.RobotPoseDict["HomePos"].action = "MoveJ"
        self.RobotPoseDict["HomePos"].speed = 1.0
        self.RobotPoseDict["HomePos"].movej.joint1 = 90.0
        self.RobotPoseDict["HomePos"].movej.joint2 = -135.0
        self.RobotPoseDict["HomePos"].movej.joint3 = 45.0
        self.RobotPoseDict["HomePos"].movej.joint4 = -90.0
        self.RobotPoseDict["HomePos"].movej.joint5 = -90.0
        self.RobotPoseDict["HomePos"].movej.joint6 = -90.0

        # ========== INTERMEDIATE ========== #
        self.RobotPoseDict["InterPos"] = Action()
        self.RobotPoseDict["InterPos"].action = "MoveJ"
        self.RobotPoseDict["InterPos"].speed = 1.0
        self.RobotPoseDict["InterPos"].movej.joint1 = 90.0
        self.RobotPoseDict["InterPos"].movej.joint2 = -90.0
        self.RobotPoseDict["InterPos"].movej.joint3 = 90.0
        self.RobotPoseDict["InterPos"].movej.joint4 = -90.0
        self.RobotPoseDict["InterPos"].movej.joint5 = -90.0
        self.RobotPoseDict["InterPos"].movej.joint6 = -90.0

        # ========== PRE-PLACING ========== #
        self.RobotPoseDict["PrePlace"] = Action()
        self.RobotPoseDict["PrePlace"].action = "MoveJ"
        self.RobotPoseDict["PrePlace"].speed = 1.0
        self.RobotPoseDict["PrePlace"].movej.joint1 = 0.0
        self.RobotPoseDict["PrePlace"].movej.joint2 = -90.0
        self.RobotPoseDict["PrePlace"].movej.joint3 = 90.0
        self.RobotPoseDict["PrePlace"].movej.joint4 = -90.0
        self.RobotPoseDict["PrePlace"].movej.joint5 = -90.0
        self.RobotPoseDict["PrePlace"].movej.joint6 = -90.0

        # ========== PLACE CUBE ========== #
        # Blue Cube:
        self.RobotPoseDict["PlaceBLUE_app"] = Pose()
        self.RobotPoseDict["PlaceBLUE_app"].position.x = 0.259 - 0.045
        self.RobotPoseDict["PlaceBLUE_app"].position.y = 0.0274
        self.RobotPoseDict["PlaceBLUE_app"].position.z = 1.03
        self.RobotPoseDict["PlaceBLUE_app"].orientation.x = 1.0
        self.RobotPoseDict["PlaceBLUE_app"].orientation.y = 0.0
        self.RobotPoseDict["PlaceBLUE_app"].orientation.z = 0.0
        self.RobotPoseDict["PlaceBLUE_app"].orientation.w = 0.0
        self.RobotPoseDict["PlaceBLUE"] = Pose()
        self.RobotPoseDict["PlaceBLUE"].position.x = 0.259 - 0.045
        self.RobotPoseDict["PlaceBLUE"].position.y = 0.0274
        self.RobotPoseDict["PlaceBLUE"].position.z = 1.00
        self.RobotPoseDict["PlaceBLUE"].orientation.x = 1.0
        self.RobotPoseDict["PlaceBLUE"].orientation.y = 0.0
        self.RobotPoseDict["PlaceBLUE"].orientation.z = 0.0
        self.RobotPoseDict["PlaceBLUE"].orientation.w = 0.0
        # Black Cube:
        self.RobotPoseDict["PlaceBLACK_app"] = Pose()
        self.RobotPoseDict["PlaceBLACK_app"].position.x = 0.259 - 0.045
        self.RobotPoseDict["PlaceBLACK_app"].position.y = 0.0274 - 0.045
        self.RobotPoseDict["PlaceBLACK_app"].position.z = 1.03
        self.RobotPoseDict["PlaceBLACK_app"].orientation.x = 1.0
        self.RobotPoseDict["PlaceBLACK_app"].orientation.y = 0.0
        self.RobotPoseDict["PlaceBLACK_app"].orientation.z = 0.0
        self.RobotPoseDict["PlaceBLACK_app"].orientation.w = 0.0
        self.RobotPoseDict["PlaceBLACK"] = Pose()
        self.RobotPoseDict["PlaceBLACK"].position.x = 0.259 - 0.045
        self.RobotPoseDict["PlaceBLACK"].position.y = 0.0274 - 0.045
        self.RobotPoseDict["PlaceBLACK"].position.z = 1.00
        self.RobotPoseDict["PlaceBLACK"].orientation.x = 1.0
        self.RobotPoseDict["PlaceBLACK"].orientation.y = 0.0
        self.RobotPoseDict["PlaceBLACK"].orientation.z = 0.0
        self.RobotPoseDict["PlaceBLACK"].orientation.w = 0.0
        # White Cube:
        self.RobotPoseDict["PlaceWHITE_app"] = Pose()
        self.RobotPoseDict["PlaceWHITE_app"].position.x = 0.259
        self.RobotPoseDict["PlaceWHITE_app"].position.y = 0.0274 - 0.045
        self.RobotPoseDict["PlaceWHITE_app"].position.z = 1.03
        self.RobotPoseDict["PlaceWHITE_app"].orientation.x = 1.0
        self.RobotPoseDict["PlaceWHITE_app"].orientation.y = 0.0
        self.RobotPoseDict["PlaceWHITE_app"].orientation.z = 0.0
        self.RobotPoseDict["PlaceWHITE_app"].orientation.w = 0.0
        self.RobotPoseDict["PlaceWHITE"] = Pose()
        self.RobotPoseDict["PlaceWHITE"].position.x = 0.259
        self.RobotPoseDict["PlaceWHITE"].position.y = 0.0274 - 0.045
        self.RobotPoseDict["PlaceWHITE"].position.z = 1.00
        self.RobotPoseDict["PlaceWHITE"].orientation.x = 1.0
        self.RobotPoseDict["PlaceWHITE"].orientation.y = 0.0
        self.RobotPoseDict["PlaceWHITE"].orientation.z = 0.0
        self.RobotPoseDict["PlaceWHITE"].orientation.w = 0.0
        # No-sticker Cube:
        self.RobotPoseDict["PlaceCUBE_app"] = Pose()
        self.RobotPoseDict["PlaceCUBE_app"].position.x = 0.259
        self.RobotPoseDict["PlaceCUBE_app"].position.y = 0.0274
        self.RobotPoseDict["PlaceCUBE_app"].position.z = 1.03
        self.RobotPoseDict["PlaceCUBE_app"].orientation.x = 1.0
        self.RobotPoseDict["PlaceCUBE_app"].orientation.y = 0.0
        self.RobotPoseDict["PlaceCUBE_app"].orientation.z = 0.0
        self.RobotPoseDict["PlaceCUBE_app"].orientation.w = 0.0
        self.RobotPoseDict["PlaceCUBE"] = Pose()
        self.RobotPoseDict["PlaceCUBE"].position.x = 0.259
        self.RobotPoseDict["PlaceCUBE"].position.y = 0.0274
        self.RobotPoseDict["PlaceCUBE"].position.z = 1.00
        self.RobotPoseDict["PlaceCUBE"].orientation.x = 1.0
        self.RobotPoseDict["PlaceCUBE"].orientation.y = 0.0
        self.RobotPoseDict["PlaceCUBE"].orientation.z = 0.0
        self.RobotPoseDict["PlaceCUBE"].orientation.w = 0.0

    def RobotPose(self, PoseName):

        result = self.RobotPoseDict[PoseName]
        return(result)          
            
