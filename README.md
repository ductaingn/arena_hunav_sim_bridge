# A tool to turn LLM responses into complicate XML Behavior Trees via automatic parsing

## 1. How to use
Example usage:
```python
from arena_hunav_sim_bridge.agent.llm_parser import Parser


llm_output: str = ...

config = {
    "obstacles": {
        "static": [],
        "dynamic": []
    }
}

# Initialize parser
parser = Parser(llm_output)
# Parse `llm_output` to arena_hunav_sim_bridge.Agent
parser.parse()

# Retrieve agents
for hunav_agent in parser.agents.values():
    hunav_config = {
        "id": hunav_agent.id,
        "name": hunav_agent.name,
        "pos": hunav_agent.pos,
        "model": hunav_agent.model,
        "waypoints": hunav_agent.waypoints
    }

    # Export behavior tree from parsed agent
    behavior_tree_xml = hunav_agent.to_xml()

    tmp_xml_file = tempfile.NamedTemporaryFile(
        mode='w+t',
        suffix='.xml',
        dir=self.tmp_dir.name,
        delete=False
    )

    tmp_xml_file.write(
        ET.tostring(
            behavior_tree_xml,
            encoding="UTF-8",
            method='xml',
            xml_declaration=True
        ).decode("utf-8")
    )

    hunav_config.update({
        "behavior_tree": tmp_xml_file.name
    })

    config["obstacles"]["dynamic"].append(hunav_config)
```

## 2. How to add a new behavior node
### 2.1. Define an `ArenaNode` in the folder `arena_behavior_nodes`
- If your node describe a behavior that involed more than one HuNav agents, you should inherit from `arena_hunav_sim_bridge.arena_behavior_nodes.ArenaMultiAgentNode`, otherwise use `arena_hunav_sim_bridge.arena_behavior_nodes.ArenaSingleAgentNode`.
- Remember to register it using `@ArenaSingleAgentNode.register_node` or `@ArenaMultiAgentNode.register_node`, see `arena_hunav_sim_bridge/arena_hunav_sim_bridge/arena_behavior_nodes/approach_agent.py` for example. Then import that node in `arena_hunav_sim_bridge/arena_hunav_sim_bridge/arena_behavior_nodes/__init__.py`.
- Design a new behavior using the available HuNavSim nodes wrapper from `arena_hunav_sim_bridge/arena_hunav_sim_bridge/hunav_sim_node_wrapper`

### 2.2. Check if your node is compatible
- See `arena_hunav_sim_bridge/arena_hunav_sim_bridge/agent/llm_parser.py` if your node can be parsed by `Parser`. Pay attention to these attribute: `agent_name`, `main_agent_name`, e.t.c, that map the agents.

### 2.3. Test your node
- Use `arena_hunav_sim_bridge/arena_hunav_sim_bridge/agent/llm_parser.py` to test if your node is parsed correctly.

### 2.4. Add the node to the reference
- Add the node name, description, input and output description to `arena_hunav_sim_bridge/arena_hunav_sim_bridge/HuNavSim_BT_Reference_Structured.json`