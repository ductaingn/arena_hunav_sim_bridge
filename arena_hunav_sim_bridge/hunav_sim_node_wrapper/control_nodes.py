from typing import List
import xml.etree.ElementTree as ET

import attrs

from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BTNode


@attrs.define
class ControlNode(BTNode):
    def get_actions_conditions(self):
        return [], []

    def to_xml(self):
        raise NotImplementedError


@attrs.define
class Sequence(ControlNode):
    children_nodes: List[BTNode]

    def to_xml(self):
        element = ET.Element(self.__class__.__name__)

        for node in self.children_nodes:
            element.append(node.to_xml())

        return element


@attrs.define
class Fallback(ControlNode):
    children_nodes: List[BTNode]

    def to_xml(self):
        element = ET.Element(self.__class__.__name__)

        for node in self.children_nodes:
            element.append(node.to_xml())

        return element
