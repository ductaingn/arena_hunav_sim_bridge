from typing import Dict, List

import attrs

from ..agent.agent import Agent


@attrs.define
class AgentIDManager:
    """
    Since HuNavSim only takes in `agent_id` as interger, this class provide IDs to the agents
    """

    agent_id: int = attrs.field(default=0, init=False)

    def get_agent_id(self):
        agent_id = self.agent_id
        self.agent_id += 1

        return agent_id
