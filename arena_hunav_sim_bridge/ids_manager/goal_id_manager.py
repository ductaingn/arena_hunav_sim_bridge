import attrs


@attrs.define
class GoalIDManager:
    """
    This class provide global IDs to the goals, so that the LLM doesn't have to.
    """

    goal_id: int = attrs.field(default=0, init=False)

    def get_goal_id(self):
        goal_id = self.goal_id
        self.goal_id += 1

        return goal_id
