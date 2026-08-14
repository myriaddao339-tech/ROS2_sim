// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from sentinel_oda_msgs:msg/ObstacleBlock.idl
// generated code does not contain a copyright notice

#ifndef SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_BLOCK__STRUCT_HPP_
#define SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_BLOCK__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__sentinel_oda_msgs__msg__ObstacleBlock __attribute__((deprecated))
#else
# define DEPRECATED__sentinel_oda_msgs__msg__ObstacleBlock __declspec(deprecated)
#endif

namespace sentinel_oda_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ObstacleBlock_
{
  using Type = ObstacleBlock_<ContainerAllocator>;

  explicit ObstacleBlock_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->distance = 0.0f;
      this->width = 0.0f;
      this->left = 0.0f;
    }
  }

  explicit ObstacleBlock_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->distance = 0.0f;
      this->width = 0.0f;
      this->left = 0.0f;
    }
  }

  // field types and members
  using _distance_type =
    float;
  _distance_type distance;
  using _width_type =
    float;
  _width_type width;
  using _left_type =
    float;
  _left_type left;

  // setters for named parameter idiom
  Type & set__distance(
    const float & _arg)
  {
    this->distance = _arg;
    return *this;
  }
  Type & set__width(
    const float & _arg)
  {
    this->width = _arg;
    return *this;
  }
  Type & set__left(
    const float & _arg)
  {
    this->left = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    sentinel_oda_msgs::msg::ObstacleBlock_<ContainerAllocator> *;
  using ConstRawPtr =
    const sentinel_oda_msgs::msg::ObstacleBlock_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<sentinel_oda_msgs::msg::ObstacleBlock_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<sentinel_oda_msgs::msg::ObstacleBlock_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      sentinel_oda_msgs::msg::ObstacleBlock_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<sentinel_oda_msgs::msg::ObstacleBlock_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      sentinel_oda_msgs::msg::ObstacleBlock_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<sentinel_oda_msgs::msg::ObstacleBlock_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<sentinel_oda_msgs::msg::ObstacleBlock_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<sentinel_oda_msgs::msg::ObstacleBlock_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__sentinel_oda_msgs__msg__ObstacleBlock
    std::shared_ptr<sentinel_oda_msgs::msg::ObstacleBlock_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__sentinel_oda_msgs__msg__ObstacleBlock
    std::shared_ptr<sentinel_oda_msgs::msg::ObstacleBlock_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ObstacleBlock_ & other) const
  {
    if (this->distance != other.distance) {
      return false;
    }
    if (this->width != other.width) {
      return false;
    }
    if (this->left != other.left) {
      return false;
    }
    return true;
  }
  bool operator!=(const ObstacleBlock_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ObstacleBlock_

// alias to use template instance with default allocator
using ObstacleBlock =
  sentinel_oda_msgs::msg::ObstacleBlock_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace sentinel_oda_msgs

#endif  // SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_BLOCK__STRUCT_HPP_
