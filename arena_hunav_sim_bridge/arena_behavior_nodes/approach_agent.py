import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaSingleAgentNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.approach_agent import (
    ApproachAgent as HNSApproachAgent,
)


@ArenaSingleAgentNode.register_node
@attrs.define
class ApproachAgent(ArenaSingleAgentNode):
    agent: Agent
    target_agent: Agent
    closest_dist: float
    max_vel: float
    duration: float
    time_step: float = 0.1

    def to_bt_node(self, **kwargs):
        aa_node = HNSApproachAgent(
            self.agent.id,
            self.target_agent.id,
            self.closest_dist,
            self.max_vel,
            self.duration,
            self.time_step,
        )

        return aa_node
