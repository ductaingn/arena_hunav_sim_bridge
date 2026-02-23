from typing import Dict, List, Tuple
from rclpy.node import Node
from rclpy.publisher import Publisher
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy

import numpy as np

from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker, MarkerArray
from std_msgs.msg import ColorRGBA


class WaypointVisualizer:
    def __init__(
        self,
        node: Node,
        topic_name: str = "/waypoints_marker",
    ):
        self.node = node
        self._logger = node.get_logger()

        # RViz Publisher
        self.qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        self.marker_publisher: Publisher = self.node.create_publisher(
            MarkerArray,
            topic_name,
            self.qos_profile,
        )

    def publish_markers(
        self,
        waypoints: Dict[str, List[Tuple[float, float]]],
    ):
        marker_array = MarkerArray()

        id_counter, n_points = 0, 0

        for agent_name, agent_waypoints in waypoints.items():
            n_makers, n_points = self._add_markers(
                agent_waypoints, agent_name, marker_array, id_counter
            )
            id_counter += n_makers
            n_points += n_points

        self._logger.info(f"Publishing {id_counter} markers with {n_points} total waypoints")
        self.marker_publisher.publish(marker_array)

    def _add_markers(
        self,
        agent_waypoints: List[Tuple[float, float]],
        namespace: str,
        marker_array: MarkerArray,
        start_id: int,
    ):
        id_counter = start_id
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.node.get_clock().now().to_msg()
        marker.ns = namespace
        marker.id = id_counter
        marker.type = Marker.POINTS
        marker.action = Marker.ADD
        marker.points = []
        # Marker size
        marker.scale.x = 0.2
        marker.scale.y = 0.2
        marker.color = ColorRGBA(r=1.0, g=0.5, b=0.0, a=1.0)

        for waypoint in agent_waypoints:
            point = Point(x=waypoint[0], y=waypoint[1], z=0.5)

            marker.points.append(point)

        marker_array.markers.append(marker)

        id_counter += 1
        n_points = len(agent_waypoints)

        return id_counter, n_points


if __name__ == "__main__":
    import rclpy
    from rclpy.executors import MultiThreadedExecutor

    rclpy.init()

    node = rclpy.create_node("waypoints_marker_test_node")

    visualizer = WaypointVisualizer(node)

    waypoints = {
        "agent_1": [(0.0, 1.0), (1.0, 0.0), (2.0, 2.0)],
        "agent_2": [(30.0, 10.0), (30.0, 11.0), (27.0, 8.0)],
    }
    visualizer.publish_markers(waypoints)

    executor = MultiThreadedExecutor()
    executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
