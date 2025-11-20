import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaSingleAgentNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.follow_agent import (
    FollowAgent as HNSFollowAgent,
)


@ArenaSingleAgentNode.register_node
@attrs.define
class FollowAgent(ArenaSingleAgentNode):
    agent: Agent
    target_agent: Agent
    duration: float
    time_step: float = 0.1

    def to_bt_node(self, **kwargs):
        aa_node = HNSFollowAgent(
            self.agent.id,
            self.target_agent.id,
            self.duration,
            self.time_step,
        )

        return aa_node
