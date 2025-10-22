import attrs

from .base_node import BaseNode


@attrs.define
class StopAndWaitTimerAction(BaseNode):
    agent_id: int
    wait_duration: float

    def get_actions_conditions(self):
        ...