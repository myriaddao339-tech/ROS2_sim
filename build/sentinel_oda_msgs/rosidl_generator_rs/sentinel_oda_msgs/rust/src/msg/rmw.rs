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
/// Published every time the depth model confirms an obstacle in view.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ObstacleInfo {
    /// Closest distance to the obstacle (metres), measured along the drone's
    /// forward axis from the depth map.
    pub closest_distance: f32,

    /// Horizontal width of the detected obstacle (metres).
    pub obstacle_width: f32,

    /// Drone's current yaw heading (radians, 0 = North, positive = East) at the
    /// moment the frame was captured.  Sourced from /mavros/local_position/pose.
    pub current_heading: f32,

    /// Horizontal offset of the left edge of the obstacle's bounding box from the
    /// drone's forward axis (metres, negative = left).
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


