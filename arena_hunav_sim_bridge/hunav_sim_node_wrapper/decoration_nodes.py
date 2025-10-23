from typing import List
import xml.etree.ElementTree as ET

import attrs

from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BTNode


@attrs.define
class DecorationNode(BTNode):
    def get_actions_conditions(self):
        return [], []

    def to_xml(self):
        raise NotImplementedError


@attrs.define
class TimeDelayDecorator(DecorationNode):
    child_node = BTNode

    def to_xml(self):
        element = ET.Element("TimeDelay")

        element.append(self.child_node.to_xml())

        return element


@attrs.define
class RetryUntilSuccessful(DecorationNode):
    child_node = BTNode

    def to_xml(self):
        element = ET.Element(self.__class__.__name__)

        element.append(self.child_node.to_xml())

        return element
