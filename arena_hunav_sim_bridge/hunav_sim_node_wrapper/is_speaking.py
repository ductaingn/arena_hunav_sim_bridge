import xml.etree.ElementTree as ET

import attrs

from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BTNode
from arena_hunav_sim_bridge.bt_models.tree_nodes_models import InputPort, Condition


@attrs.define
class IsSpeaking(BTNode):
    agent_id: int
    time_step: float
    target_id: int
    distance_threshold: float
    duration: float

    def get_actions_conditions(self):
        input_ports = [
            InputPort(name="agent_id", type="int"),
            InputPort(name="time_step", type="double"),
            InputPort(name="target_id",type="int"),
            InputPort(name="distance_threshold",type="double"),
            InputPort(name="duration", type="double"),
        ]

        actions = []

        conditions = [Condition(ID=self.__class__.__name__, input_ports=input_ports)]

        return actions, conditions

    def to_xml(self):
        element = ET.Element(
            self.__class__.__name__,
            attrib={
                "agent_id": "{id}",
                "time_step": str(self.time_step),
                "target_id": str(self.target_id),
                "distance_threshold": str(self.distance_threshold),
                "duration": str(self.duration),
            },
        )

        return element
