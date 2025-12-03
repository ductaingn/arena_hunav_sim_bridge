from abc import ABC, abstractmethod
from typing import Dict, Type, Any, Callable
import xml.etree.ElementTree as ET

from arena_hunav_sim_bridge import BaseNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BTNode


class ArenaNode(BaseNode):
    """Base class for all Arena nodes (both single and multi-agent)."""

    @abstractmethod
    def to_bt_node(self, *args, **kwargs) -> BTNode:
        raise NotImplementedError


class ArenaSingleAgentNode(ArenaNode):
    # Registry shared by all subclasses
    _registry: Dict[str, Type["ArenaSingleAgentNode"]] = {}

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

    @abstractmethod
    def to_bt_node(self, **kwargs) -> BTNode:
        raise NotImplementedError

    @classmethod
    def register_node(cls, node_cls: type["ArenaSingleAgentNode"]):
        assert (
            node_cls.__name__ not in cls._registry
        ), f"Node {node_cls.__name__} already exist!"

        cls._registry[node_cls.__name__] = node_cls

        return node_cls


class ArenaMultiAgentNode(ArenaNode):
    # Registry shared by all subclasses
    _registry: Dict[str, Type["ArenaMultiAgentNode"]] = {}

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
    def to_bt_node(self, agent_name: str, **kwargs) -> BTNode:
        raise NotImplementedError

    @classmethod
    def register_node(cls, node_cls: Callable[[], type["ArenaMultiAgentNode"]]):
        assert (
            node_cls.__name__ not in cls._registry
        ), f"Node {node_cls.__name__} already exist!"

        cls._registry[node_cls.__name__] = node_cls

        return node_cls


from .advance_queue import AdvanceQueue
from .approach_agent import ApproachAgent
from .block_agent import BlockAgent
from .conversation_formation import ConversationFormation
from .find_nearest_agent import FindNearestAgent
from .follow_agent import FollowAgent
from .form_queue import FormQueue
from .go_to import GoTo
from .group_walk import GroupWalk
from .is_agent_close import IsAgentClose
from .is_agent_visible import IsAgentVisible
from .is_anyone_looking_at_me import IsAnyoneLookingAtMe
from .is_anyone_speaking import IsAnyoneSpeaking
from .is_at_position import IsAtPosition
from .is_looking_at_me import IsLookingAtMe
from .is_speaking import IsSpeaking
from .look_at_agent import LookAtAgent
from .look_at_point import LookAtPoint
from .random_chance_condition import RandomChanceCondition
from .resume_movement import ResumeMovement
from .say_something import SaySomething
from .stop_and_wait_timer_action import StopAndWaitTimerAction
from .stop_movement import StopMovement
