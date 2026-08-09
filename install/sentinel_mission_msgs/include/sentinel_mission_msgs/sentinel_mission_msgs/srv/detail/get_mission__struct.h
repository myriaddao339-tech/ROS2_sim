// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from sentinel_mission_msgs:srv/GetMission.idl
// generated code does not contain a copyright notice

#ifndef SENTINEL_MISSION_MSGS__SRV__DETAIL__GET_MISSION__STRUCT_H_
#define SENTINEL_MISSION_MSGS__SRV__DETAIL__GET_MISSION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'mission_file'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/GetMission in the package sentinel_mission_msgs.
typedef struct sentinel_mission_msgs__srv__GetMission_Request
{
  rosidl_runtime_c__String mission_file;
} sentinel_mission_msgs__srv__GetMission_Request;

// Struct for a sequence of sentinel_mission_msgs__srv__GetMission_Request.
typedef struct sentinel_mission_msgs__srv__GetMission_Request__Sequence
{
  sentinel_mission_msgs__srv__GetMission_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} sentinel_mission_msgs__srv__GetMission_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"
// Member 'waypoints'
#include "mavros_msgs/msg/detail/waypoint__struct.h"

/// Struct defined in srv/GetMission in the package sentinel_mission_msgs.
typedef struct sentinel_mission_msgs__srv__GetMission_Response
{
  bool success;
  rosidl_runtime_c__String message;
  mavros_msgs__msg__Waypoint__Sequence waypoints;
} sentinel_mission_msgs__srv__GetMission_Response;

// Struct for a sequence of sentinel_mission_msgs__srv__GetMission_Response.
typedef struct sentinel_mission_msgs__srv__GetMission_Response__Sequence
{
  sentinel_mission_msgs__srv__GetMission_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} sentinel_mission_msgs__srv__GetMission_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SENTINEL_MISSION_MSGS__SRV__DETAIL__GET_MISSION__STRUCT_H_
