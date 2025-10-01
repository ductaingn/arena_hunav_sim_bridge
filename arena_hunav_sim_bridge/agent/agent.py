from typing import Dict, List

import xml.etree.ElementTree as ET

import attrs


@attrs.define
class Agent:
    id: int
    name: str
    pos: List
    model: str
    waypoints: List[List]

    def to_xml(self)->ET.Element: