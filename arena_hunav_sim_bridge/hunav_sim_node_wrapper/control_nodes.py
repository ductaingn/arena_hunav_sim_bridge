from typing import List
import xml.etree.ElementTree as ET

import attrs

from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BTNode


@attrs.define
class ControlNode(BTNode):
    children_nodes: List[BTNode]

    def get_actions_conditions(self):
        all_actions, all_conditions = [], []
        for node in self.children_nodes:
            actions, conditions = node.get_actions_conditions()
            for action in actions:
                all_actions.append(action)
            for condition in conditions:
                all_conditions.append(condition)

        return all_actions, all_conditions

    def to_xml(self):
        raise NotImplementedError


@attrs.define
class Sequence(ControlNode):
    def to_xml(self):
        element = ET.Element(self.__class__.__name__)

        for node in self.children_nodes:
            element.append(node.to_xml())

        return element


@attrs.define
class Fallback(ControlNode):
    def to_xml(self):
        element = ET.Element(self.__class__.__name__)

        for node in self.children_nodes:
            element.append(node.to_xml())

        return element
