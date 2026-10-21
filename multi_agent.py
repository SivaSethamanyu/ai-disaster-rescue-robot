"""
Advanced Multi-Agent Planning and Conflict Resolution Engine.
Supports prioritized cooperative planning for 2 to N agents,
dynamic target allocation, space-time reservation table management,
and telemetry metrics.
"""

from typing import List, Tuple, Set, Dict, Optional
from astar import astar_search, spacetime_astar_search, Coord, SpaceTimeState, manhattan_distance


class MultiAgentCoordinator:
    """
    Central Coordinator for Multi-Robot Rescue Missions.
    Manages:
    - Target Decomposition & Allocation
    - Prioritized Space-Time Path Planning for N agents
    - Vertex and Edge Collision Prevention
    - Dynamic Conflict Resolution & Analytics
    """
    
    def __init__(self, cols: int, rows: int):
        self.cols = cols
        self.rows = rows
        self.vertex_reservations: Set[SpaceTimeState] = set()
        self.swap_reservations: Set[Tuple[int, int, int, int, int]] = set()
        self.conflict_logs: List[str] = []
        self.total_conflicts_resolved = 0
        self.total_compute_time_ms = 0.0

    def allocate_targets(
        self,
        robot_starts: List[Coord],
        victims: List[Coord],
        obstacles: Set[Coord]
    ) -> List[Tuple[int, Coord]]:
        """
        Assigns each robot to an optimal victim target minimizing cumulative distance.
        """
        if len(robot_starts) == len(victims) and len(robot_starts) == 2:
            d1 = manhattan_distance(robot_starts[0], victims[0]) + manhattan_distance(robot_starts[1], victims[1])
            d2 = manhattan_distance(robot_starts[0], victims[1]) + manhattan_distance(robot_starts[1], victims[0])
            if d1 <= d2:
                return [(0, victims[0]), (1, victims[1])]
            else:
                return [(0, victims[1]), (1, victims[0])]
        
        # Greedy assignment for N agents
        unassigned_victims = list(victims)
        assignments = []
        for r_id, r_pos in enumerate(robot_starts):
            if not unassigned_victims:
                break
            best_victim = min(unassigned_victims, key=lambda v: manhattan_distance(r_pos, v))
            assignments.append((r_id, best_victim))
            unassigned_victims.remove(best_victim)
        return assignments

    def plan_coordinated_paths(
        self,
        robot_starts: List[Coord],
        target_assignments: List[Tuple[int, Coord]],
        obstacles: Set[Coord],
        algorithm: str = "A*",
        heuristic_name: str = "Manhattan"
    ) -> Dict[int, Dict]:
        """
        Performs Prioritized Multi-Agent Planning for N agents:
        - Agent 0 plans first using selected algorithm and heuristic.
        - Agents 1..N sequentially plan using Space-Time A* around prior reservations.
        """
        self.vertex_reservations.clear()
        self.swap_reservations.clear()
        self.conflict_logs.clear()
        self.total_compute_time_ms = 0.0
        results = {}

        num_agents = len(robot_starts)
        
        for agent_idx in range(num_agents):
            start_pos = robot_starts[agent_idx]
            # Find assigned target
            assigned_target = next((tgt for r_id, tgt in target_assignments if r_id == agent_idx), None)
            if not assigned_target:
                assigned_target = start_pos

            if agent_idx == 0:
                # Priority 0 Agent: Search with selected algorithm
                path, explored, comp_time = astar_search(
                    start_pos, assigned_target, obstacles, self.cols, self.rows,
                    algorithm=algorithm, heuristic_name=heuristic_name
                )
                waits = 0
            else:
                # Follower Agents: Space-Time A* respecting all previous reservations
                path, explored, waits, comp_time = spacetime_astar_search(
                    start_pos,
                    assigned_target,
                    obstacles,
                    self.vertex_reservations,
                    self.swap_reservations,
                    self.cols,
                    self.rows,
                    heuristic_name=heuristic_name
                )
                if not path:
                    path, explored, comp_time = astar_search(
                        start_pos, assigned_target, obstacles, self.cols, self.rows,
                        algorithm=algorithm, heuristic_name=heuristic_name
                    )
                    waits = 0

            self.total_compute_time_ms += comp_time

            if not path:
                path = [start_pos]
                explored = {start_pos}

            conflicts_avoided = waits
            if waits > 0:
                self.conflict_logs.append(f"Robot {agent_idx + 1} yielded {waits} wait-step(s) for higher priority agent.")
                self.total_conflicts_resolved += waits

            results[agent_idx] = {
                "path": path,
                "explored": explored,
                "waits": waits,
                "length": len(path),
                "conflicts_avoided": conflicts_avoided,
                "compute_time_ms": comp_time
            }

            # Register trajectory in Space-Time reservations
            for t, coord in enumerate(path):
                self.vertex_reservations.add((coord[0], coord[1], t))
                if t > 0:
                    prev = path[t - 1]
                    self.swap_reservations.add((coord[0], coord[1], prev[0], prev[1], t - 1))

            # Maintain reservation at target cell after arrival
            if path:
                gx, gy = path[-1]
                for t_after in range(len(path), len(path) + 80):
                    self.vertex_reservations.add((gx, gy, t_after))

        return results

    def check_dynamic_conflict(self, pos_list: List[Coord], next_list: List[Coord]) -> Optional[Tuple[int, int]]:
        """
        Checks for dynamic runtime conflicts among all agent pairs.
        Returns (agent_i, agent_j) if a conflict is detected, else None.
        """
        n = len(pos_list)
        for i in range(n):
            for j in range(i + 1, n):
                # Vertex conflict
                if next_list[i] == next_list[j]:
                    return (i, j)
                # Swap conflict
                if next_list[i] == pos_list[j] and next_list[j] == pos_list[i]:
                    return (i, j)
        return None
