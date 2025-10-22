import attrs

import xml.etree.ElementTree as ET

from .base_node import BTNode, InputPort, Action


@attrs.define
class SetGoal(BTNode):
    agent_id: int
    target_x: float
    target_y: float
    goal_id: int
    
    def to_xml(self):
        pass

    def get_actions_conditions(self):
        """
        Return
        ------
        actions
        conditions
        """
        input_ports = [
            InputPort(
                name="agent_id",
                type="int",
            ),
            InputPort(
                name="target_x",
                type="float"
            ),
            InputPort(
                name="target_y",
                type="float"
            ),
            InputPort(
                name="goal_id",
                type="int",
            )
        ]

        actions = [
            Action(
                ID = "SetGoal",
                input_ports=input_ports
            )
        ]

        conditions = []

        return actions, conditions
