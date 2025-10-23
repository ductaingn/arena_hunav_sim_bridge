import xml.etree.ElementTree as ET

import attrs

from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BTNode
from arena_hunav_sim_bridge.bt_models.tree_nodes_models import InputPort, Action


@attrs.define
class GoTo(BTNode):
    agent_id: int
    goal_id: int
    time_step: float = 0.1
    tolerance: float = 1

    def get_actions_conditions(self):
        input_ports = [
            InputPort(
                name="agent_id",
                type="int",
            ),
            InputPort(name="goal_id", type="int"),
            InputPort(name="time_step", type="float"),
            InputPort(
                name="tolerance",
                type="int",
            ),
        ]

        actions = [Action(ID="SetGoal", input_ports=input_ports)]

        conditions = []

        return actions, conditions

    def to_xml(self):
        element = ET.Element(
            self.__class__.__name__,
            attrib={
                "agent_id": str(self.agent_id),
                "goal_id": str(self.goal_id),
                "time_step": str(self.time_step),
                "tolerance": str(self.tolerance),
            },
        )

        return element
