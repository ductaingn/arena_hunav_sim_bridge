import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaSingleAgentNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.block_agent import (
    BlockAgent as HNSBlockAgent,
)


@ArenaSingleAgentNode.register_node
@attrs.define
class BlockAgent(ArenaSingleAgentNode):
    agent: Agent
    target_agent: Agent
    front_dist: float
    duration: float
    time_step: float = 0.1

    def to_bt_node(self, **kwargs):
        ba_node = HNSBlockAgent(
            self.agent.id,
            self.target_agent.id,
            self.front_dist,
            self.time_step,
            self.duration,
        )

        return ba_node
