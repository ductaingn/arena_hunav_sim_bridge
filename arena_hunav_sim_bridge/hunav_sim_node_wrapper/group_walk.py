import xml.etree.ElementTree as ET

import attrs

from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BTNode
from arena_hunav_sim_bridge.bt_models.tree_nodes_models import InputPort, Action


@attrs.define
class GroupWalk(BTNode):
    main_agent_id: int
    time_step: float
    non_main_agent_ids: str
    duration: float

    def get_actions_conditions(self):
        input_ports = [
            InputPort(
                name="main_agent_id",
                type="int",
            ),
            InputPort(name="duration", type="double"),
            InputPort(
                name="goal",
                type="int",
            ),
            InputPort(name="time_step", type="double"),
            InputPort(
                name="non_main_agent_ids",
                type="string",
            ),
        ]

        actions = [Action(ID="SetGroupWalk", input_ports=input_ports)]

        conditions = []

        return actions, conditions

    def to_xml(self):
        element = ET.Element(
            "SetGroupWalk",
            attrib={
                "main_agent_id": str(self.main_agent_id),
                "time_step": str(self.time_step),
                "non_main_agent_ids": self.non_main_agent_ids,
                "duration": str(self.duration),
            },
        )

        return element
