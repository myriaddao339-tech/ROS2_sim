// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from sentinel_oda_msgs:msg/ObstacleBlock.idl
// generated code does not contain a copyright notice

#ifndef SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_BLOCK__BUILDER_HPP_
#define SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_BLOCK__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "sentinel_oda_msgs/msg/detail/obstacle_block__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace sentinel_oda_msgs
{

namespace msg
{

namespace builder
{

class Init_ObstacleBlock_left
{
public:
  explicit Init_ObstacleBlock_left(::sentinel_oda_msgs::msg::ObstacleBlock & msg)
  : msg_(msg)
  {}
  ::sentinel_oda_msgs::msg::ObstacleBlock left(::sentinel_oda_msgs::msg::ObstacleBlock::_left_type arg)
  {
    msg_.left = std::move(arg);
    return std::move(msg_);
  }

private:
  ::sentinel_oda_msgs::msg::ObstacleBlock msg_;
};

class Init_ObstacleBlock_width
{
public:
  explicit Init_ObstacleBlock_width(::sentinel_oda_msgs::msg::ObstacleBlock & msg)
  : msg_(msg)
  {}
  Init_ObstacleBlock_left width(::sentinel_oda_msgs::msg::ObstacleBlock::_width_type arg)
  {
    msg_.width = std::move(arg);
    return Init_ObstacleBlock_left(msg_);
  }

private:
  ::sentinel_oda_msgs::msg::ObstacleBlock msg_;
};

class Init_ObstacleBlock_distance
{
public:
  Init_ObstacleBlock_distance()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ObstacleBlock_width distance(::sentinel_oda_msgs::msg::ObstacleBlock::_distance_type arg)
  {
    msg_.distance = std::move(arg);
    return Init_ObstacleBlock_width(msg_);
  }

private:
  ::sentinel_oda_msgs::msg::ObstacleBlock msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::sentinel_oda_msgs::msg::ObstacleBlock>()
{
  return sentinel_oda_msgs::msg::builder::Init_ObstacleBlock_distance();
}

}  // namespace sentinel_oda_msgs

#endif  // SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_BLOCK__BUILDER_HPP_
