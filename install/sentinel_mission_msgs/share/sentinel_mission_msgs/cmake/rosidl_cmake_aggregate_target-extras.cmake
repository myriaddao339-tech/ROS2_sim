# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target sentinel_mission_msgs::sentinel_mission_msgs
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${sentinel_mission_msgs_TARGETS}.
if(sentinel_mission_msgs_TARGETS AND NOT TARGET sentinel_mission_msgs::sentinel_mission_msgs)
  add_library(sentinel_mission_msgs::sentinel_mission_msgs INTERFACE IMPORTED)
  set_target_properties(sentinel_mission_msgs::sentinel_mission_msgs PROPERTIES
    INTERFACE_LINK_LIBRARIES "${sentinel_mission_msgs_TARGETS}")
endif()
