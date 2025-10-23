import attrs

from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaNode


@attrs.define
class GroupIDManager:
    """
    This class provide global IDs to the groups, so that the LLM doesn't have to.
    """

    group_id: int = attrs.field(default=0, init=False)

    def get_groups_ids(self):
        group_id = self.group_id
        self.group_id += 1

        return group_id
