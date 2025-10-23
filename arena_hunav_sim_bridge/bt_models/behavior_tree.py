import xml.etree.ElementTree as ET
from typing import Dict
import attrs

from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BTNode
from .tree_nodes_models import TreeNodesModel


@attrs.define
class BehaviorTree:
    child_node: BTNode

    def to_xml(self) -> ET.Element:
        element = ET.Element("BehaviorTree", attrib={"ID": self.__class__.__name__})

        element.append(self.child_node.to_xml())

        return element


@attrs.define
class Root:
    main_tree_to_execute: str
    BTCPP_format: str = "4"
    tree_nodes_model: TreeNodesModel = TreeNodesModel()
    behavior_trees: Dict[str, BehaviorTree] = {}

    def to_xml(
        self,
        include_ros_pkg: str = "arena_simulation_setup",
        include_path: str = "configs/hunav/behavior_trees/BTRegularNav.xml",
    ) -> ET.Element:
        element = ET.Element(
            "root",
            attrib={
                "main_tree_to_execute": self.main_tree_to_execute,
                "BTCPP_format": self.BTCPP_format,
            },
        )

        element.append(self.tree_nodes_model.to_xml())

        element.append(
            ET.Element(
                "include", attrib={"ros_pkg": include_ros_pkg, "path": include_path}
            )
        )

        for bt_name, behavior_tree in self.behavior_trees.items():
            element.append(behavior_tree.to_xml())

        return element


if __name__ == "__main__":
    from xml.dom import minidom
    from context import behavior_tree_format

    json_str = (
        behavior_tree_format.strip()
        .strip("Output must strictly follow this structure:")
        .strip("\n    ```json")
        .strip("\n    ```\n    Do NOT explain anything. Output JSON only.")
    )

    test = Root.model_validate_json(json_str)

    xml_str = test.to_xml()
    pretty_bytes = minidom.parseString(
        ET.tostring(xml_str, encoding="UTF-8")
    ).toprettyxml(indent="  ", encoding="UTF-8")

    pretty_str = pretty_bytes.decode("UTF-8")
    print(pretty_str)
