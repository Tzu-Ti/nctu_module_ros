cd ~/duckietown/catkin_ws/src/
catkin_create_pkg yolo rospy std_msgs
catkin_create_pkg find_person rospy std_msgs
catkin_create_pkg control_car rospy std_msgs
cp -r ~/nctu_module_ros/catkin_ws/src/yolo/src yolo
cp -r ~/nctu_module_ros/catkin_ws/src/control_car/src control_car
cp -r ~/nctu_module_ros/catkin_ws/src/find_person/src find_person
cp -r ~/nctu_module_ros/catkin_ws/src/yolo/launch yolo
cp -r ~/nctu_module_ros/catkin_ws/src/control_car/launch control_car
cp -r ~/nctu_module_ros/catkin_ws/src/find_person/launch find_person
cd ~/duckietown/catkin_ws
catkin_make
