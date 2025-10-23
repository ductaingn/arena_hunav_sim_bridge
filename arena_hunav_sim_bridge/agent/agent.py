from typing import Dict, List

import xml.etree.ElementTree as ET

import attrs

from arena_hunav_sim_bridge.bt_models.behavior_tree import Root, BehaviorTree
from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BTNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.control_nodes import Sequence


@attrs.define
class Agent:
    name: str
    pos: List  # [x, y, yaw (deg)]
    model: str
    waypoints: List[List]
    id: int = attrs.field(init=False)  # Will be provided later by AgentIDManger
    behavior_tree_root: Root = attrs.field(init=False)
    nodes: Dict[int, BTNode] = attrs.field(init=False, default={})

    @behavior_tree_root.default
    def _behavior_tree_root_factory(self):
        return Root(
            main_tree_to_execute=f"{self.name}_behavior_tree",
        )

    def add_actions_conditions(self, actions, conditions):
        for action in actions:
            self.behavior_tree_root.tree_nodes_model.actions.append(action)
        for condition in conditions:
            self.behavior_tree_root.tree_nodes_model.conditions.append(condition)

    def add_node(self, node: BTNode, order: int):
        self.nodes.update({order: node})

    def to_xml(self) -> ET.Element:
        """
        Convert to a XML behavior tree
        """
        nodes = []
        for order in range(len(self.nodes.values())):
            # TODO: parse this correctly
            nodes.append(self.nodes[order])

        node = Sequence(children_nodes=nodes)

        bt_name = self.behavior_tree_root.main_tree_to_execute
        behavior_tree = BehaviorTree(child_node=node)
        self.behavior_tree_root.behavior_trees[bt_name] = behavior_tree

        return self.behavior_tree_root.to_xml()
