from abc import ABC, abstractmethod
from typing import Dict, Type, Any
import xml.etree.ElementTree as ET

import attrs

from ..bt_models.bt_models import (
    InputPort,
    OutputPort,
    Condition,
    Action,
    ConditionNode, 
    ActionNode, 
    TreeNode,
    BehaviorTree
)


@attrs.define
class BaseNode(ABC):
    @abstractmethod
    def to_xml(self) -> ET.Element:
        raise NotImplementedError
    
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

class ArenaNode(BaseNode):
    """Base class for all Arena nodes (both single and multi-agent)."""

    @abstractmethod
    def to_bt_node(self, **kwargs) -> BTNode:
        raise NotImplementedError

class ArenaSingleAgentNode(ArenaNode):
    # Registry shared by all subclasses
    _registry: Dict[str, Type["ArenaSingleAgentNode"]] = {}

    def __init_subclass__(cls, **kwargs):
        """Auto-register subclasses by class name."""
        super().__init_subclass__(**kwargs)
        ArenaSingleAgentNode._registry[cls.__name__] = cls

    @classmethod
    def from_json(cls, class_name, **kwargs) -> "ArenaSingleAgentNode":
        """
        Factory: dynamically instantiate the correct subclass
        based on the 'name' field in the LLM JSON response.
        """
        node_cls = cls._registry.get(class_name)
        if node_cls is None:
            raise ValueError(f"Unknown node type: {class_name}")
        return node_cls(**kwargs)

class ArenaMultiAgentNode(ArenaNode):
    agents: Dict[int, Any]
    # Registry shared by all subclasses
    _registry: Dict[str, Type["ArenaMultiAgentNode"]] = {}

    def __init_subclass__(cls, **kwargs):
        """Auto-register subclasses by class name."""
        super().__init_subclass__(**kwargs)
        ArenaMultiAgentNode._registry[cls.__name__] = cls

    @classmethod
    def from_json(cls, class_name, **kwargs) -> "ArenaMultiAgentNode":
        """
        Factory: dynamically instantiate the correct subclass
        based on the 'name' field in the LLM JSON response.
        """
        node_cls = cls._registry.get(class_name)
        if node_cls is None:
            raise ValueError(f"Unknown node type: {class_name}")
        return node_cls(**kwargs)

    @abstractmethod
    def to_bt_node(self, agent_id: int, **kwargs) -> BTNode:
        raise NotImplementedError