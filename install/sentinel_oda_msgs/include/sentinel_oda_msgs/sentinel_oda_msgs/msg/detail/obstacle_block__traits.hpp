// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from sentinel_oda_msgs:msg/ObstacleBlock.idl
// generated code does not contain a copyright notice

#ifndef SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_BLOCK__TRAITS_HPP_
#define SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_BLOCK__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "sentinel_oda_msgs/msg/detail/obstacle_block__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace sentinel_oda_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const ObstacleBlock & msg,
  std::ostream & out)
{
  out << "{";
  // member: distance
  {
    out << "distance: ";
    rosidl_generator_traits::value_to_yaml(msg.distance, out);
    out << ", ";
  }

  // member: width
  {
    out << "width: ";
    rosidl_generator_traits::value_to_yaml(msg.width, out);
    out << ", ";
  }

  // member: left
  {
    out << "left: ";
    rosidl_generator_traits::value_to_yaml(msg.left, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ObstacleBlock & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: distance
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "distance: ";
    rosidl_generator_traits::value_to_yaml(msg.distance, out);
    out << "\n";
  }

  // member: width
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "width: ";
    rosidl_generator_traits::value_to_yaml(msg.width, out);
    out << "\n";
  }

  // member: left
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "left: ";
    rosidl_generator_traits::value_to_yaml(msg.left, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ObstacleBlock & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace sentinel_oda_msgs

namespace rosidl_generator_traits
{

[[deprecated("use sentinel_oda_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const sentinel_oda_msgs::msg::ObstacleBlock & msg,
  std::ostream & out, size_t indentation = 0)
{
  sentinel_oda_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use sentinel_oda_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const sentinel_oda_msgs::msg::ObstacleBlock & msg)
{
  return sentinel_oda_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<sentinel_oda_msgs::msg::ObstacleBlock>()
{
  return "sentinel_oda_msgs::msg::ObstacleBlock";
}

template<>
inline const char * name<sentinel_oda_msgs::msg::ObstacleBlock>()
{
  return "sentinel_oda_msgs/msg/ObstacleBlock";
}

template<>
struct has_fixed_size<sentinel_oda_msgs::msg::ObstacleBlock>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<sentinel_oda_msgs::msg::ObstacleBlock>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<sentinel_oda_msgs::msg::ObstacleBlock>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_BLOCK__TRAITS_HPP_
