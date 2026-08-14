#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "sentinel_oda_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__sentinel_oda_msgs__msg__ObstacleInfo() -> *const std::ffi::c_void;
}

#[link(name = "sentinel_oda_msgs__rosidl_generator_c")]
extern "C" {
    fn sentinel_oda_msgs__msg__ObstacleInfo__init(msg: *mut ObstacleInfo) -> bool;
    fn sentinel_oda_msgs__msg__ObstacleInfo__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ObstacleInfo>, size: usize) -> bool;
    fn sentinel_oda_msgs__msg__ObstacleInfo__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ObstacleInfo>);
    fn sentinel_oda_msgs__msg__ObstacleInfo__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ObstacleInfo>, out_seq: *mut rosidl_runtime_rs::Sequence<ObstacleInfo>) -> bool;
}

// Corresponds to sentinel_oda_msgs__msg__ObstacleInfo
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Obstacle report from Detection node to Inner Map.
/// Published on every processed frame while an obstacle has been validated
/// (obstacles are NEVER cleared – validation is one-way until the drone
/// leaves mission/oda state).

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ObstacleInfo {
    /// All obstacle blocks currently in view (may be empty).  Width/left of each
    /// block are already inflated by box_margin on both sides, so consumers can
    /// mark tiles directly.
    pub blocks: rosidl_runtime_rs::Sequence<super::super::msg::rmw::ObstacleBlock>,

    /// Legacy single-obstacle fields – mirror the closest block (or 0.0 when no
    /// block is in view).  Kept for compatibility with earlier subscribers.
    /// Median-smoothed distance to the closest point of the closest block (m).
    pub closest_distance: f32,

    /// Horizontal width of the closest block (metres, margin-inflated).
    pub obstacle_width: f32,

    /// Drone's current yaw heading (radians, 0 = North, positive = East) at the
    /// moment the frame was captured.  Sourced from /mavros/local_position/pose.
    pub current_heading: f32,

    /// Horizontal offset of the left edge of the closest block from the drone's
    /// forward axis (metres, negative = left, margin-inflated).
    pub obstacle_left: f32,

}



impl Default for ObstacleInfo {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !sentinel_oda_msgs__msg__ObstacleInfo__init(&mut msg as *mut _) {
        panic!("Call to sentinel_oda_msgs__msg__ObstacleInfo__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ObstacleInfo {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { sentinel_oda_msgs__msg__ObstacleInfo__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { sentinel_oda_msgs__msg__ObstacleInfo__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { sentinel_oda_msgs__msg__ObstacleInfo__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ObstacleInfo {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ObstacleInfo where Self: Sized {
  const TYPE_NAME: &'static str = "sentinel_oda_msgs/msg/ObstacleInfo";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__sentinel_oda_msgs__msg__ObstacleInfo() }
  }
}


#[link(name = "sentinel_oda_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__sentinel_oda_msgs__msg__ObstacleBlock() -> *const std::ffi::c_void;
}

#[link(name = "sentinel_oda_msgs__rosidl_generator_c")]
extern "C" {
    fn sentinel_oda_msgs__msg__ObstacleBlock__init(msg: *mut ObstacleBlock) -> bool;
    fn sentinel_oda_msgs__msg__ObstacleBlock__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ObstacleBlock>, size: usize) -> bool;
    fn sentinel_oda_msgs__msg__ObstacleBlock__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ObstacleBlock>);
    fn sentinel_oda_msgs__msg__ObstacleBlock__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ObstacleBlock>, out_seq: *mut rosidl_runtime_rs::Sequence<ObstacleBlock>) -> bool;
}

// Corresponds to sentinel_oda_msgs__msg__ObstacleBlock
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// A single obstacle "block" as seen by the Detection node.
/// A block is a cluster of near-threshold depth pixels considered one
/// obstacle: clusters separated by a gap the drone could fly through
/// (>= drone_width + 2*box_margin) become separate blocks.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ObstacleBlock {
    /// Distance to the closest point of the block (metres, along the camera axis).
    pub distance: f32,

    /// Horizontal extent of the block (metres), already inflated by box_margin
    /// on both sides: every tile in [left, left + width] must be marked dangerous.
    pub width: f32,

    /// Horizontal offset of the margin-inflated left edge from the camera
    /// forward axis (metres, negative = left).
    pub left: f32,

}



impl Default for ObstacleBlock {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !sentinel_oda_msgs__msg__ObstacleBlock__init(&mut msg as *mut _) {
        panic!("Call to sentinel_oda_msgs__msg__ObstacleBlock__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ObstacleBlock {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { sentinel_oda_msgs__msg__ObstacleBlock__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { sentinel_oda_msgs__msg__ObstacleBlock__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { sentinel_oda_msgs__msg__ObstacleBlock__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ObstacleBlock {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ObstacleBlock where Self: Sized {
  const TYPE_NAME: &'static str = "sentinel_oda_msgs/msg/ObstacleBlock";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__sentinel_oda_msgs__msg__ObstacleBlock() }
  }
}


