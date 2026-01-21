import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaSingleAgentNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.follow_velocity_field import FollowVelocityField as HNSFollowVelocityField
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.control_nodes import Sequence


@ArenaSingleAgentNode.register_node
@attrs.define
class FollowVelocityField(ArenaSingleAgentNode):
    agent: Agent
    velocity_field_group_id: int
    time_step: float = 0.1
    tolerance: float = 1

    def to_bt_node(self, **kwargs):
        fvf_node = HNSFollowVelocityField(self.agent.id, self.velocity_field_group_id, self.time_step, self.tolerance)

        control_node = Sequence(children_nodes=[fvf_node])

        return control_node
