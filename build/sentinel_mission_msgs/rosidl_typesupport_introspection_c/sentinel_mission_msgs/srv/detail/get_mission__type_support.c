// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from sentinel_mission_msgs:srv/GetMission.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "sentinel_mission_msgs/srv/detail/get_mission__rosidl_typesupport_introspection_c.h"
#include "sentinel_mission_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "sentinel_mission_msgs/srv/detail/get_mission__functions.h"
#include "sentinel_mission_msgs/srv/detail/get_mission__struct.h"


// Include directives for member types
// Member `mission_file`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void sentinel_mission_msgs__srv__GetMission_Request__rosidl_typesupport_introspection_c__GetMission_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  sentinel_mission_msgs__srv__GetMission_Request__init(message_memory);
}

void sentinel_mission_msgs__srv__GetMission_Request__rosidl_typesupport_introspection_c__GetMission_Request_fini_function(void * message_memory)
{
  sentinel_mission_msgs__srv__GetMission_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember sentinel_mission_msgs__srv__GetMission_Request__rosidl_typesupport_introspection_c__GetMission_Request_message_member_array[1] = {
  {
    "mission_file",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(sentinel_mission_msgs__srv__GetMission_Request, mission_file),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers sentinel_mission_msgs__srv__GetMission_Request__rosidl_typesupport_introspection_c__GetMission_Request_message_members = {
  "sentinel_mission_msgs__srv",  // message namespace
  "GetMission_Request",  // message name
  1,  // number of fields
  sizeof(sentinel_mission_msgs__srv__GetMission_Request),
  sentinel_mission_msgs__srv__GetMission_Request__rosidl_typesupport_introspection_c__GetMission_Request_message_member_array,  // message members
  sentinel_mission_msgs__srv__GetMission_Request__rosidl_typesupport_introspection_c__GetMission_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  sentinel_mission_msgs__srv__GetMission_Request__rosidl_typesupport_introspection_c__GetMission_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t sentinel_mission_msgs__srv__GetMission_Request__rosidl_typesupport_introspection_c__GetMission_Request_message_type_support_handle = {
  0,
  &sentinel_mission_msgs__srv__GetMission_Request__rosidl_typesupport_introspection_c__GetMission_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_sentinel_mission_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sentinel_mission_msgs, srv, GetMission_Request)() {
  if (!sentinel_mission_msgs__srv__GetMission_Request__rosidl_typesupport_introspection_c__GetMission_Request_message_type_support_handle.typesupport_identifier) {
    sentinel_mission_msgs__srv__GetMission_Request__rosidl_typesupport_introspection_c__GetMission_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &sentinel_mission_msgs__srv__GetMission_Request__rosidl_typesupport_introspection_c__GetMission_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "sentinel_mission_msgs/srv/detail/get_mission__rosidl_typesupport_introspection_c.h"
// already included above
// #include "sentinel_mission_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "sentinel_mission_msgs/srv/detail/get_mission__functions.h"
// already included above
// #include "sentinel_mission_msgs/srv/detail/get_mission__struct.h"


// Include directives for member types
// Member `message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"
// Member `waypoints`
#include "mavros_msgs/msg/waypoint.h"
// Member `waypoints`
#include "mavros_msgs/msg/detail/waypoint__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__GetMission_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  sentinel_mission_msgs__srv__GetMission_Response__init(message_memory);
}

void sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__GetMission_Response_fini_function(void * message_memory)
{
  sentinel_mission_msgs__srv__GetMission_Response__fini(message_memory);
}

size_t sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__size_function__GetMission_Response__waypoints(
  const void * untyped_member)
{
  const mavros_msgs__msg__Waypoint__Sequence * member =
    (const mavros_msgs__msg__Waypoint__Sequence *)(untyped_member);
  return member->size;
}

const void * sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__get_const_function__GetMission_Response__waypoints(
  const void * untyped_member, size_t index)
{
  const mavros_msgs__msg__Waypoint__Sequence * member =
    (const mavros_msgs__msg__Waypoint__Sequence *)(untyped_member);
  return &member->data[index];
}

void * sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__get_function__GetMission_Response__waypoints(
  void * untyped_member, size_t index)
{
  mavros_msgs__msg__Waypoint__Sequence * member =
    (mavros_msgs__msg__Waypoint__Sequence *)(untyped_member);
  return &member->data[index];
}

void sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__fetch_function__GetMission_Response__waypoints(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const mavros_msgs__msg__Waypoint * item =
    ((const mavros_msgs__msg__Waypoint *)
    sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__get_const_function__GetMission_Response__waypoints(untyped_member, index));
  mavros_msgs__msg__Waypoint * value =
    (mavros_msgs__msg__Waypoint *)(untyped_value);
  *value = *item;
}

void sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__assign_function__GetMission_Response__waypoints(
  void * untyped_member, size_t index, const void * untyped_value)
{
  mavros_msgs__msg__Waypoint * item =
    ((mavros_msgs__msg__Waypoint *)
    sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__get_function__GetMission_Response__waypoints(untyped_member, index));
  const mavros_msgs__msg__Waypoint * value =
    (const mavros_msgs__msg__Waypoint *)(untyped_value);
  *item = *value;
}

bool sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__resize_function__GetMission_Response__waypoints(
  void * untyped_member, size_t size)
{
  mavros_msgs__msg__Waypoint__Sequence * member =
    (mavros_msgs__msg__Waypoint__Sequence *)(untyped_member);
  mavros_msgs__msg__Waypoint__Sequence__fini(member);
  return mavros_msgs__msg__Waypoint__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__GetMission_Response_message_member_array[3] = {
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(sentinel_mission_msgs__srv__GetMission_Response, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "message",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(sentinel_mission_msgs__srv__GetMission_Response, message),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "waypoints",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(sentinel_mission_msgs__srv__GetMission_Response, waypoints),  // bytes offset in struct
    NULL,  // default value
    sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__size_function__GetMission_Response__waypoints,  // size() function pointer
    sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__get_const_function__GetMission_Response__waypoints,  // get_const(index) function pointer
    sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__get_function__GetMission_Response__waypoints,  // get(index) function pointer
    sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__fetch_function__GetMission_Response__waypoints,  // fetch(index, &value) function pointer
    sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__assign_function__GetMission_Response__waypoints,  // assign(index, value) function pointer
    sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__resize_function__GetMission_Response__waypoints  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__GetMission_Response_message_members = {
  "sentinel_mission_msgs__srv",  // message namespace
  "GetMission_Response",  // message name
  3,  // number of fields
  sizeof(sentinel_mission_msgs__srv__GetMission_Response),
  sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__GetMission_Response_message_member_array,  // message members
  sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__GetMission_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__GetMission_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__GetMission_Response_message_type_support_handle = {
  0,
  &sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__GetMission_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_sentinel_mission_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sentinel_mission_msgs, srv, GetMission_Response)() {
  sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__GetMission_Response_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, mavros_msgs, msg, Waypoint)();
  if (!sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__GetMission_Response_message_type_support_handle.typesupport_identifier) {
    sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__GetMission_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &sentinel_mission_msgs__srv__GetMission_Response__rosidl_typesupport_introspection_c__GetMission_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "sentinel_mission_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "sentinel_mission_msgs/srv/detail/get_mission__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers sentinel_mission_msgs__srv__detail__get_mission__rosidl_typesupport_introspection_c__GetMission_service_members = {
  "sentinel_mission_msgs__srv",  // service namespace
  "GetMission",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // sentinel_mission_msgs__srv__detail__get_mission__rosidl_typesupport_introspection_c__GetMission_Request_message_type_support_handle,
  NULL  // response message
  // sentinel_mission_msgs__srv__detail__get_mission__rosidl_typesupport_introspection_c__GetMission_Response_message_type_support_handle
};

static rosidl_service_type_support_t sentinel_mission_msgs__srv__detail__get_mission__rosidl_typesupport_introspection_c__GetMission_service_type_support_handle = {
  0,
  &sentinel_mission_msgs__srv__detail__get_mission__rosidl_typesupport_introspection_c__GetMission_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sentinel_mission_msgs, srv, GetMission_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sentinel_mission_msgs, srv, GetMission_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_sentinel_mission_msgs
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sentinel_mission_msgs, srv, GetMission)() {
  if (!sentinel_mission_msgs__srv__detail__get_mission__rosidl_typesupport_introspection_c__GetMission_service_type_support_handle.typesupport_identifier) {
    sentinel_mission_msgs__srv__detail__get_mission__rosidl_typesupport_introspection_c__GetMission_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)sentinel_mission_msgs__srv__detail__get_mission__rosidl_typesupport_introspection_c__GetMission_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sentinel_mission_msgs, srv, GetMission_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sentinel_mission_msgs, srv, GetMission_Response)()->data;
  }

  return &sentinel_mission_msgs__srv__detail__get_mission__rosidl_typesupport_introspection_c__GetMission_service_type_support_handle;
}
