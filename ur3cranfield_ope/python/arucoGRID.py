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

# arucoMRKR.py
# This script contains the ros2ope_ARUCO class and its functions.

# ===== IMPORT REQUIRED COMPONENTS ===== #
import cv2
import numpy as np
import rclpy

# ====================================== #
# arucoGRID class:
class grid():
    
    def __init__(self):

        self.ARUCOdict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000)
        self.params = cv2.aruco.DetectorParameters()
        
        # Height and Width values for our ARUCO GRID at the UR3 STAND:
        self.H = 415   # Height of ARUCO-GRID (mm)
        self.W = 550   # Width of ARUCO-GRID (mm)
        
    def detectGRID(self, FRAME):
        
        RES = {}
        RES["GRID"] = None
        RES["Success"] = False
        
        # Detect ArUco markers:
        corners, ids, rejected_img_points = cv2.aruco.detectMarkers(FRAME, self.ARUCOdict, parameters=self.params)
        
        if ids is not None:

            if len(ids) != 4:
                return(RES)
            
            # cv2.aruco.drawDetectedMarkers(FRAME, corners, ids)
        
            # Calibration process:
            src = np.zeros((4, 2), dtype=np.float32)  # Points of the corners from the input image.
            dst = np.array([[0.0, 0.0], [self.W, 0.0], [0.0, self.H], [self.W, self.H]], dtype=np.float32)  # Points calibrated with w and h.
            
            poly_corner = np.zeros((4, 3), dtype=np.int32)
            
            # Get the first corner & ID of the markers:
            for i in range(4):
                poly_corner[i][0] = int(ids[i][0])
                poly_corner[i][1] = int(corners[i][0][0][0])
                poly_corner[i][2] = int(corners[i][0][0][1])

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
            
            # Get the TRANSFORMED IMAGE:
            perspectiveImg = cv2.warpPerspective(FRAME, perspTransMatrix, (int(self.W), int(self.H)))
            
            # RESULT:
            RES["GRID"] = perspectiveImg
            RES["Success"] = True
            return(RES)
        
        else:
            
            return(RES)
        
    # The correction values have been calculated and tuned manually, and might not be 100% accurate:
    def applyCORRECTION(self, x, y, ENV):

        xo = x
        yo = y
        
        # TRANSFORMATION -> From ORIGIN (0,0) to ArUco Grid ORIGIN (0.275,-0.035):
        x = -0.275 + yo
        y = 0.38 - xo

        # CORRECTION:
        # y = y + y*0.002
        
        return(x,y)
    
    def fixedZ(self, OBJECT):

        if OBJECT == "RedCube" or OBJECT == "WhiteCube" or OBJECT == "GreenCube" or OBJECT == "BlueCube":
            return(0.86)
        else:
            return(0.0)