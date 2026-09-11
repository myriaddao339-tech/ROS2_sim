// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from sentinel_oda_msgs:msg/ObstacleInfo.idl
// generated code does not contain a copyright notice

#ifndef SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_INFO__TRAITS_HPP_
#define SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_INFO__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "sentinel_oda_msgs/msg/detail/obstacle_info__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'blocks'
#include "sentinel_oda_msgs/msg/detail/obstacle_block__traits.hpp"

namespace sentinel_oda_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const ObstacleInfo & msg,
  std::ostream & out)
{
  out << "{";
  // member: blocks
  {
    if (msg.blocks.size() == 0) {
      out << "blocks: []";
    } else {
      out << "blocks: [";
      size_t pending_items = msg.blocks.size();
      for (auto item : msg.blocks) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: closest_distance
  {
    out << "closest_distance: ";
    rosidl_generator_traits::value_to_yaml(msg.closest_distance, out);
    out << ", ";
  }

  // member: obstacle_width
  {
    out << "obstacle_width: ";
    rosidl_generator_traits::value_to_yaml(msg.obstacle_width, out);
    out << ", ";
  }

  // member: current_heading
  {
    out << "current_heading: ";
    rosidl_generator_traits::value_to_yaml(msg.current_heading, out);
    out << ", ";
  }

  // member: obstacle_left
  {
    out << "obstacle_left: ";
    rosidl_generator_traits::value_to_yaml(msg.obstacle_left, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ObstacleInfo & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: blocks
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.blocks.size() == 0) {
      out << "blocks: []\n";
    } else {
      out << "blocks:\n";
      for (auto item : msg.blocks) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: closest_distance
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "closest_distance: ";
    rosidl_generator_traits::value_to_yaml(msg.closest_distance, out);
    out << "\n";
  }

  // member: obstacle_width
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "obstacle_width: ";
    rosidl_generator_traits::value_to_yaml(msg.obstacle_width, out);
    out << "\n";
  }

  // member: current_heading
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "current_heading: ";
    rosidl_generator_traits::value_to_yaml(msg.current_heading, out);
    out << "\n";
  }

  // member: obstacle_left
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "obstacle_left: ";
    rosidl_generator_traits::value_to_yaml(msg.obstacle_left, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ObstacleInfo & msg, bool use_flow_style = false)
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
  const sentinel_oda_msgs::msg::ObstacleInfo & msg,
  std::ostream & out, size_t indentation = 0)
{
  sentinel_oda_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use sentinel_oda_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const sentinel_oda_msgs::msg::ObstacleInfo & msg)
{
  return sentinel_oda_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<sentinel_oda_msgs::msg::ObstacleInfo>()
{
  return "sentinel_oda_msgs::msg::ObstacleInfo";
}

template<>
inline const char * name<sentinel_oda_msgs::msg::ObstacleInfo>()
{
  return "sentinel_oda_msgs/msg/ObstacleInfo";
}

template<>
struct has_fixed_size<sentinel_oda_msgs::msg::ObstacleInfo>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<sentinel_oda_msgs::msg::ObstacleInfo>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<sentinel_oda_msgs::msg::ObstacleInfo>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_INFO__TRAITS_HPP_
