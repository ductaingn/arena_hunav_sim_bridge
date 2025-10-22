from typing import Dict, List

import attrs

from ..hunav_sim_node_wrapper.base_node import ArenaNode


@attrs.define
class GoalIDManager:
    """
    This class provide global IDs to the goals, so that the LLM doesn't have to.
    """
    goal_id: int = attrs.field(default=0, init=False)

    def set_goals_id(self, node: ArenaNode):
        """
        Set ID to this node if it need `goal_id` field
        """
        if not hasattr(node, "goal_id"):
            raise ModuleNotFoundError(f"This node {node.__class__} does not have `goal_id` field!")
        else:
            node.goal_id = self.goal_id
            self.goal_id += 1