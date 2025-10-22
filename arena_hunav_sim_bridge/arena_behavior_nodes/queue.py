from typing import Dict, List
import numpy as np

import attrs

from ..agent.agent import Agent
from ..bt_models.bt_models import ControlNode
from ..ids_manager.goal_id_manager import GoalIDManager
from ..hunav_sim_node_wrapper.base_node import ArenaMultiAgentNode, BehaviorTree
from ..hunav_sim_node_wrapper.set_goal import SetGoal
from ..hunav_sim_node_wrapper.go_to import GoTo
from ..hunav_sim_node_wrapper.stop_and_wait_timer_action import StopAndWaitTimerAction


@attrs.define
class Queue(ArenaMultiAgentNode):
    agents: Dict[int, Agent]
    wait_duration: Dict[int, float]
    front_agent_pose: List[float] = attrs.field(
        metadata={"description":"The pose of the agent in the front of the queue, the pose of agents behind will be calculated base on this agent's pose and queue direction"}
    )
    direction: float = attrs.field(
        metadata={"description":"The direction of the queue (yaw angle) in degree, the pose of agents will be calculated base on this attribute and front agent's pose"}
    )
    distances: List[float] = attrs.fields(
        metadata={"description":"The distance between each agents"}
    )
    waiting_poses: Dict[int, np.ndarray] = attrs.field(
        init=False,
        metadata={"description":"The calculated poses of agents."}
    )

    def set_waiting_pose(self):
        waiting_poses = []
        waiting_poses.append(np.array(self.front_agent_pose[:1])) # x,y

        direction = np.radians(self.direction)
        unit_vector = np.array([np.arccos(direction), np.arcsin(direction)])

        for index, (agent_id, agent) in enumerate(self.agents.items()[1:]):
            waiting_pose = waiting_poses[-1] + unit_vector*self.distances[index]
            self.waiting_poses[agent_id]
            waiting_poses.append(waiting_pose)
    
    def to_bt_node(self, agent_id: int, *, goal_id_manager: GoalIDManager, **kwargs):
        agent: Agent = self.agents[agent_id]

        set_goal_node = SetGoal(
            agent_id=agent.id,
            target_x=self.waiting_poses[agent_id][0],
            target_y=self.waiting_poses[agent_id][1],
        )

        goal_id_manager.set_goals_id(set_goal_node)

        go_to_node = GoTo(
            agent_id=agent.id,
            goal_id=set_goal_node.goal_id
        )

        sawta_node = StopAndWaitTimerAction(
            agent_id=agent.id,
            wait_duration=self.wait_duration[agent_id]
        )
        
        control_node = ControlNode(
            ID="Sequence",
            children_nodes=[
                set_goal_node,
                go_to_node,
                sawta_node
            ]
        )

        return control_node


    def to_xml(self):
        raise ValueError("This node includes more than one agents therefore can not be converted to XML directly!")