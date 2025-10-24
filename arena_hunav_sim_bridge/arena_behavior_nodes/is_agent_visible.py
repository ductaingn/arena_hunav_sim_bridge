import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaSingleAgentNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.is_agent_visible import (
    IsAgentVisible as HNSIsAgentVisible,
)


@ArenaSingleAgentNode.register_node
@attrs.define
class IsAgentVisible(ArenaSingleAgentNode):
    agent: Agent
    ovserver_agent: Agent
    distance: float

    def to_bt_node(self, **kwargs):
        iav_node = HNSIsAgentVisible(
            self.agent.id, self.ovserver_agent.id, self.distance
        )

        return iav_node
