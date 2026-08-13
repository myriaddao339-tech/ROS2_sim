# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target sentinel_oda_msgs::sentinel_oda_msgs
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${sentinel_oda_msgs_TARGETS}.
if(sentinel_oda_msgs_TARGETS AND NOT TARGET sentinel_oda_msgs::sentinel_oda_msgs)
  add_library(sentinel_oda_msgs::sentinel_oda_msgs INTERFACE IMPORTED)
  set_target_properties(sentinel_oda_msgs::sentinel_oda_msgs PROPERTIES
    INTERFACE_LINK_LIBRARIES "${sentinel_oda_msgs_TARGETS}")
endif()
