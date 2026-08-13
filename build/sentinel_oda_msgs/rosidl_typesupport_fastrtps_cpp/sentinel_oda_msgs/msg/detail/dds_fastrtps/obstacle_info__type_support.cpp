// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from sentinel_oda_msgs:msg/ObstacleInfo.idl
// generated code does not contain a copyright notice
#include "sentinel_oda_msgs/msg/detail/obstacle_info__rosidl_typesupport_fastrtps_cpp.hpp"
#include "sentinel_oda_msgs/msg/detail/obstacle_info__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace sentinel_oda_msgs
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_sentinel_oda_msgs
cdr_serialize(
  const sentinel_oda_msgs::msg::ObstacleInfo & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: closest_distance
  cdr << ros_message.closest_distance;
  // Member: obstacle_width
  cdr << ros_message.obstacle_width;
  // Member: current_heading
  cdr << ros_message.current_heading;
  // Member: obstacle_left
  cdr << ros_message.obstacle_left;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_sentinel_oda_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  sentinel_oda_msgs::msg::ObstacleInfo & ros_message)
{
  // Member: closest_distance
  cdr >> ros_message.closest_distance;

  // Member: obstacle_width
  cdr >> ros_message.obstacle_width;

  // Member: current_heading
  cdr >> ros_message.current_heading;

  // Member: obstacle_left
  cdr >> ros_message.obstacle_left;

  return true;
}  // NOLINT(readability/fn_size)

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_sentinel_oda_msgs
get_serialized_size(
  const sentinel_oda_msgs::msg::ObstacleInfo & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: closest_distance
  {
    size_t item_size = sizeof(ros_message.closest_distance);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: obstacle_width
  {
    size_t item_size = sizeof(ros_message.obstacle_width);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: current_heading
  {
    size_t item_size = sizeof(ros_message.current_heading);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: obstacle_left
  {
    size_t item_size = sizeof(ros_message.obstacle_left);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_sentinel_oda_msgs
max_serialized_size_ObstacleInfo(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;


  // Member: closest_distance
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: obstacle_width
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: current_heading
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: obstacle_left
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = sentinel_oda_msgs::msg::ObstacleInfo;
    is_plain =
      (
      offsetof(DataType, obstacle_left) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _ObstacleInfo__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const sentinel_oda_msgs::msg::ObstacleInfo *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _ObstacleInfo__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<sentinel_oda_msgs::msg::ObstacleInfo *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _ObstacleInfo__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const sentinel_oda_msgs::msg::ObstacleInfo *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _ObstacleInfo__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_ObstacleInfo(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _ObstacleInfo__callbacks = {
  "sentinel_oda_msgs::msg",
  "ObstacleInfo",
  _ObstacleInfo__cdr_serialize,
  _ObstacleInfo__cdr_deserialize,
  _ObstacleInfo__get_serialized_size,
  _ObstacleInfo__max_serialized_size
};

static rosidl_message_type_support_t _ObstacleInfo__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_ObstacleInfo__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace sentinel_oda_msgs

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_sentinel_oda_msgs
const rosidl_message_type_support_t *
get_message_type_support_handle<sentinel_oda_msgs::msg::ObstacleInfo>()
{
  return &sentinel_oda_msgs::msg::typesupport_fastrtps_cpp::_ObstacleInfo__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, sentinel_oda_msgs, msg, ObstacleInfo)() {
  return &sentinel_oda_msgs::msg::typesupport_fastrtps_cpp::_ObstacleInfo__handle;
}

#ifdef __cplusplus
}
#endif
