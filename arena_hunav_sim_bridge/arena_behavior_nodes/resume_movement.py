import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaSingleAgentNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.resume_movement import (
    ResumeMovement as HNSResumeMovement,
)


@ArenaSingleAgentNode.register_node
@attrs.define
class ResumeMovement(ArenaSingleAgentNode):
    agent: Agent

    def to_bt_node(self, **kwargs):
        sm_node = HNSResumeMovement(self.agent.id)

        return sm_node
