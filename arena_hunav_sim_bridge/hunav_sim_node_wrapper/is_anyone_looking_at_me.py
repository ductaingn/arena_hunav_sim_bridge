import xml.etree.ElementTree as ET

import attrs

from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BTNode
from arena_hunav_sim_bridge.bt_models.tree_nodes_models import InputPort, OutputPort, Condition


@attrs.define
class IsAnyoneLookingAtMe(BTNode):
    agent_id: int
    time_step: float
    distance_threshold: float
    angle_threshold: float
    duration: float

    def get_actions_conditions(self):
        input_ports = [
            InputPort(name="agent_id", type="int"),
            InputPort(name="time_step", type="double"),
            InputPort(name="distance_threshold",type="double"),
            InputPort(name="angle_threshold",type="double"),
            InputPort(name="duration", type="double"),
        ]
        output_ports = [
            OutputPort(name="observer_id", type="int")
        ]

        actions = []

        conditions = [Condition(ID=self.__class__.__name__, input_ports=input_ports, output_ports=output_ports)]

        return actions, conditions

    def to_xml(self):
        element = ET.Element(
            self.__class__.__name__,
            attrib={
                "agent_id": "{id}",
                "time_step": str(self.time_step),
                "distance_threshold": str(self.distance_threshold),
                "angle_threshold": str(self.angle_threshold),
                "duration": str(self.duration),
            },
        )

        return element
