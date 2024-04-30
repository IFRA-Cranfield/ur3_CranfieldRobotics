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

# detect.py:

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

# GLOBAL VARIABLES:
Gz_CAM = None
ENVIRONMENT = ""
   
# =============================================================================== #
# CLASS -> ImgSUB:
class ImgSUB(Node):

    def __init__(self):

        super().__init__("ur3cranfield_GzCAM_Subscriber")
        self.SubIMAGE = self.create_subscription(Image, "/camera/image_raw", self.CALLBACK_FN, 10)
        self.BRIDGE = CvBridge()

    def CALLBACK_FN(self, ROS2img):

        global Gz_CAM

        try:
            Gz_CAM = self.BRIDGE.imgmsg_to_cv2(ROS2img, "bgr8")
        except CvBridgeError as ERR:
            print("(cv_bridge): ERROR -> " + ERR) 
            print("")
            
# =============================================================================== #
# CLASS -> CubeDetection:

class CubeDetection():

    def __init__(self, ENV):

        global ENVIRONMENT

        modelPATH = os.path.join(os.path.expanduser('~'), 'dev_ws', 'src', 'ur3_CranfieldRobotics', 'ur3cranfield_execution', 'yolov8')
        
        # Initialise CAMERA:
        if (ENV == "GAZEBO"):

            self.GzCAM_SUB = ImgSUB()
            self.InitCamGz()
            ENVIRONMENT = "GAZEBO"
            
            # YOLO MODEL:
            self.YOLOmodel = YOLO(modelPATH + '/cubeDETECTION_Gz.pt') # Pre-trained YOLOv8n model.

        else:

            self.InitCam()
            ENVIRONMENT = "ROBOT"

            # YOLO MODEL:
            self.YOLOmodel = YOLO(modelPATH + '/cubeDETECTION.pt') # Pre-trained YOLOv8n model.

        # Values of the CALIBRATION in x and y (mm):
        self.w = 750
        self.h = 400

    def InitCam(self):
        
        print("=== WEBCAM: Initialization ===")
        print("Loading WEB-CAMERA...")
        print("")
        
        # Initialise CAMERA:
        self.camera = cv2.VideoCapture(0)
        
        # Initialise RET(OpenCV variable) and inputImg(OpenCV MAT) values:
        T = time.time() + 1.0

        while time.time() < T:
            self.ret, self.inputImg = self.camera.read()

        if self.inputImg is None:
            print("Error! Input image is empty. Please check the camera and the VideoCapture(i) index.")
            rclpy.shutdown()
            print("CLOSING PROGRAM...")
            exit()
        
        if not self.ret:
            print("Error! Failed to capture input image. Please check the camera and the VideoCapture(i) index.")
            rclpy.shutdown()
            print("CLOSING PROGRAM...")
            exit()

    def InitCamGz(self):
        
        global Gz_CAM

        print("=== Gazebo CAM: Initialization ===")
        print("Loading GAZEBO CAMERA...")
        print("")

        # Initialise RET(OpenCV variable) and inputImg(OpenCV MAT) values:
        T = time.time() + 1.0

        while time.time() < T:
            # 1. SPIN /Image topic subscriber!
            rclpy.spin_once(self.GzCAM_SUB)
            # 2. ASSIGN + Show IMG:
            self.inputImg = Gz_CAM
        
        if self.inputImg is None:
            print("Error! Input image is empty. Please check that the Gz WEBCAM is publishing the IMG correctly.")
            rclpy.shutdown()
            print("CLOSING PROGRAM...")
            exit()
            
    def ConstantVisualization(self):

        global Gz_CAM
        global ENVIRONMENT

        while True:

            if (ENVIRONMENT == "GAZEBO"):
                # 1. SPIN /Image topic subscriber!
                rclpy.spin_once(self.GzCAM_SUB)
                # 2. ASSIGN IMG:
                self.inputImg = Gz_CAM

            else:
                # ASSIGN IMG:
                self.ret, self.inputImg = self.camera.read()


            # 3. Get -> YOLOv8 MODEL RESULT:
            if self.inputImg is not None:
                results = self.YOLOmodel(self.inputImg)
                annotated_frame = results[0].plot()
                VISUALIZE = cv2.resize(annotated_frame, (1280, 720))
                cv2.imshow("UR3 Cranfield Cell (CUBE DETECTION): YOLO Output", VISUALIZE)

            key = cv2.waitKey(1)
            if key == ord('e'):
                cv2.destroyWindow("UR3 Cranfield Cell (CUBE DETECTION): YOLO Output")
                break 

