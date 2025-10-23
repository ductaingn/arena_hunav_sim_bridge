import xml.etree.ElementTree as ET

import attrs

from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BTNode
from arena_hunav_sim_bridge.bt_models.tree_nodes_models import InputPort, Action


@attrs.define
class SetGoal(BTNode):
    agent_id: int
    target_x: float
    target_y: float
    goal_id: int

    def to_xml(self):
        element = ET.Element(
            self.__class__.__name__,
            attrib={
                "agent_id": "{id}",
                "goal_id": str(self.goal_id),
                "target_x": str(self.target_x),
                "target_y": str(self.target_y),
            },
        )

        return element

    def get_actions_conditions(self):
        input_ports = [
            InputPort(
                name="agent_id",
                type="int",
            ),
            InputPort(name="target_x", type="float"),
            InputPort(name="target_y", type="float"),
            InputPort(
                name="goal_id",
                type="int",
            ),
        ]

        actions = [Action(ID="SetGoal", input_ports=input_ports)]

        conditions = []

        return actions, conditions
