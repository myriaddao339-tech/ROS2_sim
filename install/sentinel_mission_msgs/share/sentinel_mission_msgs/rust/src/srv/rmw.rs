#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "sentinel_mission_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__sentinel_mission_msgs__srv__GetMission_Request() -> *const std::ffi::c_void;
}

#[link(name = "sentinel_mission_msgs__rosidl_generator_c")]
extern "C" {
    fn sentinel_mission_msgs__srv__GetMission_Request__init(msg: *mut GetMission_Request) -> bool;
    fn sentinel_mission_msgs__srv__GetMission_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetMission_Request>, size: usize) -> bool;
    fn sentinel_mission_msgs__srv__GetMission_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetMission_Request>);
    fn sentinel_mission_msgs__srv__GetMission_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetMission_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetMission_Request>) -> bool;
}

// Corresponds to sentinel_mission_msgs__srv__GetMission_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetMission_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub mission_file: rosidl_runtime_rs::String,

}



impl Default for GetMission_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !sentinel_mission_msgs__srv__GetMission_Request__init(&mut msg as *mut _) {
        panic!("Call to sentinel_mission_msgs__srv__GetMission_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetMission_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { sentinel_mission_msgs__srv__GetMission_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { sentinel_mission_msgs__srv__GetMission_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { sentinel_mission_msgs__srv__GetMission_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetMission_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetMission_Request where Self: Sized {
  const TYPE_NAME: &'static str = "sentinel_mission_msgs/srv/GetMission_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__sentinel_mission_msgs__srv__GetMission_Request() }
  }
}


#[link(name = "sentinel_mission_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__sentinel_mission_msgs__srv__GetMission_Response() -> *const std::ffi::c_void;
}

#[link(name = "sentinel_mission_msgs__rosidl_generator_c")]
extern "C" {
    fn sentinel_mission_msgs__srv__GetMission_Response__init(msg: *mut GetMission_Response) -> bool;
    fn sentinel_mission_msgs__srv__GetMission_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetMission_Response>, size: usize) -> bool;
    fn sentinel_mission_msgs__srv__GetMission_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetMission_Response>);
    fn sentinel_mission_msgs__srv__GetMission_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetMission_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetMission_Response>) -> bool;
}

// Corresponds to sentinel_mission_msgs__srv__GetMission_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetMission_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub waypoints: rosidl_runtime_rs::Sequence<mavros_msgs::msg::rmw::Waypoint>,

}



impl Default for GetMission_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !sentinel_mission_msgs__srv__GetMission_Response__init(&mut msg as *mut _) {
        panic!("Call to sentinel_mission_msgs__srv__GetMission_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetMission_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { sentinel_mission_msgs__srv__GetMission_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { sentinel_mission_msgs__srv__GetMission_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { sentinel_mission_msgs__srv__GetMission_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetMission_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetMission_Response where Self: Sized {
  const TYPE_NAME: &'static str = "sentinel_mission_msgs/srv/GetMission_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__sentinel_mission_msgs__srv__GetMission_Response() }
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


