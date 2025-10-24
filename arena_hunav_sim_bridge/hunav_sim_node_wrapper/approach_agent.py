import xml.etree.ElementTree as ET

import attrs

from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BTNode
from arena_hunav_sim_bridge.bt_models.tree_nodes_models import InputPort, Action


@attrs.define
class ApproachAgent(BTNode):
    agent_id: int
    target_agent_id: int
    closest_dist: float
    max_vel: float
    duration: float
    time_step: float = 0.1

    def get_actions_conditions(self):
        input_ports = [
            InputPort(
                name="agent_id",
                type="int",
            ),
            InputPort(
                name="target_agent_id",
                type="int",
            ),
            InputPort(name="time_step", type="double"),
            InputPort(name="closest_dist", type="double"),
            InputPort(name="max_vel", type="double"),
            InputPort(
                name="duration",
                type="double",
            ),
        ]

        actions = [Action(ID="SetGoal", input_ports=input_ports)]

        conditions = []

        return actions, conditions

    def to_xml(self):
        element = ET.Element(
            self.__class__.__name__,
            attrib={
                "agent_id": "{id}",
                "target_agent_id": str(self.target_agent_id),
                "time_step": str(self.time_step),
                "closest_dist": str(self.closest_dist),
                "max_vel": str(self.max_vel),
                "duration": str(self.duration),
            },
        )

        return element
