from typing import List, Tuple

import numpy as np

import shapely.geometry as geom

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathfinding3d.core.diagonal_movement import DiagonalMovement
from pathfinding3d.core.grid import Grid
from pathfinding3d.finder.theta_star import ThetaStarFinder

from arena_simulation_setup.tree.World import World

def build_grid_from_world(world: World, resolution: float = 0.1) -> Tuple[np.ndarray, Tuple[float, float]]:
    """
    Converts World description into a 3D numpy grid for Pathfinding3D.
    resolution: size of one grid cell in meters (0.1 = 10cm)
    """
    # 1. Determine World Bounds
    world_descr = world.load()
    xmin, ymin, xmax, ymax = np.inf, np.inf, -np.inf, -np.inf
    for zone in world_descr.zones:
        xmin = min(xmin, zone.floor.pos.x - zone.floor.x_length / 2)
        xmax = max(xmax, zone.floor.pos.x + zone.floor.x_length / 2)
        ymin = min(ymin, zone.floor.pos.y - zone.floor.y_length / 2)
        ymax = max(ymax, zone.floor.pos.y + zone.floor.y_length / 2)

    # 2. Initialize 3D Matrix (Width, Height=1, Depth)
    # We use (x, z, y) logic to match Pathfinding3D's (x, y, z)
    width = int(np.ceil((xmax - xmin) / resolution))
    depth = int(np.ceil((ymax - ymin) / resolution))
    matrix = np.ones((width, 1, depth), dtype=np.int8)  # 1 = walkable

    def world_to_grid(x, y):
        gx = int((x - xmin) / resolution)
        gy = int((y - ymin) / resolution)
        return gx, gy

    # 3. Burn Obstacles into Matrix
    # We'll use your existing wall conversion logic but fill the grid
    for zone in world_descr.zones:
        for wall in zone.walls:
            # Create a Shapely polygon for the wall (inflated by wall thickness)
            # You can also inflate by robot_radius here for safety!
            start = np.array([wall.start.x, wall.start.y])
            end = np.array([wall.end.x, wall.end.y])
            line = geom.LineString([start, end])
            # Inflate wall + robot safety margin
            obstacle_poly = line.buffer(0.2)

            # Find cells covered by this obstacle
            o_xmin, o_ymin, o_xmax, o_ymax = obstacle_poly.bounds
            gx1, gy1 = world_to_grid(o_xmin, o_ymin)
            gx2, gy2 = world_to_grid(o_xmax, o_ymax)

            # Clip to matrix bounds
            for ix in range(max(0, gx1), min(width, gx2 + 1)):
                for iz in range(max(0, gy1), min(depth, gy2 + 1)):
                    # Check if cell center is inside the polygon
                    cell_pt = geom.Point(
                        xmin + ix * resolution, ymin + iz * resolution
                    )
                    if obstacle_poly.contains(cell_pt):
                        matrix[ix, 0, iz] = 0  # 0 = obstacle

    return matrix, (xmin, ymin)
      

class PathFinder:
    def __init__(self, matrix: np.ndarray, origin: Tuple[float, float], resolution: float = 0.1) -> None:
        self.resolution = resolution
        self.matrix = matrix
        self.origin = origin
        self.grid = Grid(matrix=self.matrix)
        self.finder = ThetaStarFinder(diagonal_movement=DiagonalMovement.always)
    
    def visualize_path(self, path, origin, resolution):
        """
        Visualizes the occupancy grid and the resulting Theta* path.
        """
        # 1. Matplotlib 2D Top-down view
        plt.figure(figsize=(10, 12))

        # Plot the grid (transpose to align axes: [width, depth])
        # We show the 0th slice of our 3D matrix
        plt.imshow(
            self.matrix[:, 0, :].T,
            origin="lower",
            cmap="Greys",
            extent=[
                origin[0],
                origin[0] + self.matrix.shape[0] * resolution,
                origin[1],
                origin[1] + self.matrix.shape[2] * resolution,
            ],
        )

        # Plot Path
        if path:
            path_x = [p[0] for p in path]
            path_y = [p[1] for p in path]
            plt.plot(path_x, path_y, "g-", linewidth=2, label="Theta* Path")
            plt.scatter(path_x, path_y, color="green", s=10)

        plt.title("Theta* Grid and Any-Angle Path")
        plt.xlabel("X (meters)")
        plt.ylabel("Y (meters)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig("path_debug.png")

    def get_waypoints(
        self, start_pos: Tuple[float, float], goal_pos: Tuple[float, float]
    ) -> List[Tuple[float, float]]:
        def to_grid_coords(pos, origin, res):
            return int((pos[0] - origin[0]) / res), 0, int((pos[1] - origin[1]) / res)

        # Reset the grid to clear any stale state from previous pathfinding calls
        # This prevents KeyError in the pathfinder's heap when making multiple queries
        self.grid.cleanup()
        
        start_node = self.grid.node(
            *to_grid_coords(start_pos, self.origin, self.resolution)
        )
        end_node = self.grid.node(
            *to_grid_coords(goal_pos, self.origin, self.resolution)
        )

        path_nodes, _ = self.finder.find_path(start_node, end_node, self.grid)

        world_path = [
            (
                self.origin[0] + n.x * self.resolution,
                0.0,
                self.origin[1] + n.z * self.resolution,
            )
            for n in path_nodes
        ]

        path = [(p[0], p[2]) for p in world_path]

        return path

if __name__ == "__main__":
    from pathlib import Path
    world_path = "/home/linh/ductai_nguyen_ws/Arena_ws/install/arena_simulation_setup/share/arena_simulation_setup/worlds/hospital_1"
    world = World(path=Path(world_path))
    matrix, origin = Grid.build_grid_from_world(world)
    path_finder = PathFinder(Grid(matrix=matrix, origin=origin))
    start = (8.5, 2.0)
    goal = (4.0, 1.0)
    waypoints = path_finder.get_waypoints(start, goal)
    print("Waypoints:", waypoints)
    path_finder.visualize_path(waypoints, path_finder.origin, path_finder.resolution)