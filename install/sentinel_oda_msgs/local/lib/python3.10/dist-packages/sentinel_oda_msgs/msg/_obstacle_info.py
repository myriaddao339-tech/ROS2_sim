# generated from rosidl_generator_py/resource/_idl.py.em
# with input from sentinel_oda_msgs:msg/ObstacleInfo.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ObstacleInfo(type):
    """Metaclass of message 'ObstacleInfo'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('sentinel_oda_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'sentinel_oda_msgs.msg.ObstacleInfo')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__obstacle_info
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__obstacle_info
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__obstacle_info
            cls._TYPE_SUPPORT = module.type_support_msg__msg__obstacle_info
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__obstacle_info

            from sentinel_oda_msgs.msg import ObstacleBlock
            if ObstacleBlock.__class__._TYPE_SUPPORT is None:
                ObstacleBlock.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ObstacleInfo(metaclass=Metaclass_ObstacleInfo):
    """Message class 'ObstacleInfo'."""

    __slots__ = [
        '_blocks',
        '_closest_distance',
        '_obstacle_width',
        '_current_heading',
        '_obstacle_left',
    ]

    _fields_and_field_types = {
        'blocks': 'sequence<sentinel_oda_msgs/ObstacleBlock>',
        'closest_distance': 'float',
        'obstacle_width': 'float',
        'current_heading': 'float',
        'obstacle_left': 'float',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['sentinel_oda_msgs', 'msg'], 'ObstacleBlock')),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.blocks = kwargs.get('blocks', [])
        self.closest_distance = kwargs.get('closest_distance', float())
        self.obstacle_width = kwargs.get('obstacle_width', float())
        self.current_heading = kwargs.get('current_heading', float())
        self.obstacle_left = kwargs.get('obstacle_left', float())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.blocks != other.blocks:
            return False
        if self.closest_distance != other.closest_distance:
            return False
        if self.obstacle_width != other.obstacle_width:
            return False
        if self.current_heading != other.current_heading:
            return False
        if self.obstacle_left != other.obstacle_left:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def blocks(self):
        """Message field 'blocks'."""
        return self._blocks

    @blocks.setter
    def blocks(self, value):
        if __debug__:
            from sentinel_oda_msgs.msg import ObstacleBlock
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, ObstacleBlock) for v in value) and
                 True), \
                "The 'blocks' field must be a set or sequence and each value of type 'ObstacleBlock'"
        self._blocks = value

    @builtins.property
    def closest_distance(self):
        """Message field 'closest_distance'."""
        return self._closest_distance

    @closest_distance.setter
    def closest_distance(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'closest_distance' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'closest_distance' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._closest_distance = value

    @builtins.property
    def obstacle_width(self):
        """Message field 'obstacle_width'."""
        return self._obstacle_width

    @obstacle_width.setter
    def obstacle_width(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'obstacle_width' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'obstacle_width' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._obstacle_width = value

    @builtins.property
    def current_heading(self):
        """Message field 'current_heading'."""
        return self._current_heading

    @current_heading.setter
    def current_heading(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'current_heading' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'current_heading' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._current_heading = value

    @builtins.property
    def obstacle_left(self):
        """Message field 'obstacle_left'."""
        return self._obstacle_left

    @obstacle_left.setter
    def obstacle_left(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'obstacle_left' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'obstacle_left' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._obstacle_left = value
