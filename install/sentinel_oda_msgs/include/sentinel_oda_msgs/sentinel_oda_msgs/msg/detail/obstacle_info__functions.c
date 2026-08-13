// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from sentinel_oda_msgs:msg/ObstacleInfo.idl
// generated code does not contain a copyright notice
#include "sentinel_oda_msgs/msg/detail/obstacle_info__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
sentinel_oda_msgs__msg__ObstacleInfo__init(sentinel_oda_msgs__msg__ObstacleInfo * msg)
{
  if (!msg) {
    return false;
  }
  // closest_distance
  // obstacle_width
  // current_heading
  // obstacle_left
  return true;
}

void
sentinel_oda_msgs__msg__ObstacleInfo__fini(sentinel_oda_msgs__msg__ObstacleInfo * msg)
{
  if (!msg) {
    return;
  }
  // closest_distance
  // obstacle_width
  // current_heading
  // obstacle_left
}

bool
sentinel_oda_msgs__msg__ObstacleInfo__are_equal(const sentinel_oda_msgs__msg__ObstacleInfo * lhs, const sentinel_oda_msgs__msg__ObstacleInfo * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // closest_distance
  if (lhs->closest_distance != rhs->closest_distance) {
    return false;
  }
  // obstacle_width
  if (lhs->obstacle_width != rhs->obstacle_width) {
    return false;
  }
  // current_heading
  if (lhs->current_heading != rhs->current_heading) {
    return false;
  }
  // obstacle_left
  if (lhs->obstacle_left != rhs->obstacle_left) {
    return false;
  }
  return true;
}

bool
sentinel_oda_msgs__msg__ObstacleInfo__copy(
  const sentinel_oda_msgs__msg__ObstacleInfo * input,
  sentinel_oda_msgs__msg__ObstacleInfo * output)
{
  if (!input || !output) {
    return false;
  }
  // closest_distance
  output->closest_distance = input->closest_distance;
  // obstacle_width
  output->obstacle_width = input->obstacle_width;
  // current_heading
  output->current_heading = input->current_heading;
  // obstacle_left
  output->obstacle_left = input->obstacle_left;
  return true;
}

sentinel_oda_msgs__msg__ObstacleInfo *
sentinel_oda_msgs__msg__ObstacleInfo__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  sentinel_oda_msgs__msg__ObstacleInfo * msg = (sentinel_oda_msgs__msg__ObstacleInfo *)allocator.allocate(sizeof(sentinel_oda_msgs__msg__ObstacleInfo), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(sentinel_oda_msgs__msg__ObstacleInfo));
  bool success = sentinel_oda_msgs__msg__ObstacleInfo__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
sentinel_oda_msgs__msg__ObstacleInfo__destroy(sentinel_oda_msgs__msg__ObstacleInfo * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    sentinel_oda_msgs__msg__ObstacleInfo__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
sentinel_oda_msgs__msg__ObstacleInfo__Sequence__init(sentinel_oda_msgs__msg__ObstacleInfo__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  sentinel_oda_msgs__msg__ObstacleInfo * data = NULL;

  if (size) {
    data = (sentinel_oda_msgs__msg__ObstacleInfo *)allocator.zero_allocate(size, sizeof(sentinel_oda_msgs__msg__ObstacleInfo), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = sentinel_oda_msgs__msg__ObstacleInfo__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        sentinel_oda_msgs__msg__ObstacleInfo__fini(&data[i - 1]);
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
sentinel_oda_msgs__msg__ObstacleInfo__Sequence__fini(sentinel_oda_msgs__msg__ObstacleInfo__Sequence * array)
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
      sentinel_oda_msgs__msg__ObstacleInfo__fini(&array->data[i]);
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

sentinel_oda_msgs__msg__ObstacleInfo__Sequence *
sentinel_oda_msgs__msg__ObstacleInfo__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  sentinel_oda_msgs__msg__ObstacleInfo__Sequence * array = (sentinel_oda_msgs__msg__ObstacleInfo__Sequence *)allocator.allocate(sizeof(sentinel_oda_msgs__msg__ObstacleInfo__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = sentinel_oda_msgs__msg__ObstacleInfo__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
sentinel_oda_msgs__msg__ObstacleInfo__Sequence__destroy(sentinel_oda_msgs__msg__ObstacleInfo__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    sentinel_oda_msgs__msg__ObstacleInfo__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
sentinel_oda_msgs__msg__ObstacleInfo__Sequence__are_equal(const sentinel_oda_msgs__msg__ObstacleInfo__Sequence * lhs, const sentinel_oda_msgs__msg__ObstacleInfo__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!sentinel_oda_msgs__msg__ObstacleInfo__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
sentinel_oda_msgs__msg__ObstacleInfo__Sequence__copy(
  const sentinel_oda_msgs__msg__ObstacleInfo__Sequence * input,
  sentinel_oda_msgs__msg__ObstacleInfo__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(sentinel_oda_msgs__msg__ObstacleInfo);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    sentinel_oda_msgs__msg__ObstacleInfo * data =
      (sentinel_oda_msgs__msg__ObstacleInfo *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!sentinel_oda_msgs__msg__ObstacleInfo__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          sentinel_oda_msgs__msg__ObstacleInfo__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!sentinel_oda_msgs__msg__ObstacleInfo__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
