from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET

import attrs


@attrs.define
class BaseNode(ABC):
    @abstractmethod
    def to_xml(self) -> ET.Element:
        raise NotImplementedError
    
    