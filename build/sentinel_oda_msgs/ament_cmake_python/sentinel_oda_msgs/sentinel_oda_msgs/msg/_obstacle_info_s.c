// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from sentinel_oda_msgs:msg/ObstacleInfo.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "sentinel_oda_msgs/msg/detail/obstacle_info__struct.h"
#include "sentinel_oda_msgs/msg/detail/obstacle_info__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool sentinel_oda_msgs__msg__obstacle_info__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[50];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("sentinel_oda_msgs.msg._obstacle_info.ObstacleInfo", full_classname_dest, 49) == 0);
  }
  sentinel_oda_msgs__msg__ObstacleInfo * ros_message = _ros_message;
  {  // closest_distance
    PyObject * field = PyObject_GetAttrString(_pymsg, "closest_distance");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->closest_distance = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // obstacle_width
    PyObject * field = PyObject_GetAttrString(_pymsg, "obstacle_width");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->obstacle_width = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // current_heading
    PyObject * field = PyObject_GetAttrString(_pymsg, "current_heading");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->current_heading = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // obstacle_left
    PyObject * field = PyObject_GetAttrString(_pymsg, "obstacle_left");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->obstacle_left = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * sentinel_oda_msgs__msg__obstacle_info__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of ObstacleInfo */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("sentinel_oda_msgs.msg._obstacle_info");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "ObstacleInfo");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  sentinel_oda_msgs__msg__ObstacleInfo * ros_message = (sentinel_oda_msgs__msg__ObstacleInfo *)raw_ros_message;
  {  // closest_distance
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->closest_distance);
    {
      int rc = PyObject_SetAttrString(_pymessage, "closest_distance", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // obstacle_width
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->obstacle_width);
    {
      int rc = PyObject_SetAttrString(_pymessage, "obstacle_width", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // current_heading
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->current_heading);
    {
      int rc = PyObject_SetAttrString(_pymessage, "current_heading", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // obstacle_left
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->obstacle_left);
    {
      int rc = PyObject_SetAttrString(_pymessage, "obstacle_left", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
