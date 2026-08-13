// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from sentinel_oda_msgs:msg/ObstacleInfo.idl
// generated code does not contain a copyright notice

#ifndef SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_INFO__STRUCT_HPP_
#define SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_INFO__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__sentinel_oda_msgs__msg__ObstacleInfo __attribute__((deprecated))
#else
# define DEPRECATED__sentinel_oda_msgs__msg__ObstacleInfo __declspec(deprecated)
#endif

namespace sentinel_oda_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ObstacleInfo_
{
  using Type = ObstacleInfo_<ContainerAllocator>;

  explicit ObstacleInfo_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->closest_distance = 0.0f;
      this->obstacle_width = 0.0f;
      this->current_heading = 0.0f;
      this->obstacle_left = 0.0f;
    }
  }

  explicit ObstacleInfo_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->closest_distance = 0.0f;
      this->obstacle_width = 0.0f;
      this->current_heading = 0.0f;
      this->obstacle_left = 0.0f;
    }
  }

  // field types and members
  using _closest_distance_type =
    float;
  _closest_distance_type closest_distance;
  using _obstacle_width_type =
    float;
  _obstacle_width_type obstacle_width;
  using _current_heading_type =
    float;
  _current_heading_type current_heading;
  using _obstacle_left_type =
    float;
  _obstacle_left_type obstacle_left;

  // setters for named parameter idiom
  Type & set__closest_distance(
    const float & _arg)
  {
    this->closest_distance = _arg;
    return *this;
  }
  Type & set__obstacle_width(
    const float & _arg)
  {
    this->obstacle_width = _arg;
    return *this;
  }
  Type & set__current_heading(
    const float & _arg)
  {
    this->current_heading = _arg;
    return *this;
  }
  Type & set__obstacle_left(
    const float & _arg)
  {
    this->obstacle_left = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    sentinel_oda_msgs::msg::ObstacleInfo_<ContainerAllocator> *;
  using ConstRawPtr =
    const sentinel_oda_msgs::msg::ObstacleInfo_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<sentinel_oda_msgs::msg::ObstacleInfo_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<sentinel_oda_msgs::msg::ObstacleInfo_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      sentinel_oda_msgs::msg::ObstacleInfo_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<sentinel_oda_msgs::msg::ObstacleInfo_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      sentinel_oda_msgs::msg::ObstacleInfo_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<sentinel_oda_msgs::msg::ObstacleInfo_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<sentinel_oda_msgs::msg::ObstacleInfo_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<sentinel_oda_msgs::msg::ObstacleInfo_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__sentinel_oda_msgs__msg__ObstacleInfo
    std::shared_ptr<sentinel_oda_msgs::msg::ObstacleInfo_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__sentinel_oda_msgs__msg__ObstacleInfo
    std::shared_ptr<sentinel_oda_msgs::msg::ObstacleInfo_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ObstacleInfo_ & other) const
  {
    if (this->closest_distance != other.closest_distance) {
      return false;
    }
    if (this->obstacle_width != other.obstacle_width) {
      return false;
    }
    if (this->current_heading != other.current_heading) {
      return false;
    }
    if (this->obstacle_left != other.obstacle_left) {
      return false;
    }
    return true;
  }
  bool operator!=(const ObstacleInfo_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ObstacleInfo_

// alias to use template instance with default allocator
using ObstacleInfo =
  sentinel_oda_msgs::msg::ObstacleInfo_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace sentinel_oda_msgs

#endif  // SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_INFO__STRUCT_HPP_
