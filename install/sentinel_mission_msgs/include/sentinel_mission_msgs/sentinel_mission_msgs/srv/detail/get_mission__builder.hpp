// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from sentinel_mission_msgs:srv/GetMission.idl
// generated code does not contain a copyright notice

#ifndef SENTINEL_MISSION_MSGS__SRV__DETAIL__GET_MISSION__BUILDER_HPP_
#define SENTINEL_MISSION_MSGS__SRV__DETAIL__GET_MISSION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "sentinel_mission_msgs/srv/detail/get_mission__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace sentinel_mission_msgs
{

namespace srv
{

namespace builder
{

class Init_GetMission_Request_mission_file
{
public:
  Init_GetMission_Request_mission_file()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::sentinel_mission_msgs::srv::GetMission_Request mission_file(::sentinel_mission_msgs::srv::GetMission_Request::_mission_file_type arg)
  {
    msg_.mission_file = std::move(arg);
    return std::move(msg_);
  }

private:
  ::sentinel_mission_msgs::srv::GetMission_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::sentinel_mission_msgs::srv::GetMission_Request>()
{
  return sentinel_mission_msgs::srv::builder::Init_GetMission_Request_mission_file();
}

}  // namespace sentinel_mission_msgs


namespace sentinel_mission_msgs
{

namespace srv
{

namespace builder
{

class Init_GetMission_Response_waypoints
{
public:
  explicit Init_GetMission_Response_waypoints(::sentinel_mission_msgs::srv::GetMission_Response & msg)
  : msg_(msg)
  {}
  ::sentinel_mission_msgs::srv::GetMission_Response waypoints(::sentinel_mission_msgs::srv::GetMission_Response::_waypoints_type arg)
  {
    msg_.waypoints = std::move(arg);
    return std::move(msg_);
  }

private:
  ::sentinel_mission_msgs::srv::GetMission_Response msg_;
};

class Init_GetMission_Response_message
{
public:
  explicit Init_GetMission_Response_message(::sentinel_mission_msgs::srv::GetMission_Response & msg)
  : msg_(msg)
  {}
  Init_GetMission_Response_waypoints message(::sentinel_mission_msgs::srv::GetMission_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_GetMission_Response_waypoints(msg_);
  }

private:
  ::sentinel_mission_msgs::srv::GetMission_Response msg_;
};

class Init_GetMission_Response_success
{
public:
  Init_GetMission_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetMission_Response_message success(::sentinel_mission_msgs::srv::GetMission_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_GetMission_Response_message(msg_);
  }

private:
  ::sentinel_mission_msgs::srv::GetMission_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::sentinel_mission_msgs::srv::GetMission_Response>()
{
  return sentinel_mission_msgs::srv::builder::Init_GetMission_Response_success();
}

}  // namespace sentinel_mission_msgs

#endif  // SENTINEL_MISSION_MSGS__SRV__DETAIL__GET_MISSION__BUILDER_HPP_
