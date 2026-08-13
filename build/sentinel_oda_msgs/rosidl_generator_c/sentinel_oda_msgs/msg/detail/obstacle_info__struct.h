// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from sentinel_oda_msgs:msg/ObstacleInfo.idl
// generated code does not contain a copyright notice

#ifndef SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_INFO__STRUCT_H_
#define SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_INFO__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/ObstacleInfo in the package sentinel_oda_msgs.
/**
  * Obstacle report from Detection node to Inner Map.
  * Published every time the depth model confirms an obstacle in view.
 */
typedef struct sentinel_oda_msgs__msg__ObstacleInfo
{
  /// Closest distance to the obstacle (metres), measured along the drone's
  /// forward axis from the depth map.
  float closest_distance;
  /// Horizontal width of the detected obstacle (metres).
  float obstacle_width;
  /// Drone's current yaw heading (radians, 0 = North, positive = East) at the
  /// moment the frame was captured.  Sourced from /mavros/local_position/pose.
  float current_heading;
  /// Horizontal offset of the left edge of the obstacle's bounding box from the
  /// drone's forward axis (metres, negative = left).
  float obstacle_left;
} sentinel_oda_msgs__msg__ObstacleInfo;

// Struct for a sequence of sentinel_oda_msgs__msg__ObstacleInfo.
typedef struct sentinel_oda_msgs__msg__ObstacleInfo__Sequence
{
  sentinel_oda_msgs__msg__ObstacleInfo * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} sentinel_oda_msgs__msg__ObstacleInfo__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_INFO__STRUCT_H_
