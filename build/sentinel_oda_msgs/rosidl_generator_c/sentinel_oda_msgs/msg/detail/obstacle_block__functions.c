// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from sentinel_oda_msgs:msg/ObstacleBlock.idl
// generated code does not contain a copyright notice
#include "sentinel_oda_msgs/msg/detail/obstacle_block__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
sentinel_oda_msgs__msg__ObstacleBlock__init(sentinel_oda_msgs__msg__ObstacleBlock * msg)
{
  if (!msg) {
    return false;
  }
  // distance
  // width
  // left
  return true;
}

void
sentinel_oda_msgs__msg__ObstacleBlock__fini(sentinel_oda_msgs__msg__ObstacleBlock * msg)
{
  if (!msg) {
    return;
  }
  // distance
  // width
  // left
}

bool
sentinel_oda_msgs__msg__ObstacleBlock__are_equal(const sentinel_oda_msgs__msg__ObstacleBlock * lhs, const sentinel_oda_msgs__msg__ObstacleBlock * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // distance
  if (lhs->distance != rhs->distance) {
    return false;
  }
  // width
  if (lhs->width != rhs->width) {
    return false;
  }
  // left
  if (lhs->left != rhs->left) {
    return false;
  }
  return true;
}

bool
sentinel_oda_msgs__msg__ObstacleBlock__copy(
  const sentinel_oda_msgs__msg__ObstacleBlock * input,
  sentinel_oda_msgs__msg__ObstacleBlock * output)
{
  if (!input || !output) {
    return false;
  }
  // distance
  output->distance = input->distance;
  // width
  output->width = input->width;
  // left
  output->left = input->left;
  return true;
}

sentinel_oda_msgs__msg__ObstacleBlock *
sentinel_oda_msgs__msg__ObstacleBlock__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  sentinel_oda_msgs__msg__ObstacleBlock * msg = (sentinel_oda_msgs__msg__ObstacleBlock *)allocator.allocate(sizeof(sentinel_oda_msgs__msg__ObstacleBlock), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(sentinel_oda_msgs__msg__ObstacleBlock));
  bool success = sentinel_oda_msgs__msg__ObstacleBlock__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
sentinel_oda_msgs__msg__ObstacleBlock__destroy(sentinel_oda_msgs__msg__ObstacleBlock * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    sentinel_oda_msgs__msg__ObstacleBlock__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
sentinel_oda_msgs__msg__ObstacleBlock__Sequence__init(sentinel_oda_msgs__msg__ObstacleBlock__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  sentinel_oda_msgs__msg__ObstacleBlock * data = NULL;

  if (size) {
    data = (sentinel_oda_msgs__msg__ObstacleBlock *)allocator.zero_allocate(size, sizeof(sentinel_oda_msgs__msg__ObstacleBlock), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = sentinel_oda_msgs__msg__ObstacleBlock__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        sentinel_oda_msgs__msg__ObstacleBlock__fini(&data[i - 1]);
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
sentinel_oda_msgs__msg__ObstacleBlock__Sequence__fini(sentinel_oda_msgs__msg__ObstacleBlock__Sequence * array)
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
      sentinel_oda_msgs__msg__ObstacleBlock__fini(&array->data[i]);
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

sentinel_oda_msgs__msg__ObstacleBlock__Sequence *
sentinel_oda_msgs__msg__ObstacleBlock__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  sentinel_oda_msgs__msg__ObstacleBlock__Sequence * array = (sentinel_oda_msgs__msg__ObstacleBlock__Sequence *)allocator.allocate(sizeof(sentinel_oda_msgs__msg__ObstacleBlock__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = sentinel_oda_msgs__msg__ObstacleBlock__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
sentinel_oda_msgs__msg__ObstacleBlock__Sequence__destroy(sentinel_oda_msgs__msg__ObstacleBlock__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    sentinel_oda_msgs__msg__ObstacleBlock__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
sentinel_oda_msgs__msg__ObstacleBlock__Sequence__are_equal(const sentinel_oda_msgs__msg__ObstacleBlock__Sequence * lhs, const sentinel_oda_msgs__msg__ObstacleBlock__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!sentinel_oda_msgs__msg__ObstacleBlock__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
sentinel_oda_msgs__msg__ObstacleBlock__Sequence__copy(
  const sentinel_oda_msgs__msg__ObstacleBlock__Sequence * input,
  sentinel_oda_msgs__msg__ObstacleBlock__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(sentinel_oda_msgs__msg__ObstacleBlock);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    sentinel_oda_msgs__msg__ObstacleBlock * data =
      (sentinel_oda_msgs__msg__ObstacleBlock *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!sentinel_oda_msgs__msg__ObstacleBlock__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          sentinel_oda_msgs__msg__ObstacleBlock__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!sentinel_oda_msgs__msg__ObstacleBlock__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
