"""
Warning: This method now support Behavior Trees that have `Sequence` control nodes only
"""

from typing import Dict, List, Tuple
from copy import deepcopy
import time

from arena_simulation_setup.tree.World import WorldDescription

from arena_hunav_sim_bridge.agent.agent import Agent
from arena_hunav_sim_bridge.hunav_sim_node_wrapper import BTNode
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.go_to import GoTo
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.stop_and_wait_timer_action import (
    StopAndWaitTimerAction,
)
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.stop_movement import StopMovement
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.resume_movement import ResumeMovement
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.set_goal import SetGoal
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.set_group_id import SetGroupId
from arena_hunav_sim_bridge.hunav_sim_node_wrapper.control_nodes import (
    Sequence,
    Fallback,
)
from arena_hunav_sim_bridge.ids_manager.goal_id_manager import GoalIDManager
from arena_hunav_sim_bridge.global_planner.path_finder import (
    PathFinder,
    build_grid_from_world,
)


class Planner:
    """
    Global planner by building a graph of GoTo nodes and inserting waypoints between adjacent GoTo nodes.

    The planner:
    1. Builds a graph where nodes are GoTo nodes (only relevant for navigation)
    2. Ignores SetGoal, SetGroupID, and "do-nothing" nodes (StopAndWaitTimerAction, StopMovement, etc.) in the graph
    3. Uses control node connections (Sequence, Fallback) to determine adjacency
    4. Finds pairs of adjacent GoTo nodes
    5. Computes waypoints between them using PathFinder
    6. Inserts new SetGoal->GoTo pairs for intermediate waypoints
    """

    # Nodes that don't move the agent and should be ignored in the graph
    IGNORED_NODES = (
        SetGoal,
        SetGroupId,
        StopAndWaitTimerAction,
        StopMovement,
        ResumeMovement,
    )

    # Control nodes that structure the graph but aren't included in it
    CONTROL_NODES = (Sequence, Fallback)

    def __init__(
        self, agent: Agent, goal_id_manager: GoalIDManager, path_finder: PathFinder
    ) -> None:
        self.agent = agent
        self.goal_id_manager = goal_id_manager
        self.path_finder = path_finder
        self.planned_nodes = deepcopy(
            agent.nodes
        )  # Copy of original nodes to modify with waypoints

    def _is_ignored_node(self, node: BTNode) -> bool:
        """Check if a node should be ignored when building the graph."""
        return isinstance(node, self.IGNORED_NODES)

    def _is_control_node(self, node: BTNode) -> bool:
        """Check if a node is a control node (structures graph but not included)."""
        return isinstance(node, self.CONTROL_NODES)

    def _flatten_node_sequence(self, node: BTNode) -> List[BTNode]:
        """
        Flatten a node to a sequence of nodes, respecting control node structure.
        Control nodes are recursively flattened.

        Returns a list of all non-control nodes in traversal order.
        """
        if self._is_control_node(node) and hasattr(node, "children_nodes"):
            flattened = []
            for child in node.children_nodes:
                flattened.extend(self._flatten_node_sequence(child))
            return flattened
        else:
            return [node]

    def _find_parent_node(
        self, current_node: BTNode, node: BTNode
    ) -> Sequence | Fallback | None:
        """
        Find the parent node of a given node in the agent's node tree.
        Returns a list of parent nodes in traversal order.
        """
        if self._is_control_node(current_node) and hasattr(
            current_node, "children_nodes"
        ):
            if node in current_node.children_nodes:
                return current_node
            else:
                for child in current_node.children_nodes:
                    parent_node = self._find_parent_node(child, node)
                    if parent_node:
                        return parent_node
        else:
            return None

    def _build_goto_graph(
        self,
    ) -> Tuple[Dict[int, List[int]], List[BTNode], Dict[int, BTNode]]:
        """
        Build a graph where keys are GoTo node indices and values are adjacent GoTo nodes.
        Only GoTo nodes that are consecutive in significant_nodes are considered adjacent.

        Returns:
            Tuple of:
            - Dictionary mapping GoTo index to adjacent GoTo indices (only truly adjacent ones)
            - List of significant nodes in traversal order (non-ignored, non-control nodes)
        """
        # Step 1: Extract all nodes and flatten control structures
        all_nodes_flat = []
        for order in sorted(self.agent.nodes.keys()):
            node = self.agent.nodes[order]
            flattened = self._flatten_node_sequence(node)
            all_nodes_flat.extend(flattened)

        # Step 2: Build adjacency by filtering out ignored nodes
        significant_nodes = []  # Nodes that matter for navigation
        for node in all_nodes_flat:
            if not self._is_ignored_node(node):
                significant_nodes.append(node)

        # Step 3: Find GoTo nodes and their adjacent GoTo nodes
        # Only GoTo nodes that are consecutive in significant_nodes are adjacent
        goto_graph = {}
        goto_indices = [
            i for i, node in enumerate(significant_nodes) if isinstance(node, GoTo)
        ]

        for i, goto_idx in enumerate(goto_indices):
            adjacent = []

            # Find next GoTo node - only if it's the next element in significant_nodes
            if i + 1 < len(goto_indices):
                next_goto_idx = goto_indices[i + 1]
                if next_goto_idx == goto_idx + 1:
                    # Directly consecutive in significant_nodes, so truly adjacent
                    adjacent.append(next_goto_idx)

            goto_graph[goto_idx] = adjacent

        # print(f"Found {len(goto_indices)} GoTo nodes, with adjacency: {goto_graph}")
        return goto_graph, significant_nodes

    def _get_goal_position(self, goto_node: GoTo) -> Tuple[float, float]:
        """
        Get the goal position that a GoTo node is trying to reach.
        Retrieves position from goal_id_manager using the GoTo node's goal_id.

        Args:
            goto_node: The GoTo node to get the position for

        Returns:
            Tuple of (x, y) position, or None if goal_id not found
        """
        goal_id = goto_node.goal_id
        if goal_id in self.goal_id_manager.goals:
            return self.goal_id_manager.goals[goal_id]
        return None

    def plan(self):
        """
        Plan waypoints between adjacent GoTo nodes.

        Strategy:
        1. Build graph from ORIGINAL node structure (self.agent.nodes)
        2. Plan and insert waypoints between all adjacent GoTo pairs
           (inserting BEFORE the second GoTo to ensure it's reached)
        3. Plan from spawn to first GoTo (after all other insertions)
        4. Finalize by copying self.planned_nodes back to self.agent.nodes

        Uses self.planned_nodes as working copy to avoid modifying indices
        during iteration.
        """
        agent_waypoints = []
        # Build the graph from ORIGINAL nodes - this gives us valid indices
        goto_graph, significant_nodes = self._build_goto_graph()

        if not goto_graph or not significant_nodes:
            return agent_waypoints

        goto_indices = sorted(goto_graph.keys())

        # Step 1: Plan waypoints between adjacent GoTo pairs
        # Insert BEFORE the second GoTo to ensure it's reached
        for i in range(1, len(goto_indices) - 1):
            current_goto_idx = goto_indices[i]
            adjacent_indices = goto_graph[current_goto_idx]
            if not adjacent_indices:
                # print(f"No adjacent GoTo nodes found for GoTo at index {current_goto_idx}, skipping.")
                continue

            current_goto_node = significant_nodes[current_goto_idx]
            next_goto_idx = adjacent_indices[0]  # Assume first adjacent is the next one
            next_goto_node = significant_nodes[next_goto_idx]

            current_goal_pos = self._get_goal_position(current_goto_node)
            next_goal_pos = self._get_goal_position(next_goto_node)

            if current_goal_pos and next_goal_pos:
                waypoints = self.path_finder.get_waypoints(
                    current_goal_pos, next_goal_pos
                )
                agent_waypoints += waypoints
                waypoints = waypoints[1:-1]  # Trim start and end
                # print(f"Planning between positions {current_goal_pos} and {next_goal_pos} for GoTo nodes at indices {current_goto_idx} and {next_goto_idx}. Found waypoints: {waypoints}")

                if waypoints:
                    # Insert BEFORE the second GoTo node (pass the actual node object)
                    self._insert_waypoints_before_goto(next_goto_node, waypoints)

        # Step 2: Plan waypoints from spawn to first GoTo (after all other insertions)
        # This ensures we don't mess up indices with early insertions
        if goto_indices:
            start_pos = (self.agent.pos[0], self.agent.pos[1])
            first_goto_idx = goto_indices[0]
            if first_goto_idx == 0:
                goto_node: GoTo = significant_nodes[first_goto_idx]
                first_goal_pos = self._get_goal_position(goto_node)

                if first_goal_pos:
                    waypoints = self.path_finder.get_waypoints(
                        start_pos, first_goal_pos
                    )
                    agent_waypoints += waypoints
                    waypoints = waypoints[1:-1]  # Trim start and end
                    # print(f"Planning between positions {start_pos} and {first_goal_pos} for GoTo node at index {first_goto_idx}. Found waypoints: {waypoints}")

                    if waypoints:
                        self._insert_waypoints_before_goto(goto_node, waypoints)

        # Step 3: Finalize - update agent.nodes with planned modifications
        self.agent.nodes = self.planned_nodes

        return agent_waypoints

    def _insert_waypoints_before_goto(
        self, goto_node: GoTo, waypoints: List[Tuple[float, float]]
    ):
        """
        Insert waypoint nodes BEFORE a specific GoTo node.

        This is critical: inserting BEFORE the second GoTo ensures waypoints only execute
        when the second GoTo will be reached. If we inserted after the first GoTo, the
        waypoints might be unreachable (e.g., in a Fallback branch that doesn't execute).

        Args:
            goto_node: The actual GoTo node object to insert before
            waypoints: List of (x, y) tuples representing waypoint positions
        """
        new_nodes = []
        for x, y in waypoints:
            goal_id = self.goal_id_manager.get_goal_id()
            new_nodes.append(
                Sequence(
                    children_nodes=[
                        SetGoal(self.agent.id, x, y, goal_id),
                        GoTo(self.agent.id, goal_id),
                    ]
                )
            )
            self.goal_id_manager.update_goal_pos(goal_id, (x, y))

        # Find the order key of the goto_node in planned_nodes
        # We search by object identity to find the exact node
        parent_node = None
        # print(f"Looking for GoTo node to insert before: {goto_node}")
        for _, node in self.planned_nodes.items():
            # Find the parent node of the GoTo node
            parent_node = self._find_parent_node(node, goto_node)
            if parent_node:
                parent_node: Sequence
                for order, child_node in enumerate(parent_node.children_nodes):
                    if child_node == goto_node:
                        for new_node in new_nodes:
                            # print(f"Inserting new node {new_node} before GoTo node {goto_node} in parent node {parent_node}")
                            parent_node.children_nodes.insert(order, new_node)
                            order += 1  # Increment order for next insertion
                        break
                break

        if parent_node is None:
            raise ValueError(
                "Target GoTo node not found in planned nodes for insertion."
            )


class MultiAgentPlanner:
    def __init__(
        self,
        agents: List[Agent],
        goal_id_manager: GoalIDManager,
        world: WorldDescription,
    ):
        self.agents = agents
        self.goal_id_manager = goal_id_manager
        self.matrix, self.origin = build_grid_from_world(world)

    def plan(self):
        waypoints = {}
        start = time.time()
        for agent in self.agents:
            print("Planning for agent:", agent.name)
            # Rebuild PathFinder for each agent to ensure it has the correct grid and origin
            matrix = deepcopy(self.matrix.copy())
            origin = deepcopy(self.origin)
            path_finder = PathFinder(matrix=matrix, origin=origin)
            planner = Planner(agent, self.goal_id_manager, path_finder)
            agent_waypoints = planner.plan()
            if len(agent_waypoints) > 0:
                waypoints.update({agent.name: agent_waypoints})
        end = time.time()
        print(f"Multi-agent planning took {end - start:.2f} seconds.")

        return waypoints
