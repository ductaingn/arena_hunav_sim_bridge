from typing import Dict, List

import xml.etree.ElementTree as ET

import attrs

from arena_hunav_sim_bridge.bt_models.bt_models import Root, ActionNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.base_node import BTNode


@attrs.define
class Agent:
    name: str
    pos: List # [x, y, yaw (deg)]
    model: str
    waypoints: List[List]
    id: int = attrs.field(init=False) # Will be provided later by AgentIDManger
    behavior_tree_root: Root = attrs.field(init=False)
    nodes: Dict[int, BTNode] = attrs.field(init=False)

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
    
    def add_node(self, node: BTNode, order:int):
        self.nodes.update({
            order, node
        })

    def to_xml(self)->ET.Element:
        """
        Convert to a XML behavior tree
        """
        for order in range(len(self.nodes)):
            # TODO: parse this correctly
            node = self.nodes[f"{order}"]
            
            self.behavior_tree_root.behavior_trees.append(ActionNode(node))
            
        return self.behavior_tree_root.to_xml()
        
        