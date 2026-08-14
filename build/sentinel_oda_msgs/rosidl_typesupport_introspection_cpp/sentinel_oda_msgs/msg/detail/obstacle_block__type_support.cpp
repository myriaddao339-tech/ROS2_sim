// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from sentinel_oda_msgs:msg/ObstacleBlock.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "sentinel_oda_msgs/msg/detail/obstacle_block__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace sentinel_oda_msgs
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void ObstacleBlock_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) sentinel_oda_msgs::msg::ObstacleBlock(_init);
}

void ObstacleBlock_fini_function(void * message_memory)
{
  auto typed_message = static_cast<sentinel_oda_msgs::msg::ObstacleBlock *>(message_memory);
  typed_message->~ObstacleBlock();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ObstacleBlock_message_member_array[3] = {
  {
    "distance",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(sentinel_oda_msgs::msg::ObstacleBlock, distance),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "width",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(sentinel_oda_msgs::msg::ObstacleBlock, width),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "left",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(sentinel_oda_msgs::msg::ObstacleBlock, left),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ObstacleBlock_message_members = {
  "sentinel_oda_msgs::msg",  // message namespace
  "ObstacleBlock",  // message name
  3,  // number of fields
  sizeof(sentinel_oda_msgs::msg::ObstacleBlock),
  ObstacleBlock_message_member_array,  // message members
  ObstacleBlock_init_function,  // function to initialize message memory (memory has to be allocated)
  ObstacleBlock_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ObstacleBlock_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ObstacleBlock_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace sentinel_oda_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<sentinel_oda_msgs::msg::ObstacleBlock>()
{
  return &::sentinel_oda_msgs::msg::rosidl_typesupport_introspection_cpp::ObstacleBlock_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, sentinel_oda_msgs, msg, ObstacleBlock)() {
  return &::sentinel_oda_msgs::msg::rosidl_typesupport_introspection_cpp::ObstacleBlock_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
