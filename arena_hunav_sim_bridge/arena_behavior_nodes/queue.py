from typing import Dict, List

import attrs

from ..hunav_sim_node_wrapper.base_node import BaseNode
from ..agent.agent import Agent


@attrs.define
class Queue(BaseNode):
    agents: List[Agent]
    wait_duration: List[float]
    front_agent_pose: List[float] = attrs.field(
        metadata={"description":"The pose of the agent in the front of the queue, the pose of agents behind will be calculated base on this agent's pose and queue direction"}
    )
    direction: float = attrs.field(
        metadata={"description":"The direction of the queue in degree, the pose of agents will be calculated base on this attribute and front agent's pose"}
    )
    distances: List[float]

    def set_waiting_pose(self):
        ...
    
    def to_xml(self):
        ...