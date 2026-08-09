import rclpy
import json
from rclpy.node import Node
from mavros_msgs.msg import CommandCode, Waypoint, State
from geometry_msgs.msg import PoseStamped


def load_qgc_plan(path):
    """Parse a QGroundControl .plan (JSON) file into Waypoint messages."""
    with open(path, "r") as f:
        data = json.load(f)
 
    mission = data["mission"]
    home_lat, home_lon, home_alt = mission["plannedHomePosition"]
 
    # QGC stores home separately in the JSON, but ArduPilot expects it
    # as seq 0 of the pushed mission - the same slot the older .waypoints
    # format bakes directly into the file.
    waypoints = [
        Waypoint(
            frame=Waypoint.FRAME_GLOBAL,
            command=CommandCode.NAV_WAYPOINT,
            is_current=True,
            autocontinue=True,
            param1=0.0, param2=0.0, param3=0.0, param4=0.0,
            x_lat=home_lat, y_long=home_lon, z_alt=home_alt,
        )
    ]
 
    for item in mission["items"]:
        if item.get("type") != "SimpleItem":
            raise ValueError(
                f"item type {item.get('type')!r} not handled here - this "
                "covers plain waypoints, not surveys/complex patterns"
            )
        p1, p2, p3, p4, lat, lon, alt = item["params"]
        waypoints.append(Waypoint(
            frame=item["frame"],
            command=item["command"],
            is_current=False,
            autocontinue=item["autoContinue"],
            param1=_f(p1), param2=_f(p2), param3=_f(p3), param4=_f(p4),
            x_lat=lat, y_long=lon, z_alt=alt,
        ))
 
    return waypoints


class OffboardNode(Node):

    def __init__(self):
        super().__init__("offboard_node")

        self.state = State()
        self.msg = PoseStamped()

        self.create_subscription(
            State,
            "/mavros/state",
            self.state_callback,
            10
        )

        self.publisher = self.create_publisher(
            PoseStamped,
            "/mavros/setpoint_position/local",
            10
        )

        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.pose_callback)
        self.i = 0

    def pose_callback(self):
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.position.x = 5.0
        msg.pose.position.y = 0.0
        msg.pose.position.z = 2.0
        self.publisher.publish(msg)
        self.get_logger().info('Publishing: waypoint coordinates')
        self.i += 1

    def state_callback(self, msg):
        self.state = msg


def main():
    rclpy.init()

    node = OffboardNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()