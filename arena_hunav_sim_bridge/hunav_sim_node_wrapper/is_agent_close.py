import xml.etree.ElementTree as ET

import attrs

from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BTNode
from arena_hunav_sim_bridge.bt_models.tree_nodes_models import InputPort, Condition


@attrs.define
class IsAgentClose(BTNode):
    agent_id: int
    observer_id: int

    def to_xml(self):
        element = ET.Element(
            self.__class__.__name__,
            attrib={
                "agent_id": "{id}",
                "observer_id": str(self.observer_id),
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
                name="observer_id",
                type="int",
            ),
        ]

        actions = []

        conditions = [Condition(ID="IsAgentClose", input_ports=input_ports)]

        return actions, conditions
