from typing import List, Dict
import json
import xml.etree.ElementTree as ET

import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.base_node import ArenaSingleAgentNode, ArenaMultiAgentNode
from arena_hunav_sim_bridge.ids_manager.agent_id_manager import AgentIDManager
from arena_hunav_sim_bridge.ids_manager.goal_id_manager import GoalIDManager
from arena_hunav_sim_bridge.ids_manager.group_id_manager import GroupIDManager

@attrs.define
class Parser:
    llm_res: str
    agents: Dict[int, Agent] = attrs.field(init=False)
    single_agent_nodes: List[ArenaSingleAgentNode] = attrs.field(init=False)
    multi_agent_nodes: List[ArenaMultiAgentNode] = attrs.field(init=False)


    @agents.default
    def _agent_factory(self) -> Dict[int, Agent]:
        llm_res: Dict = json.loads(self.llm_res)
        agents_json: List[Dict] = llm_res.pop("hunav_agents")
        agent_id_manager = AgentIDManager()

        agents: Dict[str, Agent] = []
        for agent_json in agents_json:
            agent = Agent(
                    agent_json["name"],
                    agent_json["pos"],
                    agent_json["model"],
                    agent_json["waypoints"]
                )
            agent_id_manager.set_agent_id(agent)
            agents.update({
                agent.id: agent
            })

        return agents
    
    def parse(self) -> List[ET.ElementTree]:
        goal_id_manager = GoalIDManager()
        group_id_manager = GroupIDManager()

        llm_res: Dict = json.loads(self.llm_res)
        single_agent_nodes_json: List[Dict] = llm_res.pop("single_agent_nodes")
        multi_agent_nodes_json: List[Dict] = llm_res.pop("multi_agent_nodes")

        for node_json in single_agent_nodes_json:
            node_cls = node_json["name"]
            agent_name: str = node_json["agent_name"]
            agent = self.agents[agent_name]
            node_order: int = node_json["order"]
            node_attributes: Dict = node_json["attributes"]

            node: ArenaSingleAgentNode = ArenaSingleAgentNode.from_json(**node_attributes)
            bt_node = node.to_bt_node()
            actions, conditions = bt_node.get_actions_conditions()

            agent.add_actions_conditions(actions, conditions)
            agent.add_node(node, node_order)
        
        for node_json in multi_agent_nodes_json:
            node_cls = node_json["name"]
            agents_names: List[str] = node_json["agents_names"]
            nodes_orders: Dict[str, int] = node_json["orders"]
            agents: Dict[str, Agent] = {}
            for a_n in agents_names:
                for a_id, agent in self.agents.items():
                    if a_n == agent.name:
                        agents.update({
                            a_id: agent
                        })

            node_attributes: Dict = node_json["attributes"]
            node_attributes.update({
                "agents": agents
            })
            node: ArenaMultiAgentNode = ArenaMultiAgentNode.from_json(node_cls, **node_attributes)

            for agent in agents.values():
                bt_node = node.to_bt_node(
                    agent.id,
                    goal_id_manager=goal_id_manager,
                    group_id_manager=group_id_manager
                )
                actions, conditions = bt_node.get_actions_conditions()

                agent.add_actions_conditions(actions, conditions)
                agent.add_node(node, nodes_orders[agent.name])

        for agent in self.agents.values():
            agent.to_xml()
            
if __name__ == "__main__":
    with open("/home/linh/ductai_nguyen_ws/arena6_ws/src/deps/hunav/arena_hunav_sim_bridge/arena_hunav_sim_bridge/agent/example_llm_response.json", "rt") as file:
        llm_res = file.read()

    parser = Parser(llm_res)

    behavior_trees: List = parser.parse()
    