import xml.etree.ElementTree as ET

import attrs

from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BTNode
from arena_hunav_sim_bridge.bt_models.tree_nodes_models import InputPort, Condition


@attrs.define
class IsAtPosition(BTNode):
    agent_id: int
    goal_id: int
    tolerance: float

    def to_xml(self):
        element = ET.Element(
            self.__class__.__name__,
            attrib={
                "agent_id": "{id}",
                "goal_id": str(self.goal_id),
                "tolerance": str(self.tolerance),
            },
        )

        return element

    def get_actions_conditions(self):
        input_ports = [
            InputPort(
                name="agent_id",
                type="int",
            ),
            InputPort(
                name="goal_id",
                type="int",
            ),
            InputPort(
                name="tolerance",
                type="double",
            ),
        ]

        actions = []

        conditions = [Condition(ID="IsAtPosition", input_ports=input_ports)]

        return actions, conditions
