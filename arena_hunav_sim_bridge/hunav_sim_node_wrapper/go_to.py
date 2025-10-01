import attrs

from .base_node import BaseNode


@attrs.define
class GoTo(BaseNode):
    agent_id: int
    time_step: float
    goal_id: int
    tolerance: float

    def to_xml(self):
        ...