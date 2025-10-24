import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaSingleAgentNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.stop_movement import (
    StopMovement as HNSStopMovement,
)


@ArenaSingleAgentNode.register_node
@attrs.define
class StopMovement(ArenaSingleAgentNode):
    agent: Agent

    def to_bt_node(self, **kwargs):
        sm_node = HNSStopMovement(self.agent.id)

        return sm_node
