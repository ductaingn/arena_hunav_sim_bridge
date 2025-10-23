import attrs

from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaNode


@attrs.define
class GroupIDManager:
    """
    This class provide global IDs to the groups, so that the LLM doesn't have to.
    """

    group_id: int = attrs.field(default=0, init=False)

    def set_groups_ids(self, node: ArenaNode):
        """
        Set ID to all the nodes that need `group_id` field recursively
        """
        # if node has children then self.set_goals_ids(children)
        # if node has `group_id` fied then node.group_id = self.group_id ++
