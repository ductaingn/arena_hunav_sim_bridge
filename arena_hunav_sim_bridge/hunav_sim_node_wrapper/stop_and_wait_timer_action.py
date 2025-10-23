import xml.etree.ElementTree as ET

import attrs

from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BaseNode
from arena_hunav_sim_bridge.bt_models.tree_nodes_models import InputPort, Action


@attrs.define
class StopAndWaitTimerAction(BaseNode):
    agent_id: int
    wait_duration: float

    def get_actions_conditions(self):
        input_ports = [
            InputPort(
                name="agent_id",
                type="int",
            ),
            InputPort(name="wait_duration", type="float"),
        ]

        actions = [Action(ID="StopAndWaitTimerAction", input_ports=input_ports)]

        conditions = []

        return actions, conditions

    def to_xml(self):
        element = ET.Element(
            self.__class__.__name__,
            attrib={
                "agent_id": str(self.agent_id),
                "wait_duration": str(self.wait_duration),
            },
        )

        return element
