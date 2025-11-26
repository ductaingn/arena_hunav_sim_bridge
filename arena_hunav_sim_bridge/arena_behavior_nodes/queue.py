from typing import Dict, List
import numpy as np

import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaMultiAgentNode
from arena_hunav_sim_bridge.ids_manager.goal_id_manager import GoalIDManager
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.set_goal import SetGoal
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.go_to import GoTo
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.stop_and_wait_timer_action import (
    StopAndWaitTimerAction,
)
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.control_nodes import Sequence


@ArenaMultiAgentNode.register_node
@attrs.define
class Queue(ArenaMultiAgentNode):
    agents: Dict[str, Agent]
    wait_duration: List[float]
    _wait_duration: Dict[str, float] = attrs.field(init=False)
    front_agent_pose: List[float] = attrs.field(
        metadata={
            "description": "The pose of the agent in the front of the queue, the pose of agents behind will be calculated base on this agent's pose and queue direction"
        }
    )
    direction: float = attrs.field(
        metadata={
            "description": "The direction of the queue line given in yaw angle, the pose of agents will be calculated base on this attribute and front agent's pose"
        }
    )
    distance: List[float] = attrs.field(
        metadata={"description": "The distance between each agents"}
    )
    waiting_poses: Dict[int, np.ndarray[float, float, float]] = attrs.field(
        init=False, metadata={"description": "The calculated poses of agents."}
    )

    @waiting_poses.default
    def _set_waiting_pose(self):
        waiting_poses_dict = {}
        waiting_poses = []
        front_agent = list(self.agents.values())[0]
        waiting_poses_dict.update(
            {front_agent.name: np.array(self.front_agent_pose[:2])}
        )
        waiting_poses.append(np.array(self.front_agent_pose[:2]))  # x,y

        direction = np.radians(self.direction)
        unit_vector = np.array([np.cos(direction), np.sin(direction)])

        for agent in list(self.agents.values())[1:]:
            distance = np.random.normal(self.distance, 0.1) # Make distance between agents a litle bit different from each other to look more realistic
            waiting_pose = waiting_poses[-1] + unit_vector * distance
            waiting_poses_dict[agent.name] = waiting_pose
            waiting_poses.append(waiting_pose)

        return waiting_poses_dict

    @_wait_duration.default
    def _wait_duration_factory(self):
        wait_duration_dict = {}
        for index, agent in enumerate(list(self.agents.values())):
            wait_duration_dict[agent.name] = self.wait_duration[index]

        return wait_duration_dict

    def to_bt_node(self, agent_name: str, *, goal_id_manager: GoalIDManager, **kwargs):
        agent: Agent = self.agents[agent_name]

        goal_id = goal_id_manager.get_goal_id()

        set_goal_node = SetGoal(
            agent_id=agent.id,
            target_x=self.waiting_poses[agent_name][0],
            target_y=self.waiting_poses[agent_name][1],
            goal_id=goal_id,
        )

        go_to_node = GoTo(agent_id=agent.id, goal_id=goal_id)

        sawta_node = StopAndWaitTimerAction(
            agent_id=agent.id, wait_duration=self._wait_duration[agent_name]
        )

        control_node = Sequence(children_nodes=[set_goal_node, go_to_node, sawta_node])

        return control_node

    def to_xml(self):
        raise ValueError(
            "This node includes more than one agents therefore can not be converted to XML directly!"
        )
