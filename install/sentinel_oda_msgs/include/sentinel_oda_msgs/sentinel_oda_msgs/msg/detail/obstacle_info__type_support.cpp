// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from sentinel_oda_msgs:msg/ObstacleInfo.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "sentinel_oda_msgs/msg/detail/obstacle_info__struct.hpp"
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

void ObstacleInfo_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) sentinel_oda_msgs::msg::ObstacleInfo(_init);
}

void ObstacleInfo_fini_function(void * message_memory)
{
  auto typed_message = static_cast<sentinel_oda_msgs::msg::ObstacleInfo *>(message_memory);
  typed_message->~ObstacleInfo();
}

size_t size_function__ObstacleInfo__blocks(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<sentinel_oda_msgs::msg::ObstacleBlock> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ObstacleInfo__blocks(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<sentinel_oda_msgs::msg::ObstacleBlock> *>(untyped_member);
  return &member[index];
}

void * get_function__ObstacleInfo__blocks(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<sentinel_oda_msgs::msg::ObstacleBlock> *>(untyped_member);
  return &member[index];
}

void fetch_function__ObstacleInfo__blocks(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const sentinel_oda_msgs::msg::ObstacleBlock *>(
    get_const_function__ObstacleInfo__blocks(untyped_member, index));
  auto & value = *reinterpret_cast<sentinel_oda_msgs::msg::ObstacleBlock *>(untyped_value);
  value = item;
}

void assign_function__ObstacleInfo__blocks(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<sentinel_oda_msgs::msg::ObstacleBlock *>(
    get_function__ObstacleInfo__blocks(untyped_member, index));
  const auto & value = *reinterpret_cast<const sentinel_oda_msgs::msg::ObstacleBlock *>(untyped_value);
  item = value;
}

void resize_function__ObstacleInfo__blocks(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<sentinel_oda_msgs::msg::ObstacleBlock> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ObstacleInfo_message_member_array[5] = {
  {
    "blocks",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<sentinel_oda_msgs::msg::ObstacleBlock>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(sentinel_oda_msgs::msg::ObstacleInfo, blocks),  // bytes offset in struct
    nullptr,  // default value
    size_function__ObstacleInfo__blocks,  // size() function pointer
    get_const_function__ObstacleInfo__blocks,  // get_const(index) function pointer
    get_function__ObstacleInfo__blocks,  // get(index) function pointer
    fetch_function__ObstacleInfo__blocks,  // fetch(index, &value) function pointer
    assign_function__ObstacleInfo__blocks,  // assign(index, value) function pointer
    resize_function__ObstacleInfo__blocks  // resize(index) function pointer
  },
  {
    "closest_distance",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(sentinel_oda_msgs::msg::ObstacleInfo, closest_distance),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "obstacle_width",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(sentinel_oda_msgs::msg::ObstacleInfo, obstacle_width),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "current_heading",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(sentinel_oda_msgs::msg::ObstacleInfo, current_heading),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "obstacle_left",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(sentinel_oda_msgs::msg::ObstacleInfo, obstacle_left),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ObstacleInfo_message_members = {
  "sentinel_oda_msgs::msg",  // message namespace
  "ObstacleInfo",  // message name
  5,  // number of fields
  sizeof(sentinel_oda_msgs::msg::ObstacleInfo),
  ObstacleInfo_message_member_array,  // message members
  ObstacleInfo_init_function,  // function to initialize message memory (memory has to be allocated)
  ObstacleInfo_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ObstacleInfo_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ObstacleInfo_message_members,
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
get_message_type_support_handle<sentinel_oda_msgs::msg::ObstacleInfo>()
{
  return &::sentinel_oda_msgs::msg::rosidl_typesupport_introspection_cpp::ObstacleInfo_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, sentinel_oda_msgs, msg, ObstacleInfo)() {
  return &::sentinel_oda_msgs::msg::rosidl_typesupport_introspection_cpp::ObstacleInfo_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
