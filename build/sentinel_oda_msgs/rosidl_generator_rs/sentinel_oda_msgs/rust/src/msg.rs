#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to sentinel_oda_msgs__msg__ObstacleInfo
/// Obstacle report from Detection node to Inner Map.
/// Published on every processed frame while an obstacle has been validated
/// (obstacles are NEVER cleared – validation is one-way until the drone
/// leaves mission/oda state).

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ObstacleInfo {
    /// All obstacle blocks currently in view (may be empty).  Width/left of each
    /// block are already inflated by box_margin on both sides, so consumers can
    /// mark tiles directly.
    pub blocks: Vec<super::msg::ObstacleBlock>,

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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ObstacleInfo::default())
  }
}

impl rosidl_runtime_rs::Message for ObstacleInfo {
  type RmwMsg = super::msg::rmw::ObstacleInfo;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        blocks: msg.blocks
          .into_iter()
          .map(|elem| super::msg::ObstacleBlock::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        closest_distance: msg.closest_distance,
        obstacle_width: msg.obstacle_width,
        current_heading: msg.current_heading,
        obstacle_left: msg.obstacle_left,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        blocks: msg.blocks
          .iter()
          .map(|elem| super::msg::ObstacleBlock::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      closest_distance: msg.closest_distance,
      obstacle_width: msg.obstacle_width,
      current_heading: msg.current_heading,
      obstacle_left: msg.obstacle_left,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      blocks: msg.blocks
          .into_iter()
          .map(super::msg::ObstacleBlock::from_rmw_message)
          .collect(),
      closest_distance: msg.closest_distance,
      obstacle_width: msg.obstacle_width,
      current_heading: msg.current_heading,
      obstacle_left: msg.obstacle_left,
    }
  }
}


// Corresponds to sentinel_oda_msgs__msg__ObstacleBlock
/// A single obstacle "block" as seen by the Detection node.
/// A block is a cluster of near-threshold depth pixels considered one
/// obstacle: clusters separated by a gap the drone could fly through
/// (>= drone_width + 2*box_margin) become separate blocks.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ObstacleBlock::default())
  }
}

impl rosidl_runtime_rs::Message for ObstacleBlock {
  type RmwMsg = super::msg::rmw::ObstacleBlock;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        distance: msg.distance,
        width: msg.width,
        left: msg.left,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      distance: msg.distance,
      width: msg.width,
      left: msg.left,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      distance: msg.distance,
      width: msg.width,
      left: msg.left,
    }
  }
}


