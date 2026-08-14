// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from sentinel_oda_msgs:msg/ObstacleBlock.idl
// generated code does not contain a copyright notice

#ifndef SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_BLOCK__STRUCT_H_
#define SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_BLOCK__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/ObstacleBlock in the package sentinel_oda_msgs.
/**
  * A single obstacle "block" as seen by the Detection node.
  * A block is a cluster of near-threshold depth pixels considered one
  * obstacle: clusters separated by a gap the drone could fly through
  * (>= drone_width + 2*box_margin) become separate blocks.
 */
typedef struct sentinel_oda_msgs__msg__ObstacleBlock
{
  /// Distance to the closest point of the block (metres, along the camera axis).
  float distance;
  /// Horizontal extent of the block (metres), already inflated by box_margin
  /// on both sides: every tile in [left, left + width] must be marked dangerous.
  float width;
  /// Horizontal offset of the margin-inflated left edge from the camera
  /// forward axis (metres, negative = left).
  float left;
} sentinel_oda_msgs__msg__ObstacleBlock;

// Struct for a sequence of sentinel_oda_msgs__msg__ObstacleBlock.
typedef struct sentinel_oda_msgs__msg__ObstacleBlock__Sequence
{
  sentinel_oda_msgs__msg__ObstacleBlock * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} sentinel_oda_msgs__msg__ObstacleBlock__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SENTINEL_ODA_MSGS__MSG__DETAIL__OBSTACLE_BLOCK__STRUCT_H_
