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
# COORDINATES ROS2msg:
from ur3cranfield_data.msg import Coordinates
# OpenCV:
import cv2
from cv2 import aruco
import numpy as np
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

# ========================================================================================= #
# PUBLISHER (COORDINATES):
class CoordinatePublisher(Node):
    def __init__(self):
        super().__init__("ur3cranfield_CoordinatePublisher")
        self.publisher_ = self.create_publisher(Coordinates, "CubeCoordinates", 10)
            
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
        self.w = 569
        self.h = 299

        # Coordinates PUBLISHER:
        self.PUB = CoordinatePublisher()

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

    def UpdateCamera(self, ENV):

        if (ENV == "GAZEBO"):
            rclpy.spin_once(self.GzCAM_SUB)
            self.inputImg = Gz_CAM
        else:
            self.ret, self.inputImg = self.camera.read()


    def GetPerspectiveImg(self, ShowPerspective):

        if ShowPerspective:
            print("=== DETECTION: Calibration ===")
            print("Transforming the InputIMG into PerspectiveIMG using the ARUCO Tags...")
            print("")

        # Detection of the Aruco Markers in the input image:
        param = cv2.aruco.DetectorParameters()
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000)
        detector = aruco.ArucoDetector(aruco_dict,param)
        markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(self.inputImg)

        # Visualize detection of the Aruco markers:
        outputImage = self.inputImg.copy()
        cv2.aruco.drawDetectedMarkers(outputImage, markerCorners, markerIds)

        # Test if ArUco tags are detected properly:
        '''while True:
            cv2.imshow("UR3 Cranfield Cell (CUBE DETECTION): ArUco Detection", outputImage)

            key = cv2.waitKey(1)
            if key == ord('q'):
                cv2.destroyWindow("UR3 Cranfield Cell (CUBE DETECTION): ArUco Detection", self.outputImage)
                break'''

        # Calibration process:
        src = np.zeros((4, 2), dtype=np.float32)  # Points of the corners from the input image.
        dst = np.array([[0.0, 0.0], [self.w, 0.0], [0.0, self.h], [self.w, self.h]], dtype=np.float32)  # Points calibrated with w and h.
        
        poly_corner = np.zeros((4, 3), dtype=np.int32)

        # Get the first corner & ID of the markers:
        for i in range(4):
            poly_corner[i][0] = int(markerIds[i][0])
            poly_corner[i][1] = int(markerCorners[i][0][0][0])
            poly_corner[i][2] = int(markerCorners[i][0][0][1])

        # Arrange by ID: 
        for i in range(3):
            for j in range(i + 1, 4):
                if poly_corner[i][0] > poly_corner[j][0]:
                    for k in range(3):
                        aux = poly_corner[i][k]
                        poly_corner[i][k] = poly_corner[j][k]
                        poly_corner[j][k] = aux

        # Get the source vector:
        for i in range(4):
            src[i] = np.array([poly_corner[i][1], poly_corner[i][2]], dtype=np.float32)

        # Get the transform matrix:
        perspTransMatrix = cv2.getPerspectiveTransform(src, dst)

        # Get image of the perspective:
        self.perspectiveImg = cv2.warpPerspective(outputImage, perspTransMatrix, (int(self.w), int(self.h)))
        
        if ShowPerspective:

            while True:

                if self.perspectiveImg is not None:
                    self.perspectiveImgSHOW = cv2.resize(self.perspectiveImg, (750, 400))
                    cv2.imshow("UR3 Cranfield Cell (CUBE DETECTION): Perspective Image", self.perspectiveImgSHOW)

                key = cv2.waitKey(1)
                if key == ord('q'):
                    cv2.destroyWindow("UR3 Cranfield Cell (CUBE DETECTION): Perspective Image")
                    break 

    def CubeLocation(self):

        print("=== DETECTION: YOLOv8 MODEL ===")
        print("DETECTING the cube with YOLOv8 and getting its POSE...")
        print("")

        RESULT = {"x": 0.0, "y": 0.0, "yaw": 0.0, "detection": "", "success": False}

        # Run YOLOv8 model once, to load it properly:
        results = self.YOLOmodel(self.perspectiveImg)
        names = self.YOLOmodel.names

        # Run YOLOv8 detection for 1 seconds, and get RESULT:
        t_end = time.time() + 1.0
        Detected = False
        while time.time() < t_end:

            results = self.YOLOmodel(self.perspectiveImg)
            boxes = results[0].boxes

            ids = []
            for box in boxes:
                box = boxes.xyxy
                for c in boxes.cls:
                    ids.append(names[int(c)])

            for id in ids:

                if id == "sticker" or id == "cube":
                    print("")
                    Detected = True
                    break

            if Detected:
                self.YOLOOutput = results[0].plot()
                break

        if not Detected:

            self.YOLOOutput = self.perspectiveImg

            print("")
            print("ERROR: The YOLOv8 model could not detect any cube in the workspace.")
            print("")
            return(RESULT)

        # AFTER DETECTION -> Get ROI (Region-of-Interest):
        for box in boxes:
            name = names[int(box.cls[0])]
            if (name == "sticker" or name == "cube"): # The ROI must take the whole cube's BOUNDING BOX, not sticker's BOUNDING BOX!
                x1, y1, x2, y2 = box.xyxy[0] 
                break

        x = int(x1)-3
        y = int(y1)-3
        w = int(x2)+3
        h = int(y2)+3
        ROI = self.perspectiveImg[y:h, x:w]

        # Apply mask to IMG:
        ROI = cv2.GaussianBlur(ROI,(3,3),0)
        imgHSV = cv2.cvtColor(ROI, cv2.COLOR_BGR2HSV)
        lowLimit = (0, 10, 10)
        upLimit = (70, 255, 255)
        mask = cv2.inRange(imgHSV, lowLimit, upLimit)

        # Visualize ROI:
        '''while True:
            cv2.imshow("IRB-120 PoseEstimation: Cube-ROI", ROI)
            key = cv2.waitKey(1)
            if key == ord('q'):
                cv2.destroyWindow("IRB-120 PoseEstimation: Cube-ROI")
                break'''

        # Find CONTOURS:
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        poly_contour = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:
                poly_contour.append(contour)

        if not poly_contour:
            print("ERROR: No contours detected.")
            return(RESULT)

        for cnt in poly_contour:
            rect = cv2.minAreaRect(cnt)
            (xo, yo), (wo, ho), angle = rect
            xo = xo + x
            yo = yo + y

        RESULT["angle"] = angle
        RESULT["yaw"] = -(angle * 3.1416/180.0)
        RESULT["x"] = xo/1000 - 0.569/2
        RESULT["y"] = -yo/1000 + 0.299 + 0.095
        RESULT["detection"] = "Cube"
        RESULT["success"] = True

        for id in ids:

            if id == "white":
                RESULT["detection"] = "WhiteCube"
                break

            if id == "black":
                RESULT["detection"] = "BlackCube"
                break

            if id == "blue":
                RESULT["detection"] = "BlueCube"
                break

            if id == "sticker":
                RESULT["detection"] = "Sticker"

        return(RESULT)
    
    def PublishCoordinates(self, TYPE, X, Y, ANGLE):
        
        MSG = Coordinates()
        MSG.cubetype = TYPE
        MSG.x = X
        MSG.y = Y
        MSG.angle = ANGLE
     
        self.PUB.publisher_.publish(MSG)
            
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

    def ConstantVisualization_Perspective(self):

        global Gz_CAM
        global ENVIRONMENT

        while True:

            if (ENVIRONMENT == "GAZEBO"):
                # 1. SPIN /Image topic subscriber!
                rclpy.spin_once(self.GzCAM_SUB)
                # 2. ASSIGN IMG:
                self.inputImg = Gz_CAM
                # Get Perspective Image:
                self.GetPerspectiveImg(ShowPerspective = False)

            else:
                # ASSIGN IMG:
                self.ret, self.inputImg = self.camera.read()
                # Get Perspective Image:
                self.GetPerspectiveImg(ShowPerspective = False)


            # 3. Get -> YOLOv8 MODEL RESULT:
            if self.perspectiveImg is not None:
                results = self.YOLOmodel(self.perspectiveImg)
                annotated_frame = results[0].plot()
                VISUALIZE = cv2.resize(annotated_frame, (1280, 720))
                cv2.imshow("UR3 Cranfield Cell (CUBE DETECTION): YOLO Output (PerspectiveImg)", VISUALIZE)

            key = cv2.waitKey(1)
            if key == ord('e'):
                cv2.destroyWindow("UR3 Cranfield Cell (CUBE DETECTION): YOLO Output (PerspectiveImg)")
                break 

