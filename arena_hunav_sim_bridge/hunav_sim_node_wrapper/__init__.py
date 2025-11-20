from abc import abstractmethod
import xml.etree.ElementTree as ET

from arena_hunav_sim_bridge import BaseNode


class BTNode(BaseNode):
    @abstractmethod
    def get_actions_conditions(self):
        """
        Return
        ------
        actions
        conditions
        """
        raise NotImplementedError

    @abstractmethod
    def to_xml(self):
        raise NotImplementedError
