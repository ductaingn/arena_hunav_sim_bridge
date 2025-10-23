from typing import Dict, List

import xml.etree.ElementTree as ET

import attrs

from arena_hunav_sim_bridge.bt_models.behavior_tree import Root, BehaviorTree
from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BTNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.control_nodes import Sequence
from arena_hunav_sim_bridge.bt_models.tree_nodes_models import Action, Condition


@attrs.define
class Agent:
    name: str
    pos: List  # [x, y, yaw (deg)]
    model: str
    waypoints: List[List]
    id: int = attrs.field(init=False)  # Will be provided later by AgentIDManger
    behavior_tree_root: Root = attrs.field(init=False)
    nodes: Dict[int, BTNode] = attrs.field(init=False, factory=dict)

    @behavior_tree_root.default
    def _behavior_tree_root_factory(self):
        main_tree_to_execute = f"{self.name}_behavior_tree"
        behavior_tree = BehaviorTree(ID=main_tree_to_execute)

        return Root(
            main_tree_to_execute=main_tree_to_execute,
            behavior_trees={main_tree_to_execute: behavior_tree},
        )

    def add_actions_conditions(
        self, actions: List[Action], conditions: List[Condition]
    ):
        existing_action_ids = {
            a.ID for a in self.behavior_tree_root.tree_nodes_model.actions
        }
        existing_condition_ids = {
            c.ID for c in self.behavior_tree_root.tree_nodes_model.conditions
        }

        for action in actions:
            if action.ID not in existing_action_ids:
                self.behavior_tree_root.tree_nodes_model.actions.append(action)
                existing_action_ids.add(action.ID)

        for condition in conditions:
            if condition.ID not in existing_condition_ids:
                self.behavior_tree_root.tree_nodes_model.conditions.append(condition)
                existing_condition_ids.add(condition.ID)

    def add_node(self, node: BTNode, order: int):
        self.nodes.update({order: node})

    def to_xml(self) -> ET.Element:
        """
        Convert to a XML behavior tree
        """
        nodes = []
        for order in range(len(self.nodes.values())):
            nodes.append(self.nodes[order])

        node = Sequence(children_nodes=nodes)

        bt_name = self.behavior_tree_root.main_tree_to_execute

        self.behavior_tree_root.behavior_trees[bt_name].child_node = node

        return self.behavior_tree_root.to_xml()
