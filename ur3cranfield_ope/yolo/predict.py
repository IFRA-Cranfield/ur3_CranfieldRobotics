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
#  AUTHORS: Mikel Bueno Viso - Mikel.Bueno-Viso@cranfield.ac.uk                         #
#           Dr. Seemal Asif  - s.asif@cranfield.ac.uk                                   #
#           Prof. Phil Webb  - p.f.webb@cranfield.ac.uk                                 #
#                                                                                       #
#  Date: April, 2025.                                                                   #
#                                                                                       #
# ===================================== COPYRIGHT ===================================== #

# ======= CITE OUR WORK ======= #
# You can cite our work with the following statements:
# IFRA-Cranfield (2023) ROS 2 Sim-to-Real Robot Control. URL: https://github.com/IFRA-Cranfield/ros2_SimRealRobotControl.
# IFRA-Cranfield (2025) ROS 2 Sim-to-Real Robot Control. UR3 Robot. URL: https://github.com/IFRA-Cranfield/ur3_CranfieldRobotics.

# predict.py
# This script runs the YOLO-predict execution for a custom detection model.

# ===== IMPORT REQUIRED COMPONENTS ===== #
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
import os, sys

# Global Variable:
Gz_CAM = None

# ================================================== #
# CLASS -> GazeboCamera:
class GazeboCamera(Node):

    def __init__(self):

        super().__init__("ros2ope_GzCAM")
        self.SubIMAGE = self.create_subscription(Image, "/camera/image_raw", self.CALLBACK_FN, 10)
        self.BRIDGE = CvBridge()

    def CALLBACK_FN(self, ROS2img):

        global Gz_CAM

        try:
            Gz_CAM = self.BRIDGE.imgmsg_to_cv2(ROS2img, "bgr8")
        except CvBridgeError as ERR:
            print("(cv_bridge): ERROR -> " + ERR) 
            print("")

# ===== EVALUATE INPUT ARGUMENTS ===== #         
def AssignArgument(ARGUMENT):
    ARGUMENTS = sys.argv
    for y in ARGUMENTS:
        if (ARGUMENT + ":=") in y:
            ARG = y.replace((ARGUMENT + ":="),"")
            return(ARG)

# ===== TRAIN MODEL ===== #
def main(args=None):

    global Gz_CAM

    print("")
    print(" --- Cranfield University --- ")
    print("        (c) IFRA Group        ")
    print("")

    print("Object Detection and Pose Estimation in ROS 2.")
    print("Python script -> predict.py")
    print("")

    # Get ENVIRONMENT parameter value:
    ENVIRONMENT = AssignArgument("environment")
    if ENVIRONMENT == "gazebo" or ENVIRONMENT == "robot":
        print("Environment selected -> "+ ENVIRONMENT)
    else:
        print("")
        print("ERROR: environment INPUT ARGUMENT has not been properly defined (gazebo/robot). Please try again.")
        print("Closing... BYE!")
        exit()

    # Get MODELname parameter value:
    MODELname = AssignArgument("model")
    if MODELname != None:
        print("YOLO model selected -> "+ MODELname)
    else:
        print("")
        print("ERROR: model INPUT ARGUMENT has not been defined. Please try again.")
        print("Closing... BYE!")
        exit()
    
    print("")

    # Load custom MODEL:
    DIR = os.path.join(os.path.expanduser('~'), 'dev_ws', 'src', 'ur3_CranfieldRobotics', 'ur3_ope',  'yolo', 'models')
    modelPATH = DIR + "/" + MODELname + ".pt"

    if not os.path.exists(modelPATH):
        print("Selected YOLO model file not found. Please double check and try again.")
        print("Closing... BYE!")
        exit()
    
    # YOLOmodel:
    YOLOmodel = YOLO(modelPATH)

    # Initialise CAMERAS:
    if ENVIRONMENT == "gazebo":
        rclpy.init()
        CAMERA = GazeboCamera()
    elif ENVIRONMENT == "robot":
        CAMERA = cv2.VideoCapture(0)

    # Run execution-PREDICTION INFERENCE:
    while True:
        
        if ENVIRONMENT == "gazebo":
            rclpy.spin_once(CAMERA)
            inputIMG = Gz_CAM
        elif ENVIRONMENT == "robot":
            ret, inputIMG = CAMERA.read()

        if inputIMG is not None:
            
            PREDICTION = YOLOmodel(inputIMG)
            RESULTS = PREDICTION[0].plot()
            
            WINDOW = cv2.resize(RESULTS, (1280, 720))

            TITLE = "YOLO MODEL -> " + MODELname + " PREDICTION RESULTS"
            cv2.imshow(TITLE, WINDOW)

        key = cv2.waitKey(1)
        if key == ord('e'):
            cv2.destroyWindow(TITLE)
            break

    print("")
    print("YOLO model prediction successfully closed.")
    print("Closing... BYE!")

    if ENVIRONMENT == "gazebo":
        rclpy.shutdown()
    
    exit()

if __name__ == '__main__':
    main()