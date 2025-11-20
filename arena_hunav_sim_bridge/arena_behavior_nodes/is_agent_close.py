import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaSingleAgentNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.is_agent_close import (
    IsAgentClose as HNSIsAgentClose,
)


@ArenaSingleAgentNode.register_node
@attrs.define
class IsAgentClose(ArenaSingleAgentNode):
    agent: Agent
    observer_agent: Agent
    threshold: float = 1.0

    def to_bt_node(self, **kwargs):
        iac_node = HNSIsAgentClose(
            self.agent.id, self.observer_agent.id, self.threshold
        )

        return iac_node
