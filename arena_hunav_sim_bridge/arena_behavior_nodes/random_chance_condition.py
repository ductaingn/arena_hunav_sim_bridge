import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaSingleAgentNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.random_chance_condition import (
    RandomChanceCondition as HNSRandomChanceCondition,
)


@ArenaSingleAgentNode.register_node
@attrs.define
class RandomChanceCondition(ArenaSingleAgentNode):
    agent: Agent
    probability: float

    def to_bt_node(self, **kwargs):
        rcc_node = HNSRandomChanceCondition(self.agent.id, self.probability)

        return rcc_node
