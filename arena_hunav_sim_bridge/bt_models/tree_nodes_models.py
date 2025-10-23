import xml.etree.ElementTree as ET
from typing import List, Optional

import attrs

CONTROL_NODE_ID_MAP = {}

DECORATION_NODE_ID_MAP = {"TimeDelayDecorator": "TimeDelay"}

ACTION_NODE_ID_MAP = {
    "GroupWalk": "SetGroupWalk",
}

CONDITION_NODE_ID_MAP = {}


@attrs.define
class InputPort:
    name: str
    type: str
    default: Optional[str] = None
    description: Optional[str] = None

    def to_xml(self) -> ET.Element:
        element = ET.Element(
            "input_port", attrib={"name": self.name, "type": self.type}
        )
        if self.default:
            element.set("default", self.default)
        if self.description:
            element.text = self.description

        return element


@attrs.define
class OutputPort:
    name: str
    type: str
    default: Optional[str] = None
    description: Optional[str] = None

    def to_xml(self) -> ET.Element:
        element = ET.Element(
            "output_port", attrib={"name": self.name, "type": self.type}
        )
        if self.default:
            element.set("default", self.default)
        if self.description:
            element.text = self.description

        return element


@attrs.define
class Condition:
    ID: str
    input_ports: Optional[List[InputPort]] = []
    output_port: Optional[List[OutputPort]] = []

    def to_xml(self) -> ET.Element:
        element = ET.Element("Condition", attrib={"ID": self.ID})

        for ip in self.input_ports or []:
            ip: InputPort
            element.append(ip.to_xml())

        for op in self.output_port or []:
            op: OutputPort
            element.append(op.to_xml())

        return element


@attrs.define
class Action:
    ID: str
    input_ports: Optional[List[InputPort]] = []
    output_port: Optional[List[OutputPort]] = []

    def __attrs_post_init__(self):
        if self.ID in ACTION_NODE_ID_MAP:
            self.ID = ACTION_NODE_ID_MAP[self.ID]

    def to_xml(self) -> ET.Element:
        element = ET.Element("Action", attrib={"ID": self.ID})

        for ip in self.input_ports or []:
            ip: InputPort
            element.append(ip.to_xml())

        for op in self.output_port or []:
            op: OutputPort
            element.append(op.to_xml())

        return element


@attrs.define
class TreeNodesModel:
    conditions: Optional[List[Condition]] = []
    actions: Optional[List[Action]] = []

    def to_xml(self) -> ET.Element:
        element = ET.Element("TreeNodesModel")

        for action in self.actions:
            element.append(action.to_xml())

        for condition in self.conditions:
            element.append(condition.to_xml())

        return element
