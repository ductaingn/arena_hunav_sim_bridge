import attrs

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.arena_behavior_nodes import ArenaSingleAgentNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.stop_and_wait_timer_action import (
    StopAndWaitTimerAction as HNSStopAndWaitTimerAction,
)


@ArenaSingleAgentNode.register_node
@attrs.define
class StopAndWaitTimerAction(ArenaSingleAgentNode):
    agent: Agent
    wait_duration: float

    def to_bt_node(self, **kwargs):
        sm_node = HNSStopAndWaitTimerAction(self.agent.id, self.wait_duration)

        return sm_node
