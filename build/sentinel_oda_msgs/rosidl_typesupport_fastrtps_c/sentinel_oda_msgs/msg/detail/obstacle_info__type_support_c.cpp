// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from sentinel_oda_msgs:msg/ObstacleInfo.idl
// generated code does not contain a copyright notice
#include "sentinel_oda_msgs/msg/detail/obstacle_info__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "sentinel_oda_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "sentinel_oda_msgs/msg/detail/obstacle_info__struct.h"
#include "sentinel_oda_msgs/msg/detail/obstacle_info__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif


// forward declare type support functions


using _ObstacleInfo__ros_msg_type = sentinel_oda_msgs__msg__ObstacleInfo;

static bool _ObstacleInfo__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _ObstacleInfo__ros_msg_type * ros_message = static_cast<const _ObstacleInfo__ros_msg_type *>(untyped_ros_message);
  // Field name: closest_distance
  {
    cdr << ros_message->closest_distance;
  }

  // Field name: obstacle_width
  {
    cdr << ros_message->obstacle_width;
  }

  // Field name: current_heading
  {
    cdr << ros_message->current_heading;
  }

  // Field name: obstacle_left
  {
    cdr << ros_message->obstacle_left;
  }

  return true;
}

static bool _ObstacleInfo__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _ObstacleInfo__ros_msg_type * ros_message = static_cast<_ObstacleInfo__ros_msg_type *>(untyped_ros_message);
  // Field name: closest_distance
  {
    cdr >> ros_message->closest_distance;
  }

  // Field name: obstacle_width
  {
    cdr >> ros_message->obstacle_width;
  }

  // Field name: current_heading
  {
    cdr >> ros_message->current_heading;
  }

  // Field name: obstacle_left
  {
    cdr >> ros_message->obstacle_left;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_sentinel_oda_msgs
size_t get_serialized_size_sentinel_oda_msgs__msg__ObstacleInfo(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _ObstacleInfo__ros_msg_type * ros_message = static_cast<const _ObstacleInfo__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name closest_distance
  {
    size_t item_size = sizeof(ros_message->closest_distance);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name obstacle_width
  {
    size_t item_size = sizeof(ros_message->obstacle_width);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name current_heading
  {
    size_t item_size = sizeof(ros_message->current_heading);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name obstacle_left
  {
    size_t item_size = sizeof(ros_message->obstacle_left);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _ObstacleInfo__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_sentinel_oda_msgs__msg__ObstacleInfo(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_sentinel_oda_msgs
size_t max_serialized_size_sentinel_oda_msgs__msg__ObstacleInfo(
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

  // member: closest_distance
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: obstacle_width
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: current_heading
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: obstacle_left
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
    using DataType = sentinel_oda_msgs__msg__ObstacleInfo;
    is_plain =
      (
      offsetof(DataType, obstacle_left) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _ObstacleInfo__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_sentinel_oda_msgs__msg__ObstacleInfo(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_ObstacleInfo = {
  "sentinel_oda_msgs::msg",
  "ObstacleInfo",
  _ObstacleInfo__cdr_serialize,
  _ObstacleInfo__cdr_deserialize,
  _ObstacleInfo__get_serialized_size,
  _ObstacleInfo__max_serialized_size
};

static rosidl_message_type_support_t _ObstacleInfo__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_ObstacleInfo,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, sentinel_oda_msgs, msg, ObstacleInfo)() {
  return &_ObstacleInfo__type_support;
}

#if defined(__cplusplus)
}
#endif
