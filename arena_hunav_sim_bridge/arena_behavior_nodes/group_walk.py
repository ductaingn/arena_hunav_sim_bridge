from typing import Dict

import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaMultiAgentNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.group_walk import (
    GroupWalk as HNSGroupWalk,
)


@ArenaMultiAgentNode.register_node
@attrs.define
class GroupWalk(ArenaMultiAgentNode):
    main_agent: Agent
    non_main_agents: Dict[str, Agent]
    duration: float
    time_step: float = 0.1

    def to_bt_node(self, agent_name: str, **kwargs):
        non_main_agent_ids = "".join(
            f"{a.id}," for a in self.non_main_agents.values()
        ).strip(",")

        gw_node = HNSGroupWalk(
            self.main_agent.id,
            self.time_step,
            non_main_agent_ids,
            self.duration,
        )

        return gw_node
