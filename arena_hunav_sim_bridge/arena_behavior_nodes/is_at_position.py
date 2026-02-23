import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.ids_manager.goal_id_manager import GoalIDManager
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaSingleAgentNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.set_goal import SetGoal
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.is_at_position import (
    IsAtPosition as HNSIsAtPosition,
)
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.control_nodes import Sequence


@ArenaSingleAgentNode.register_node
@attrs.define
class IsAtPosition(ArenaSingleAgentNode):
    agent: Agent
    target_x: float
    target_y: float
    tolerance: float = 1

    def to_bt_node(self, *, goal_id_manager: GoalIDManager, **kwargs):
        goal_id = goal_id_manager.get_goal_id()
        goal_id_manager.update_goal_pos(goal_id, (self.target_x, self.target_y))

        set_goal_node = SetGoal(self.agent.id, self.target_x, self.target_y, goal_id)

        iap_node = HNSIsAtPosition(self.agent.id, goal_id, self.tolerance)

        # TODO: check logic
        control_node = Sequence(children_nodes=[set_goal_node, iap_node])

        return control_node
