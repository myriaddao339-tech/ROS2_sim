// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from sentinel_mission_msgs:srv/GetMission.idl
// generated code does not contain a copyright notice
#include "sentinel_mission_msgs/srv/detail/get_mission__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `mission_file`
#include "rosidl_runtime_c/string_functions.h"

bool
sentinel_mission_msgs__srv__GetMission_Request__init(sentinel_mission_msgs__srv__GetMission_Request * msg)
{
  if (!msg) {
    return false;
  }
  // mission_file
  if (!rosidl_runtime_c__String__init(&msg->mission_file)) {
    sentinel_mission_msgs__srv__GetMission_Request__fini(msg);
    return false;
  }
  return true;
}

void
sentinel_mission_msgs__srv__GetMission_Request__fini(sentinel_mission_msgs__srv__GetMission_Request * msg)
{
  if (!msg) {
    return;
  }
  // mission_file
  rosidl_runtime_c__String__fini(&msg->mission_file);
}

bool
sentinel_mission_msgs__srv__GetMission_Request__are_equal(const sentinel_mission_msgs__srv__GetMission_Request * lhs, const sentinel_mission_msgs__srv__GetMission_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // mission_file
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->mission_file), &(rhs->mission_file)))
  {
    return false;
  }
  return true;
}

bool
sentinel_mission_msgs__srv__GetMission_Request__copy(
  const sentinel_mission_msgs__srv__GetMission_Request * input,
  sentinel_mission_msgs__srv__GetMission_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // mission_file
  if (!rosidl_runtime_c__String__copy(
      &(input->mission_file), &(output->mission_file)))
  {
    return false;
  }
  return true;
}

sentinel_mission_msgs__srv__GetMission_Request *
sentinel_mission_msgs__srv__GetMission_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  sentinel_mission_msgs__srv__GetMission_Request * msg = (sentinel_mission_msgs__srv__GetMission_Request *)allocator.allocate(sizeof(sentinel_mission_msgs__srv__GetMission_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(sentinel_mission_msgs__srv__GetMission_Request));
  bool success = sentinel_mission_msgs__srv__GetMission_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
sentinel_mission_msgs__srv__GetMission_Request__destroy(sentinel_mission_msgs__srv__GetMission_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    sentinel_mission_msgs__srv__GetMission_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
sentinel_mission_msgs__srv__GetMission_Request__Sequence__init(sentinel_mission_msgs__srv__GetMission_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  sentinel_mission_msgs__srv__GetMission_Request * data = NULL;

  if (size) {
    data = (sentinel_mission_msgs__srv__GetMission_Request *)allocator.zero_allocate(size, sizeof(sentinel_mission_msgs__srv__GetMission_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = sentinel_mission_msgs__srv__GetMission_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        sentinel_mission_msgs__srv__GetMission_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
sentinel_mission_msgs__srv__GetMission_Request__Sequence__fini(sentinel_mission_msgs__srv__GetMission_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      sentinel_mission_msgs__srv__GetMission_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

sentinel_mission_msgs__srv__GetMission_Request__Sequence *
sentinel_mission_msgs__srv__GetMission_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  sentinel_mission_msgs__srv__GetMission_Request__Sequence * array = (sentinel_mission_msgs__srv__GetMission_Request__Sequence *)allocator.allocate(sizeof(sentinel_mission_msgs__srv__GetMission_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = sentinel_mission_msgs__srv__GetMission_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
sentinel_mission_msgs__srv__GetMission_Request__Sequence__destroy(sentinel_mission_msgs__srv__GetMission_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    sentinel_mission_msgs__srv__GetMission_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
sentinel_mission_msgs__srv__GetMission_Request__Sequence__are_equal(const sentinel_mission_msgs__srv__GetMission_Request__Sequence * lhs, const sentinel_mission_msgs__srv__GetMission_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!sentinel_mission_msgs__srv__GetMission_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
sentinel_mission_msgs__srv__GetMission_Request__Sequence__copy(
  const sentinel_mission_msgs__srv__GetMission_Request__Sequence * input,
  sentinel_mission_msgs__srv__GetMission_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(sentinel_mission_msgs__srv__GetMission_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    sentinel_mission_msgs__srv__GetMission_Request * data =
      (sentinel_mission_msgs__srv__GetMission_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!sentinel_mission_msgs__srv__GetMission_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          sentinel_mission_msgs__srv__GetMission_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!sentinel_mission_msgs__srv__GetMission_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"
// Member `waypoints`
#include "mavros_msgs/msg/detail/waypoint__functions.h"

bool
sentinel_mission_msgs__srv__GetMission_Response__init(sentinel_mission_msgs__srv__GetMission_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    sentinel_mission_msgs__srv__GetMission_Response__fini(msg);
    return false;
  }
  // waypoints
  if (!mavros_msgs__msg__Waypoint__Sequence__init(&msg->waypoints, 0)) {
    sentinel_mission_msgs__srv__GetMission_Response__fini(msg);
    return false;
  }
  return true;
}

void
sentinel_mission_msgs__srv__GetMission_Response__fini(sentinel_mission_msgs__srv__GetMission_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
  // message
  rosidl_runtime_c__String__fini(&msg->message);
  // waypoints
  mavros_msgs__msg__Waypoint__Sequence__fini(&msg->waypoints);
}

bool
sentinel_mission_msgs__srv__GetMission_Response__are_equal(const sentinel_mission_msgs__srv__GetMission_Response * lhs, const sentinel_mission_msgs__srv__GetMission_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  // waypoints
  if (!mavros_msgs__msg__Waypoint__Sequence__are_equal(
      &(lhs->waypoints), &(rhs->waypoints)))
  {
    return false;
  }
  return true;
}

bool
sentinel_mission_msgs__srv__GetMission_Response__copy(
  const sentinel_mission_msgs__srv__GetMission_Response * input,
  sentinel_mission_msgs__srv__GetMission_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  // waypoints
  if (!mavros_msgs__msg__Waypoint__Sequence__copy(
      &(input->waypoints), &(output->waypoints)))
  {
    return false;
  }
  return true;
}

sentinel_mission_msgs__srv__GetMission_Response *
sentinel_mission_msgs__srv__GetMission_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  sentinel_mission_msgs__srv__GetMission_Response * msg = (sentinel_mission_msgs__srv__GetMission_Response *)allocator.allocate(sizeof(sentinel_mission_msgs__srv__GetMission_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(sentinel_mission_msgs__srv__GetMission_Response));
  bool success = sentinel_mission_msgs__srv__GetMission_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
sentinel_mission_msgs__srv__GetMission_Response__destroy(sentinel_mission_msgs__srv__GetMission_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    sentinel_mission_msgs__srv__GetMission_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
sentinel_mission_msgs__srv__GetMission_Response__Sequence__init(sentinel_mission_msgs__srv__GetMission_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  sentinel_mission_msgs__srv__GetMission_Response * data = NULL;

  if (size) {
    data = (sentinel_mission_msgs__srv__GetMission_Response *)allocator.zero_allocate(size, sizeof(sentinel_mission_msgs__srv__GetMission_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = sentinel_mission_msgs__srv__GetMission_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        sentinel_mission_msgs__srv__GetMission_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
sentinel_mission_msgs__srv__GetMission_Response__Sequence__fini(sentinel_mission_msgs__srv__GetMission_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      sentinel_mission_msgs__srv__GetMission_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

sentinel_mission_msgs__srv__GetMission_Response__Sequence *
sentinel_mission_msgs__srv__GetMission_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  sentinel_mission_msgs__srv__GetMission_Response__Sequence * array = (sentinel_mission_msgs__srv__GetMission_Response__Sequence *)allocator.allocate(sizeof(sentinel_mission_msgs__srv__GetMission_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = sentinel_mission_msgs__srv__GetMission_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
sentinel_mission_msgs__srv__GetMission_Response__Sequence__destroy(sentinel_mission_msgs__srv__GetMission_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    sentinel_mission_msgs__srv__GetMission_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
sentinel_mission_msgs__srv__GetMission_Response__Sequence__are_equal(const sentinel_mission_msgs__srv__GetMission_Response__Sequence * lhs, const sentinel_mission_msgs__srv__GetMission_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!sentinel_mission_msgs__srv__GetMission_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
sentinel_mission_msgs__srv__GetMission_Response__Sequence__copy(
  const sentinel_mission_msgs__srv__GetMission_Response__Sequence * input,
  sentinel_mission_msgs__srv__GetMission_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(sentinel_mission_msgs__srv__GetMission_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    sentinel_mission_msgs__srv__GetMission_Response * data =
      (sentinel_mission_msgs__srv__GetMission_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!sentinel_mission_msgs__srv__GetMission_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          sentinel_mission_msgs__srv__GetMission_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!sentinel_mission_msgs__srv__GetMission_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
