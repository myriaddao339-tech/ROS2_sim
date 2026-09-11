// NOLINT: This file starts with a BOM since it contain non-ASCII characters
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

// Include directives for member types
// Member 'blocks'
#include "sentinel_oda_msgs/msg/detail/obstacle_block__struct.h"

/// Struct defined in msg/ObstacleInfo in the package sentinel_oda_msgs.
/**
  * Obstacle report from Detection node to Inner Map.
  * Published on every processed frame while an obstacle has been validated
  * (obstacles are NEVER cleared – validation is one-way until the drone
  * leaves mission/oda state).
 */
typedef struct sentinel_oda_msgs__msg__ObstacleInfo
{
  /// All obstacle blocks currently in view (may be empty).  Width/left of each
  /// block are already inflated by box_margin on both sides, so consumers can
  /// mark tiles directly.
  sentinel_oda_msgs__msg__ObstacleBlock__Sequence blocks;
  /// Legacy single-obstacle fields – mirror the closest block (or 0.0 when no
  /// block is in view).  Kept for compatibility with earlier subscribers.
  /// Median-smoothed distance to the closest point of the closest block (m).
  float closest_distance;
  /// Horizontal width of the closest block (metres, margin-inflated).
  float obstacle_width;
  /// Drone's current yaw heading (radians, ENU convention: 0 = East,
  /// positive = counterclockwise toward North) at the moment the frame was
  /// captured.  Sourced from /mavros/local_position/pose.
  float current_heading;
  /// Horizontal offset of the left edge of the closest block from the drone's
  /// forward axis (metres, negative = left, margin-inflated).
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
