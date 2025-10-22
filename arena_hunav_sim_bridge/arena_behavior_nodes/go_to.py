from typing import Dict, List
import numpy as np

import attrs

from ..agent.agent import Agent
from ..bt_models.bt_models import ControlNode
from ..ids_manager.goal_id_manager import GoalIDManager
from ..hunav_sim_node_wrapper.base_node import ArenaSingleAgentNode, BehaviorTree
from ..hunav_sim_node_wrapper.set_goal import SetGoal
from ..hunav_sim_node_wrapper.go_to import GoTo as HNSGoto


@attrs.define
class GoTo(ArenaSingleAgentNode):
    agent_id: int
    time_step: float = 0.1
    target_x: float
    target_y: float
    tolerance: float = 1
    goal_id: int

    def to_bt_node(self, goal_id_manager: GoalIDManager, **kwargs):
        set_goal_node = SetGoal(self.agent_id, self.target_x, self.target_y, self.goal_id)

        goal_id_manager.set_goals_id()

        go_to_node = HNSGoto(self.agent_id, self.time_step, self.goal_id, self.tolerance)
        
        control_node = ControlNode(
            ID="Sequence",
            name="",
            children_nodes=[
                set_goal_node, 
                go_to_node
            ]
        )
        
        return control_node