import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaSingleAgentNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.say_something import (
    SaySomething as HNSSaySomething,
)


@ArenaSingleAgentNode.register_node
@attrs.define
class SaySomething(ArenaSingleAgentNode):
    agent: Agent
    message: str

    def to_bt_node(self, **kwargs):
        ss_node = HNSSaySomething(self.agent.id, self.message)

        return ss_node
