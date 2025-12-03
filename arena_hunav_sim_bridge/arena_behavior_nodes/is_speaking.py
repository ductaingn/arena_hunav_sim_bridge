import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaSingleAgentNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.is_speaking import (
    IsSpeaking as HNSIsSpeaking,
)


@ArenaSingleAgentNode.register_node
@attrs.define
class IsSpeaking(ArenaSingleAgentNode):
    agent: Agent
    time_step: float
    target_agent: Agent
    distance_threshold: float
    duration: float

    def to_bt_node(self, **kwargs):
        is_node = HNSIsSpeaking(
            self.agent.id, self.time_step, self.target_agent.id, self.distance_threshold, self.duration
        )

        return is_node
