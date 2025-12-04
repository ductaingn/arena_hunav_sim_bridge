import xml.etree.ElementTree as ET

import attrs

from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BTNode
from arena_hunav_sim_bridge.bt_models.tree_nodes_models import InputPort, Action


@attrs.define
class LookAtPoint(BTNode):
    agent_id: int
    goal_id: int
    yaw_tolerance: float = 0.087 # [rad] ~ 5 degree

    def get_actions_conditions(self):
        input_ports = [
            InputPort(
                name="agent_id",
                type="int",
            ),
            InputPort(name="goal_id", type="int"),
            InputPort(
                name="yaw_tolerance",
                type="int",
            ),
        ]

        actions = [Action(ID="LookAtPoint", input_ports=input_ports)]

        conditions = []

        return actions, conditions

    def to_xml(self):
        element = ET.Element(
            self.__class__.__name__,
            attrib={
                "agent_id": "{id}",
                "goal_id": str(self.goal_id),
                "yaw_tolerance": str(self.yaw_tolerance),
            },
        )

        return element
