#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to sentinel_oda_msgs__msg__ObstacleInfo
/// Obstacle report from Detection node to Inner Map.
/// Published every time the depth model confirms an obstacle in view.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ObstacleInfo::default())
  }
}

impl rosidl_runtime_rs::Message for ObstacleInfo {
  type RmwMsg = super::msg::rmw::ObstacleInfo;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        closest_distance: msg.closest_distance,
        obstacle_width: msg.obstacle_width,
        current_heading: msg.current_heading,
        obstacle_left: msg.obstacle_left,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      closest_distance: msg.closest_distance,
      obstacle_width: msg.obstacle_width,
      current_heading: msg.current_heading,
      obstacle_left: msg.obstacle_left,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      closest_distance: msg.closest_distance,
      obstacle_width: msg.obstacle_width,
      current_heading: msg.current_heading,
      obstacle_left: msg.obstacle_left,
    }
  }
}


