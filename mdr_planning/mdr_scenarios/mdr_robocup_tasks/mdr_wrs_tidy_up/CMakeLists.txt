cmake_minimum_required(VERSION 2.8.3)
project(mdr_wrs_tidy_up)

find_package(catkin REQUIRED COMPONENTS
  rospy
  roslint
  std_msgs
  geometry_msgs
  mdr_manipulation_msgs
  mas_execution_manager
  mas_knowledge_base
)

catkin_python_setup()

catkin_package(
  CATKIN_DEPENDS
    rospy
    std_msgs
    geometry_msgs
    mdr_manipulation_msgs
    mas_execution_manager
    mas_knowledge_base
)

include_directories()

install(DIRECTORY ros/launch/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/ros/launch
)
