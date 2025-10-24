import xml.etree.ElementTree as ET

import attrs

from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BTNode
from arena_hunav_sim_bridge.bt_models.tree_nodes_models import (
    InputPort,
    OutputPort,
    Action,
)


@attrs.define
class FindNearestAgent(BTNode):
    agent_id: int

    def to_xml(self):
        element = ET.Element(
            self.__class__.__name__,
            attrib={
                "agent_id": "{id}",
            },
        )

        return element

    def get_actions_conditions(self):
        input_ports = [
            InputPort(
                name="agent_id",
                type="int",
            ),
        ]
        output_ports = [OutputPort(name="target_agent_id", type="int")]

        actions = [
            Action(
                ID="FindNearestAgent", input_ports=input_ports, output_port=output_ports
            )
        ]

        conditions = []

        return actions, conditions
