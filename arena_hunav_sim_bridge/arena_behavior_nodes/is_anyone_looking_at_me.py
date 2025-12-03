import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaSingleAgentNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.is_anyone_looking_at_me import (
    IsAnyoneLookingAtMe as HNSIsAnyoneLookingAtMe,
)


@ArenaSingleAgentNode.register_node
@attrs.define
class IsAnyoneLookingAtMe(ArenaSingleAgentNode):
    agent: Agent
    time_step: float
    distance_threshold: float
    angle_threshold: float
    duration: float

    def to_bt_node(self, **kwargs):
        ialam_node = HNSIsAnyoneLookingAtMe(
            self.agent.id, self.time_step, self.distance_threshold, self.angle_threshold, self.duration
        )

        return ialam_node
