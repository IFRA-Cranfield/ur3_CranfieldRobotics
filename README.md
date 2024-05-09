# ur3_CranfieldRobotics

SPAWN CUBES:
ros2 run ur3cranfield_execution SpawnObject.py --package "ur3cranfield_gazebo" --urdf "BlackCube.urdf" --name "BlackCube" --x -0.255 --y 0.12 --z 0.9
ros2 run ur3cranfield_execution SpawnObject.py --package "ur3cranfield_gazebo" --urdf "BlueCube.urdf" --name "BlueCube" --x -0.255 --y 0.36 --z 0.9
ros2 run ur3cranfield_execution SpawnObject.py --package "ur3cranfield_gazebo" --urdf "WhiteCube.urdf" --name "WhiteCube" --x 0.255 --y 0.12 --z 0.9
ros2 run ur3cranfield_execution SpawnObject.py --package "ur3cranfield_gazebo" --urdf "Cube.urdf" --name "Cube" --x 0.255 --y 0.36 --z 0.9

EXECUTE PROGRAM:
ros2 run ur3cranfield_execution sequence.py --ros-args -p PROGRAM_FILENAME:="cubePP_handE" -p ROBOT_MODEL:="ur3" -p EE_MODEL:="robotiq_hande" -p GzBr_ENV:="gazebo"