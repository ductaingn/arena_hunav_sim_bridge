import attrs
from typing import Dict, Tuple


@attrs.define
class GoalIDManager:
    """
    This class provide global IDs to the goals, so that the LLM doesn't have to.
    """

    goal_id: int = attrs.field(default=0, init=False)
    goals: Dict[int, Tuple[float, float]] = attrs.field(default=dict(), init=False)

    def get_goal_id(self, goal_pos: Tuple[float, float] = None) -> int:
        goal_id = self.goal_id
        self.goal_id += 1

        if goal_pos is not None:
            self.goals[goal_id] = goal_pos

        return goal_id

    def update_goal_pos(self, goal_id: int, goal_pos: Tuple[float, float]):
        self.goals[goal_id] = goal_pos
