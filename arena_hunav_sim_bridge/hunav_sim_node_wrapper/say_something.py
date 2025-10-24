import xml.etree.ElementTree as ET

import attrs

from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BTNode
from arena_hunav_sim_bridge.bt_models.tree_nodes_models import InputPort, Action


@attrs.define
class SaySomething(BTNode):
    agent_id: int
    message: str

    def to_xml(self):
        element = ET.Element(
            self.__class__.__name__,
            attrib={"agent_id": "{id}", "message": self.message},
        )

        return element

    def get_actions_conditions(self):
        input_ports = [
            InputPort(
                name="agent_id",
                type="int",
            ),
            InputPort(
                name="message",
                type="string",
            ),
        ]

        actions = [Action(ID="SaySomething", input_ports=input_ports)]

        conditions = []

        return actions, conditions
