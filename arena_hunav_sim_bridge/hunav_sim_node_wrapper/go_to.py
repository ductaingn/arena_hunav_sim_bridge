import attrs

from .base_node import BaseNode


@attrs.define
class GoTo(BaseNode):
    agent_id: int
    time_step: float = 0.1
    goal_id: int
    tolerance: float = 1

    def get_actions_conditions(self):
        ...