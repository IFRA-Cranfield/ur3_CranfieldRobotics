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

# coordinates2Topic.py:

# ================================================================================= #
# Required to include ROS2 and its components:
import rclpy
from rclpy.node import Node
# CAMERA ROS2msg:
from sensor_msgs.msg import Image
# OpenCV:
import cv2
# ROS2 to OpenCV -> cv_bridge:
from cv_bridge import CvBridge, CvBridgeError
# YOLOv8:
from ultralytics import YOLO
# Extra:
import os, sys, time

# Detection CLASS:
from detection import CubeDetection

# ================================================================================= #
# Input arguments:
def AssignArgument(ARGUMENT):
    
    ARGUMENTS = sys.argv
    for y in ARGUMENTS:
        if (ARGUMENT + ":=") in y:
            ARG = y.replace((ARGUMENT + ":="),"")
            return(ARG)

# ================================================================================= #
# ===================================== MAIN ====================================== #
# ================================================================================= #

def main(args=None):

    print (" ========== UR3 Robot: Cranfield University Cell =========")
    print ("(c) Centre for Robotics and Assembly, Cranfield University")
    print ("")
    
    rclpy.init()
    
    # Get input argument -> ENVIRONMENT:
    ENV = AssignArgument("environment")
    if ENV == None:
        print("")
        print("ERROR: [environment] INPUT ARGUMENT has not been defined. Please try again.")
        print('COMMAND: ros2 run ur3cranfield_execution visualize.py environment:="", OPTIONS: "GAZEBO", "ROBOT".')
        print("Closing... BYE!")
        exit()
    elif ENV != "GAZEBO" and ENV != "ROBOT":
        print("")
        print("ERROR: [environment] INPUT ARGUMENT has not been properly defined. Please try again.")
        print('COMMAND: ros2 run ur3cranfield_execution visualize.py environment:="", OPTIONS: "GAZEBO", "ROBOT".')
        print("Closing... BYE!")
        exit()
    
    DETECTION = CubeDetection(ENV)
    
    while True:

        DETECTION.UpdateCamera(ENV)
        DETECTION.GetPerspectiveImg(ShowPerspective=False)
        RESULT = DETECTION.CubeLocation()

        if RESULT["success"]:
            DETECTION.PublishCoordinates(RESULT["detection"],RESULT["x"],RESULT["y"],RESULT["angle"])
        else:
            DETECTION.PublishCoordinates("NO DETECTION",0.0,0.0,0.0)

        # Show YOLO Output:
        output = cv2.resize(DETECTION.YOLOOutput, (750, 400))
        cv2.imshow("UR3 Cranfield Cell (CUBE DETECTION): YOLO Output", output)

        key = cv2.waitKey(1)
        if key == ord('q'):
            cv2.destroyWindow("UR3 Cranfield Cell (CUBE DETECTION): YOLO Output")
            break 

    rclpy.shutdown() 

    print("")
    print("")
    print("Closing program... BYE!")

if __name__ == '__main__':
    main()