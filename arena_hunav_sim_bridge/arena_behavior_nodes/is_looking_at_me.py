import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaSingleAgentNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.is_looking_at_me import (
    IsLookingAtMe as HNSIsLookingAtMe,
)


@ArenaSingleAgentNode.register_node
@attrs.define
class IsLookingAtMe(ArenaSingleAgentNode):
    agent: Agent
    time_step: float
    target_agent: Agent
    distance_threshold: float
    angle_threshold: float
    duration: float

    def to_bt_node(self, **kwargs):
        ilam_node = HNSIsLookingAtMe(
            self.agent.id, self.time_step, self.target_agent.id, self.distance_threshold, self.angle_threshold, self.duration
        )

        return ilam_node
