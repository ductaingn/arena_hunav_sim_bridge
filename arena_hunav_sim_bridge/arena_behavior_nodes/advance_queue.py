from typing import Dict, List, Tuple
import numpy as np

import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaMultiAgentNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BTNode
from arena_hunav_sim_bridge.ids_manager.goal_id_manager import GoalIDManager
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.set_goal import SetGoal
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.go_to import GoTo
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.look_at_point import LookAtPoint
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.stop_and_wait_timer_action import (
    StopAndWaitTimerAction,
)
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.control_nodes import Sequence


@ArenaMultiAgentNode.register_node
@attrs.define
class AdvanceQueue(ArenaMultiAgentNode):
    agents: Dict[str, Agent]
    wait_duration: float
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
    distance: float = attrs.field(
        metadata={"description": "The distance between agents"}
    )
    agent_ordered: List[Agent] = attrs.field(init=False)
    waiting_poses: Dict[str, np.ndarray[float]] = attrs.field(
        init=False, metadata={"description": "The calculated poses of agents."}
    )
    goals_ids: Dict[str, int | None] = attrs.field(
        init=False,
        metadata={
            "description": "This dict contains the ID of each agent's initial position in the queue line. This must be assigned for every agent at once."
        },
    )
    point_to_look_at: Tuple[float, float] = attrs.field(
        init=False,
        metadata={
            "description": "Because HuNavSim social force model does not include yaw angle, so we need to create a point in front of the line to make agents look at it to adjust the yaw of agents for realisticity."
        },
    )

    def __attrs_post_init__(self):
        self.agent_ordered = list(self.agents.values())

        # Set waiting pose
        waiting_poses_dict = {}
        waiting_poses = []
        front_agent = self.agent_ordered[0]
        waiting_poses_dict.update(
            {front_agent.name: np.array(self.front_agent_pose[:2])}
        )
        waiting_poses.append(np.array(self.front_agent_pose[:2]))  # x,y

        direction = np.radians(self.direction)
        unit_vector = np.array([np.cos(direction), np.sin(direction)])

        self.point_to_look_at = (
            waiting_poses[0] - unit_vector * 4
        )  # 4[m] from the first position in the line

        for agent in self.agent_ordered[1:]:
            _distance = np.random.normal(
                max(self.distance, 1.5), 0.1
            )  # Make distance between agents a litle bit different from each other to look more realistic
            waiting_pose = waiting_poses[-1] + unit_vector * _distance
            waiting_poses_dict[agent.name] = waiting_pose
            waiting_poses.append(waiting_pose)

        self.waiting_poses = waiting_poses_dict

        wait_duration_dict = {}
        for agent in self.agent_ordered:
            wait_duration_dict[agent.name] = self.wait_duration

        self._wait_duration = wait_duration_dict

        goals_ids = {}
        for agent in self.agent_ordered:
            goals_ids.update({agent.name: None})

        self.goals_ids = goals_ids

    def _assign_goals_ids(self, goal_id_manager: GoalIDManager):
        self.goals_ids["point_to_look_at"] = goal_id_manager.get_goal_id()

        for agent in self.agent_ordered:
            goal_id = goal_id_manager.get_goal_id()
            self.goals_ids[agent.name] = goal_id

    def to_bt_node(self, agent_name: str, *, goal_id_manager: GoalIDManager, **kwargs):
        agent: Agent = self.agents[agent_name]
        agent_index = self.agent_ordered.index(agent)

        if None in self.goals_ids.values():
            self._assign_goals_ids(goal_id_manager)

        # Initial position in the queue
        set_goal_node = SetGoal(
            agent_id=agent.id,
            target_x=self.waiting_poses[agent_name][0],
            target_y=self.waiting_poses[agent_name][1],
            goal_id=self.goals_ids[agent.name],
        )
        goal_id_manager.update_goal_pos(
            self.goals_ids[agent.name],
            (self.waiting_poses[agent_name][0], self.waiting_poses[agent_name][1]),
        )

        go_to_node = GoTo(agent_id=agent.id, goal_id=self.goals_ids[agent.name])

        sawta_node = StopAndWaitTimerAction(
            agent_id=agent.id, wait_duration=self._wait_duration[agent_name]
        )
        nodes: List[BTNode] = [set_goal_node, go_to_node, sawta_node]

        # Each agent waits until the agent in front of it move, then moves to that position, until it reaches the front of the queue line
        for index in reversed(range(agent_index)):
            # Get the initial waiting position of the agent ahead
            agent_ahead = self.agent_ordered[index]
            nodes.append(
                GoTo(agent_id=agent.id, goal_id=self.goals_ids[agent_ahead.name])
            )
            nodes.append(
                StopAndWaitTimerAction(
                    agent_id=agent.id, wait_duration=self._wait_duration[agent_name]
                )
            )

        control_node = Sequence(children_nodes=nodes)

        return control_node

    def to_xml(self):
        raise ValueError(
            "This node includes more than one agents therefore can not be converted to XML directly!"
        )
