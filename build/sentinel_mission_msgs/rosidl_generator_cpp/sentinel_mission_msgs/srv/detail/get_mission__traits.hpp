// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from sentinel_mission_msgs:srv/GetMission.idl
// generated code does not contain a copyright notice

#ifndef SENTINEL_MISSION_MSGS__SRV__DETAIL__GET_MISSION__TRAITS_HPP_
#define SENTINEL_MISSION_MSGS__SRV__DETAIL__GET_MISSION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "sentinel_mission_msgs/srv/detail/get_mission__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace sentinel_mission_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetMission_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: mission_file
  {
    out << "mission_file: ";
    rosidl_generator_traits::value_to_yaml(msg.mission_file, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetMission_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: mission_file
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "mission_file: ";
    rosidl_generator_traits::value_to_yaml(msg.mission_file, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetMission_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace sentinel_mission_msgs

namespace rosidl_generator_traits
{

[[deprecated("use sentinel_mission_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const sentinel_mission_msgs::srv::GetMission_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  sentinel_mission_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use sentinel_mission_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const sentinel_mission_msgs::srv::GetMission_Request & msg)
{
  return sentinel_mission_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<sentinel_mission_msgs::srv::GetMission_Request>()
{
  return "sentinel_mission_msgs::srv::GetMission_Request";
}

template<>
inline const char * name<sentinel_mission_msgs::srv::GetMission_Request>()
{
  return "sentinel_mission_msgs/srv/GetMission_Request";
}

template<>
struct has_fixed_size<sentinel_mission_msgs::srv::GetMission_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<sentinel_mission_msgs::srv::GetMission_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<sentinel_mission_msgs::srv::GetMission_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'waypoints'
#include "mavros_msgs/msg/detail/waypoint__traits.hpp"

namespace sentinel_mission_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetMission_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << ", ";
  }

  // member: waypoints
  {
    if (msg.waypoints.size() == 0) {
      out << "waypoints: []";
    } else {
      out << "waypoints: [";
      size_t pending_items = msg.waypoints.size();
      for (auto item : msg.waypoints) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetMission_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }

  // member: waypoints
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.waypoints.size() == 0) {
      out << "waypoints: []\n";
    } else {
      out << "waypoints:\n";
      for (auto item : msg.waypoints) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetMission_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace sentinel_mission_msgs

namespace rosidl_generator_traits
{

[[deprecated("use sentinel_mission_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const sentinel_mission_msgs::srv::GetMission_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  sentinel_mission_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use sentinel_mission_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const sentinel_mission_msgs::srv::GetMission_Response & msg)
{
  return sentinel_mission_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<sentinel_mission_msgs::srv::GetMission_Response>()
{
  return "sentinel_mission_msgs::srv::GetMission_Response";
}

template<>
inline const char * name<sentinel_mission_msgs::srv::GetMission_Response>()
{
  return "sentinel_mission_msgs/srv/GetMission_Response";
}

template<>
struct has_fixed_size<sentinel_mission_msgs::srv::GetMission_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<sentinel_mission_msgs::srv::GetMission_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<sentinel_mission_msgs::srv::GetMission_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<sentinel_mission_msgs::srv::GetMission>()
{
  return "sentinel_mission_msgs::srv::GetMission";
}

template<>
inline const char * name<sentinel_mission_msgs::srv::GetMission>()
{
  return "sentinel_mission_msgs/srv/GetMission";
}

template<>
struct has_fixed_size<sentinel_mission_msgs::srv::GetMission>
  : std::integral_constant<
    bool,
    has_fixed_size<sentinel_mission_msgs::srv::GetMission_Request>::value &&
    has_fixed_size<sentinel_mission_msgs::srv::GetMission_Response>::value
  >
{
};

template<>
struct has_bounded_size<sentinel_mission_msgs::srv::GetMission>
  : std::integral_constant<
    bool,
    has_bounded_size<sentinel_mission_msgs::srv::GetMission_Request>::value &&
    has_bounded_size<sentinel_mission_msgs::srv::GetMission_Response>::value
  >
{
};

template<>
struct is_service<sentinel_mission_msgs::srv::GetMission>
  : std::true_type
{
};

template<>
struct is_service_request<sentinel_mission_msgs::srv::GetMission_Request>
  : std::true_type
{
};

template<>
struct is_service_response<sentinel_mission_msgs::srv::GetMission_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // SENTINEL_MISSION_MSGS__SRV__DETAIL__GET_MISSION__TRAITS_HPP_
