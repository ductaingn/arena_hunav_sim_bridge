import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaSingleAgentNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.find_nearest_agent import (
    FindNearestAgent as HNSFindNearestAgent,
)


@ArenaSingleAgentNode.register_node
@attrs.define
class FindNearestAgent(ArenaSingleAgentNode):
    agent: Agent

    def to_bt_node(self, **kwargs):
        fna_node = HNSFindNearestAgent(self.agent.id)

        return fna_node
