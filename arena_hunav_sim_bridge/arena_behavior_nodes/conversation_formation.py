from typing import Dict

import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.ids_manager.goal_id_manager import GoalIDManager
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaMultiAgentNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.set_goal import SetGoal
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.conversation_formation import (
    ConversationFormation as HNSConversationFormation,
)
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.control_nodes import Sequence


@ArenaMultiAgentNode.register_node
@attrs.define
class ConversationFormation(ArenaMultiAgentNode):
    main_agent: Agent
    non_main_agents: Dict[str, Agent]
    conversation_duration: float
    target_x: float = attrs.field(
        metadata={"description": "Where conversation's central point will take place."}
    )
    target_y: float = attrs.field(
        metadata={"description": "Where conversation's central point will take place."}
    )
    time_step: float = 0.1
    goal_id: int = attrs.field(default=None, init=False)

    def to_bt_node(self, agent_name: str, *, goal_id_manager: GoalIDManager, **kwargs):
        non_main_agent_ids = "".join(
            f"{a.id}," for a in self.non_main_agents.values()
        ).strip(",")

        if self.goal_id is None:
            self.goal_id = goal_id_manager.get_goal_id()

        if agent_name == self.main_agent.name:
            set_goal_node = SetGoal(
                self.main_agent.id, self.target_x, self.target_y, self.goal_id
            )

            cf_node = HNSConversationFormation(
                self.main_agent.id,
                self.conversation_duration,
                self.goal_id,
                self.time_step,
                non_main_agent_ids,
            )

            control_node = Sequence(children_nodes=[set_goal_node, cf_node])

            return control_node

        else:
            cf_node = HNSConversationFormation(
                self.non_main_agents[agent_name].id,
                self.conversation_duration,
                self.goal_id,
                self.time_step,
                non_main_agent_ids,
            )

            return cf_node
