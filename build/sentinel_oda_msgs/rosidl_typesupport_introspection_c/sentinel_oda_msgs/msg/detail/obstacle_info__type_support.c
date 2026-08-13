// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from sentinel_oda_msgs:msg/ObstacleInfo.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "sentinel_oda_msgs/msg/detail/obstacle_info__rosidl_typesupport_introspection_c.h"
#include "sentinel_oda_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "sentinel_oda_msgs/msg/detail/obstacle_info__functions.h"
#include "sentinel_oda_msgs/msg/detail/obstacle_info__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void sentinel_oda_msgs__msg__ObstacleInfo__rosidl_typesupport_introspection_c__ObstacleInfo_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  sentinel_oda_msgs__msg__ObstacleInfo__init(message_memory);
}

void sentinel_oda_msgs__msg__ObstacleInfo__rosidl_typesupport_introspection_c__ObstacleInfo_fini_function(void * message_memory)
{
  sentinel_oda_msgs__msg__ObstacleInfo__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember sentinel_oda_msgs__msg__ObstacleInfo__rosidl_typesupport_introspection_c__ObstacleInfo_message_member_array[4] = {
  {
    "closest_distance",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(sentinel_oda_msgs__msg__ObstacleInfo, closest_distance),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "obstacle_width",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(sentinel_oda_msgs__msg__ObstacleInfo, obstacle_width),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "current_heading",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(sentinel_oda_msgs__msg__ObstacleInfo, current_heading),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "obstacle_left",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(sentinel_oda_msgs__msg__ObstacleInfo, obstacle_left),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers sentinel_oda_msgs__msg__ObstacleInfo__rosidl_typesupport_introspection_c__ObstacleInfo_message_members = {
  "sentinel_oda_msgs__msg",  // message namespace
  "ObstacleInfo",  // message name
  4,  // number of fields
  sizeof(sentinel_oda_msgs__msg__ObstacleInfo),
  sentinel_oda_msgs__msg__ObstacleInfo__rosidl_typesupport_introspection_c__ObstacleInfo_message_member_array,  // message members
  sentinel_oda_msgs__msg__ObstacleInfo__rosidl_typesupport_introspection_c__ObstacleInfo_init_function,  // function to initialize message memory (memory has to be allocated)
  sentinel_oda_msgs__msg__ObstacleInfo__rosidl_typesupport_introspection_c__ObstacleInfo_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t sentinel_oda_msgs__msg__ObstacleInfo__rosidl_typesupport_introspection_c__ObstacleInfo_message_type_support_handle = {
  0,
  &sentinel_oda_msgs__msg__ObstacleInfo__rosidl_typesupport_introspection_c__ObstacleInfo_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_sentinel_oda_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sentinel_oda_msgs, msg, ObstacleInfo)() {
  if (!sentinel_oda_msgs__msg__ObstacleInfo__rosidl_typesupport_introspection_c__ObstacleInfo_message_type_support_handle.typesupport_identifier) {
    sentinel_oda_msgs__msg__ObstacleInfo__rosidl_typesupport_introspection_c__ObstacleInfo_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &sentinel_oda_msgs__msg__ObstacleInfo__rosidl_typesupport_introspection_c__ObstacleInfo_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
