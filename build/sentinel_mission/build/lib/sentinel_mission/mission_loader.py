#!/usr/bin/env python3
"""
Shared mission file loader.
Parses a QGroundControl .plan (JSON) file into ROS Waypoint messages.
"""

import json
from mavros_msgs.msg import CommandCode, Waypoint


def _f(value, default=0.0):
    """QGC's JSON often has `null` for unused params - coerce to a float."""
    return float(value) if value is not None else default


def load_qgc_plan(path: str) -> list:
    """
    Parse a QGroundControl .plan (JSON) file into a list of Waypoint messages.

    The first waypoint (seq 0) is always the home position, which ArduPilot
    expects as part of the pushed mission.
    """
    with open(path, "r") as f:
        data = json.load(f)

    mission = data["mission"]
    home_lat, home_lon, home_alt = mission["plannedHomePosition"]

    waypoints = [
        Waypoint(
            frame=Waypoint.FRAME_GLOBAL,
            command=CommandCode.NAV_WAYPOINT,
            is_current=True,
            autocontinue=True,
            param1=0.0, param2=0.0, param3=0.0, param4=0.0,
            x_lat=_f(home_lat), y_long=_f(home_lon), z_alt=_f(home_alt),
        )
    ]

    for item in mission["items"]:
        if item.get("type") != "SimpleItem":
            raise ValueError(
                f"Item type {item.get('type')!r} not handled — this loader "
                "covers plain waypoints only, not surveys or complex patterns."
            )
        p1, p2, p3, p4, lat, lon, alt = item["params"]
        waypoints.append(Waypoint(
            frame=item["frame"],
            command=item["command"],
            is_current=False,
            autocontinue=item["autoContinue"],
            param1=_f(p1), param2=_f(p2), param3=_f(p3), param4=_f(p4),
            x_lat=_f(lat), y_long=_f(lon), z_alt=_f(alt),
        ))

    return waypoints
