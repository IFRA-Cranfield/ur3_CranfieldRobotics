#!/usr/bin/python3
import sys
sys.dont_write_bytecode = True

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

# PositionEstimation.py
# This script performs:
#   - Object Detection using a custom YOLO model.
#   - Object Position Estimation (center of the detected YOLO-based bounding box) by calculating the object's position relative to the OpenCV-ArUco marker.

# ===== IMPORT REQUIRED COMPONENTS ===== #
import os, sys

# Required to include ROS 2 and its components:
import rclpy
from rclpy.node import Node

# ROS 2 data:
from objectpose_msgs.msg import ObjectPose
from sensor_msgs.msg import Image

# OpenCV:
import cv2
# ROS 2 to OpenCV -> cv_bridge:
from cv_bridge import CvBridge, CvBridgeError

# YOLO:
from ultralytics import YOLO

# ARUCO:
from arucoGRID import grid

# ================================================== #
# CLASS -> GazeboCamera:
class GazeboCamera(Node):

    def __init__(self):

        super().__init__("ros2ope_GzCAM")
        self.SubIMAGE = self.create_subscription(Image, "/camera/image_raw", self.CALLBACK_FN, 10)
        self.BRIDGE = CvBridge()

    def CALLBACK_FN(self, ros2_img):

        global GZ_CAM

        try:
            GZ_CAM = self.BRIDGE.imgmsg_to_cv2(ros2_img, "bgr8")
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

    global GZ_CAM

    print("")
    print(" --- Cranfield University --- ")
    print("        (c) IFRA Group        ")
    print("")

    print("Object Detection and Pose Estimation in ROS 2.")
    print("Python script -> PositionEstimation.py")
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

    # Get VISUALIZE parameter value:
    VISUALIZE = AssignArgument("visualize")
    if VISUALIZE == "True" or VISUALIZE == "true":
        print("Visualize results -> True")
        print("")
        VISUALIZE = True
    elif VISUALIZE == "False" or VISUALIZE == "false" or VISUALIZE == None:
        print("Visualize results -> False")
        print("")
        VISUALIZE = False
    else:
        print("")
        print("ERROR: visualize INPUT ARGUMENT has not been properly defined (True/False). Please try again.")
        print("Closing... BYE!")
        exit()

    rclpy.init()

    # Initialise CAMERAS:
    if ENVIRONMENT == "gazebo":
        CAMERA = GazeboCamera()
    elif ENVIRONMENT == "robot":
        CAMERA = cv2.VideoCapture(0)

    # Load custom YOLO MODEL:
    DIR = os.path.join(os.path.expanduser('~'), 'dev_ws', 'src', 'ur3_CranfieldRobotics', 'ur3cranfield_ope',  'yolo', 'models')
    modelPATH = DIR + "/" + MODELname + ".pt"

    if not os.path.exists(modelPATH):
        print("Selected YOLO model file not found. Please double check and try again.")
        print("Closing... BYE!")
        exit()

    # YOLOmodel:
    YOLOmodel = YOLO(modelPATH)
    names = YOLOmodel.names
    print("The YOLO model will try to detect the following objects:")
    print(names)
    print("")

    ObjectList = []
    for key in names:
        ObjectList.append(names[key])

    # Initialise PUBLISHER NODE:
    PUBnode = rclpy.create_node("ros2ope_PUBLISHER")

    PUBList = {}
    for x in ObjectList:
        TopicName = "/" + x + "/ObjectPoseEstimation"
        PUBList[x] = PUBnode.create_publisher(ObjectPose, TopicName, 10)

    # ARUCO:
    GRID = grid()

    # Run execution-PREDICTION INFERENCE:
    while True:

        if ENVIRONMENT == "gazebo":
            rclpy.spin_once(CAMERA)
            inputIMG = GZ_CAM
        elif ENVIRONMENT == "robot":
            ret, inputIMG = CAMERA.read()

        if inputIMG is not None:

            # A. DETECT ARUCO and RETURN ARUCO POSITION:
            ARUCO_RES = GRID.detectGRID(inputIMG)

            if not ARUCO_RES["Success"]:
                print("ERROR: ArUco grid detection lost. Please check ArUco markers are visible!")
                print("")

            else:

                convertedIMG = ARUCO_RES["GRID"]

                # B. EXECUTE YOLO-based object detection:
                PREDICTION = YOLOmodel.predict(convertedIMG, verbose=False)

                for R in PREDICTION:

                    boxes = R.boxes

                    for box in boxes:

                        # Get NAME of the detected OBJECT:
                        C = int(box.cls)
                        ObjectName = YOLOmodel.names[C]

                        ConfLevel = box.conf.item() # LEVEL OF CONFIDENCE.
                        B = box.xyxy[0] # Detected object's BOUNDING BOX.

                        # Calculate CENTER of BB:
                        BBx = (B[0] + B[2])/2
                        BBy = (B[1] + B[3])/2

                        print("Object found -> " + ObjectName + ", CL: " + str(ConfLevel))

                        if (ConfLevel >= 0.60):

                            print("=== PIXEL COORDINATES ===")
                            print("NAME: " + ObjectName + " X: " + str(BBx.item()) +", Y: " + str(BBy.item()))

                            # CALCULATE x and y COORDINATES of OBJECT:
                            OBJx = BBy/1000
                            OBJy = BBx/1000

                            # CALCULATE OBJECT COORDINATES RELATIVE TO ARUCO:
                            X = float(OBJx.item())
                            Y = float(OBJy.item())

                            print("=== LOCAL COORDINATES (ArUco Grid) ===")
                            print("NAME: " + ObjectName + " X: " + str(X) +", Y: " + str(Y))

                            # APPLY -> Corrections:
                            (X,Y) = GRID.applyCORRECTION(X,Y, ENVIRONMENT)

                            print("=== GLOBAL COORDINATES (CORRECTED) ===")
                            print("NAME: " + ObjectName + " X: " + str(X) +", Y: " + str(Y))
                            print("")

                            # PUBLISH POSE:
                            POSE = ObjectPose()
                            POSE.objectname = ObjectName
                            POSE.x = X
                            POSE.y = Y
                            POSE.z = GRID.fixedZ(ObjectName)

                            PUBList[ObjectName].publish(POSE)

                            # To visualize BoundingBoxes:
                            cv2.rectangle(convertedIMG, (int(B[0]), int(B[1])), (int(B[2]), int(B[3])), (0,0,0), 2)
                            cv2.circle(convertedIMG, (int(BBx), int(BBy)), radius=3, color=(0,255,0), thickness=-1)

                            # To visualize pose next to objects:
                            LABEL = ObjectName + " -> x: " + str(X) + ", y: " + str(Y)
                            cv2.putText(convertedIMG, LABEL, (int(B[0]), int(B[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)

                    print("")

                if VISUALIZE:

                    WINDOW = cv2.resize(convertedIMG, (850, 480))
                    TITLE = "YOLO MODEL -> " + MODELname + " PREDICTION RESULTS and OBJECT POSITION ESTIMATION"
                    cv2.imshow(TITLE, WINDOW)

                    key = cv2.waitKey(1)
                    if key == ord('e'):
                        cv2.destroyWindow(TITLE)
                        break

    print("")
    print("Object POSITION ESTIMATION finalised.")
    print("Closing... BYE!")

    if ENVIRONMENT == "gazebo":
        rclpy.shutdown()

if __name__ == '__main__':
    main()
