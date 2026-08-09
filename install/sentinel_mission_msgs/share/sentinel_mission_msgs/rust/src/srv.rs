#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to sentinel_mission_msgs__srv__GetMission_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetMission_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub mission_file: std::string::String,

}



impl Default for GetMission_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetMission_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetMission_Request {
  type RmwMsg = super::srv::rmw::GetMission_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        mission_file: msg.mission_file.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        mission_file: msg.mission_file.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      mission_file: msg.mission_file.to_string(),
    }
  }
}


// Corresponds to sentinel_mission_msgs__srv__GetMission_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetMission_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub waypoints: Vec<mavros_msgs::msg::Waypoint>,

}



impl Default for GetMission_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetMission_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetMission_Response {
  type RmwMsg = super::srv::rmw::GetMission_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
        waypoints: msg.waypoints
          .into_iter()
          .map(|elem| mavros_msgs::msg::Waypoint::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
        waypoints: msg.waypoints
          .iter()
          .map(|elem| mavros_msgs::msg::Waypoint::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
      waypoints: msg.waypoints
          .into_iter()
          .map(mavros_msgs::msg::Waypoint::from_rmw_message)
          .collect(),
    }
  }
}






#[link(name = "sentinel_mission_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__sentinel_mission_msgs__srv__GetMission() -> *const std::ffi::c_void;
}

// Corresponds to sentinel_mission_msgs__srv__GetMission
#[allow(missing_docs, non_camel_case_types)]
pub struct GetMission;

impl rosidl_runtime_rs::Service for GetMission {
    type Request = GetMission_Request;
    type Response = GetMission_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__sentinel_mission_msgs__srv__GetMission() }
    }
}


