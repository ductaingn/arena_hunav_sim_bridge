import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaSingleAgentNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.is_anyone_speaking import (
    IsAnyoneSpeaking as HNSIsAnyoneSpeaking,
)


@ArenaSingleAgentNode.register_node
@attrs.define
class IsAnyoneSpeaking(ArenaSingleAgentNode):
    agent: Agent
    time_step: float
    distance_threshold: float
    duration: float

    def to_bt_node(self, **kwargs):
        ias_node = HNSIsAnyoneSpeaking(
            self.agent.id, self.time_step, self.distance_threshold, self.duration
        )

        return ias_node
