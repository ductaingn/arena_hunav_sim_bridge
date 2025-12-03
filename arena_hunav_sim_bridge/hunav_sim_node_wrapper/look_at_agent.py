import xml.etree.ElementTree as ET

import attrs

from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BTNode
from arena_hunav_sim_bridge.bt_models.tree_nodes_models import InputPort, Action


@attrs.define
class LookAtAgent(BTNode):
    observer_id: int
    target_id: int
    yaw_tolerance: float

    def get_actions_conditions(self):
        input_ports = [
            InputPort(name="observer_id", type="int"),
            InputPort(name="target_id", type="int"),
            InputPort(name="yaw_tolerance",type="double"),
        ]

        actions = [Action(ID=self.__class__.__name__, input_ports=input_ports)]

        conditions = []

        return actions, conditions

    def to_xml(self):
        element = ET.Element(
            self.__class__.__name__,
            attrib={
                "agent_id": "{id}",
                "target_id": str(self.target_id),
                "yaw_tolerance": str(self.yaw_tolerance),
            },
        )

        return element
