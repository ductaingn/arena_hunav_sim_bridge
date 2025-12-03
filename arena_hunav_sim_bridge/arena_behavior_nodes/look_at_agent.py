import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaSingleAgentNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.look_at_agent import (
    LookAtAgent as HNSLookAtAgent,
)


@ArenaSingleAgentNode.register_node
@attrs.define
class LookAtAgent(ArenaSingleAgentNode):
    observer_agent: Agent
    target_agent: Agent
    yaw_tolerance: float

    def to_bt_node(self, **kwargs):
        laa_node = HNSLookAtAgent(
            self.observer_agent.id,
            self.target_agent.id,
            self.yaw_tolerance
        )

        return laa_node
