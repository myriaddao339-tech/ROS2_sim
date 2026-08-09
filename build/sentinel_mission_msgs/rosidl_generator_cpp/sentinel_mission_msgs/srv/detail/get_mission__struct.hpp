// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from sentinel_mission_msgs:srv/GetMission.idl
// generated code does not contain a copyright notice

#ifndef SENTINEL_MISSION_MSGS__SRV__DETAIL__GET_MISSION__STRUCT_HPP_
#define SENTINEL_MISSION_MSGS__SRV__DETAIL__GET_MISSION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__sentinel_mission_msgs__srv__GetMission_Request __attribute__((deprecated))
#else
# define DEPRECATED__sentinel_mission_msgs__srv__GetMission_Request __declspec(deprecated)
#endif

namespace sentinel_mission_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetMission_Request_
{
  using Type = GetMission_Request_<ContainerAllocator>;

  explicit GetMission_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->mission_file = "";
    }
  }

  explicit GetMission_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : mission_file(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->mission_file = "";
    }
  }

  // field types and members
  using _mission_file_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _mission_file_type mission_file;

  // setters for named parameter idiom
  Type & set__mission_file(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->mission_file = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    sentinel_mission_msgs::srv::GetMission_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const sentinel_mission_msgs::srv::GetMission_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<sentinel_mission_msgs::srv::GetMission_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<sentinel_mission_msgs::srv::GetMission_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      sentinel_mission_msgs::srv::GetMission_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<sentinel_mission_msgs::srv::GetMission_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      sentinel_mission_msgs::srv::GetMission_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<sentinel_mission_msgs::srv::GetMission_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<sentinel_mission_msgs::srv::GetMission_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<sentinel_mission_msgs::srv::GetMission_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__sentinel_mission_msgs__srv__GetMission_Request
    std::shared_ptr<sentinel_mission_msgs::srv::GetMission_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__sentinel_mission_msgs__srv__GetMission_Request
    std::shared_ptr<sentinel_mission_msgs::srv::GetMission_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetMission_Request_ & other) const
  {
    if (this->mission_file != other.mission_file) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetMission_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetMission_Request_

// alias to use template instance with default allocator
using GetMission_Request =
  sentinel_mission_msgs::srv::GetMission_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace sentinel_mission_msgs


// Include directives for member types
// Member 'waypoints'
#include "mavros_msgs/msg/detail/waypoint__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__sentinel_mission_msgs__srv__GetMission_Response __attribute__((deprecated))
#else
# define DEPRECATED__sentinel_mission_msgs__srv__GetMission_Response __declspec(deprecated)
#endif

namespace sentinel_mission_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetMission_Response_
{
  using Type = GetMission_Response_<ContainerAllocator>;

  explicit GetMission_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  explicit GetMission_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;
  using _waypoints_type =
    std::vector<mavros_msgs::msg::Waypoint_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<mavros_msgs::msg::Waypoint_<ContainerAllocator>>>;
  _waypoints_type waypoints;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }
  Type & set__waypoints(
    const std::vector<mavros_msgs::msg::Waypoint_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<mavros_msgs::msg::Waypoint_<ContainerAllocator>>> & _arg)
  {
    this->waypoints = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    sentinel_mission_msgs::srv::GetMission_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const sentinel_mission_msgs::srv::GetMission_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<sentinel_mission_msgs::srv::GetMission_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<sentinel_mission_msgs::srv::GetMission_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      sentinel_mission_msgs::srv::GetMission_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<sentinel_mission_msgs::srv::GetMission_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      sentinel_mission_msgs::srv::GetMission_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<sentinel_mission_msgs::srv::GetMission_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<sentinel_mission_msgs::srv::GetMission_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<sentinel_mission_msgs::srv::GetMission_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__sentinel_mission_msgs__srv__GetMission_Response
    std::shared_ptr<sentinel_mission_msgs::srv::GetMission_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__sentinel_mission_msgs__srv__GetMission_Response
    std::shared_ptr<sentinel_mission_msgs::srv::GetMission_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetMission_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    if (this->waypoints != other.waypoints) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetMission_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetMission_Response_

// alias to use template instance with default allocator
using GetMission_Response =
  sentinel_mission_msgs::srv::GetMission_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace sentinel_mission_msgs

namespace sentinel_mission_msgs
{

namespace srv
{

struct GetMission
{
  using Request = sentinel_mission_msgs::srv::GetMission_Request;
  using Response = sentinel_mission_msgs::srv::GetMission_Response;
};

}  // namespace srv

}  // namespace sentinel_mission_msgs

#endif  // SENTINEL_MISSION_MSGS__SRV__DETAIL__GET_MISSION__STRUCT_HPP_
