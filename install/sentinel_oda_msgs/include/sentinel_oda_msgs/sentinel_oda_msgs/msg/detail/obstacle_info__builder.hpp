// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from sentinel_oda_msgs:msg/ObstacleInfo.idl
// generated code does not contain a copyright notice

#ifndef SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_INFO__BUILDER_HPP_
#define SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_INFO__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "sentinel_oda_msgs/msg/detail/obstacle_info__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace sentinel_oda_msgs
{

namespace msg
{

namespace builder
{

class Init_ObstacleInfo_obstacle_left
{
public:
  explicit Init_ObstacleInfo_obstacle_left(::sentinel_oda_msgs::msg::ObstacleInfo & msg)
  : msg_(msg)
  {}
  ::sentinel_oda_msgs::msg::ObstacleInfo obstacle_left(::sentinel_oda_msgs::msg::ObstacleInfo::_obstacle_left_type arg)
  {
    msg_.obstacle_left = std::move(arg);
    return std::move(msg_);
  }

private:
  ::sentinel_oda_msgs::msg::ObstacleInfo msg_;
};

class Init_ObstacleInfo_current_heading
{
public:
  explicit Init_ObstacleInfo_current_heading(::sentinel_oda_msgs::msg::ObstacleInfo & msg)
  : msg_(msg)
  {}
  Init_ObstacleInfo_obstacle_left current_heading(::sentinel_oda_msgs::msg::ObstacleInfo::_current_heading_type arg)
  {
    msg_.current_heading = std::move(arg);
    return Init_ObstacleInfo_obstacle_left(msg_);
  }

private:
  ::sentinel_oda_msgs::msg::ObstacleInfo msg_;
};

class Init_ObstacleInfo_obstacle_width
{
public:
  explicit Init_ObstacleInfo_obstacle_width(::sentinel_oda_msgs::msg::ObstacleInfo & msg)
  : msg_(msg)
  {}
  Init_ObstacleInfo_current_heading obstacle_width(::sentinel_oda_msgs::msg::ObstacleInfo::_obstacle_width_type arg)
  {
    msg_.obstacle_width = std::move(arg);
    return Init_ObstacleInfo_current_heading(msg_);
  }

private:
  ::sentinel_oda_msgs::msg::ObstacleInfo msg_;
};

class Init_ObstacleInfo_closest_distance
{
public:
  Init_ObstacleInfo_closest_distance()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ObstacleInfo_obstacle_width closest_distance(::sentinel_oda_msgs::msg::ObstacleInfo::_closest_distance_type arg)
  {
    msg_.closest_distance = std::move(arg);
    return Init_ObstacleInfo_obstacle_width(msg_);
  }

private:
  ::sentinel_oda_msgs::msg::ObstacleInfo msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::sentinel_oda_msgs::msg::ObstacleInfo>()
{
  return sentinel_oda_msgs::msg::builder::Init_ObstacleInfo_closest_distance();
}

}  // namespace sentinel_oda_msgs

#endif  // SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_INFO__BUILDER_HPP_
