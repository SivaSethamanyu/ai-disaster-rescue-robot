"""
Advanced Multi-Algorithm Pathfinding and Heuristics Benchmark Module.
Supports live algorithm switching and comparative benchmarks:
- A* Search (Optimal & Heuristic Guided)
- Dijkstra's Algorithm (Uniform Cost Search)
- Greedy Best-First Search (Suboptimal Fast Heuristic)
- Breadth-First Search (BFS, Uninformed Queue)
Heuristics supported:
- Manhattan Distance (L1 Norm)
- Euclidean Distance (L2 Norm)
- Chebyshev Distance (L-infinity Norm)
"""

import time
import math
import heapq
from collections import deque
from typing import List, Tuple, Set, Dict, Optional, Callable

Coord = Tuple[int, int]
SpaceTimeState = Tuple[int, int, int]  # (x, y, t)


# --- HEURISTIC FUNCTIONS ---
def manhattan_distance(p1: Coord, p2: Coord) -> float:
    """L1 Norm: |x1 - x2| + |y1 - y2|."""
    return float(abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]))


def euclidean_distance(p1: Coord, p2: Coord) -> float:
    """L2 Norm: sqrt((x1 - x2)^2 + (y1 - y2)^2)."""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def chebyshev_distance(p1: Coord, p2: Coord) -> float:
    """L-infinity Norm: max(|x1 - x2|, |y1 - y2|)."""
    return float(max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1])))


HEURISTICS: Dict[str, Callable[[Coord, Coord], float]] = {
    "Manhattan": manhattan_distance,
    "Euclidean": euclidean_distance,
    "Chebyshev": chebyshev_distance
}

ALGORITHMS = ["A*", "Dijkstra", "Greedy", "BFS"]


def astar_search(
    start: Coord,
    goal: Coord,
    obstacles: Set[Coord],
    cols: int,
    rows: int,
    favor_straight: bool = True,
    algorithm: str = "A*",
    heuristic_name: str = "Manhattan"
) -> Tuple[Optional[List[Coord]], Set[Coord], float]:
    """
    Multi-algorithm search engine for comparative evaluation.
    
    Returns:
        (path, explored_nodes, compute_time_ms)
    """
    t0 = time.perf_counter()
    if start == goal:
        return [start], {start}, 0.01
    
    if start in obstacles or goal in obstacles:
        return None, set(), (time.perf_counter() - t0) * 1000.0

    heuristic = HEURISTICS.get(heuristic_name, manhattan_distance)
    explored: Set[Coord] = set()
    directions = [(1, 0), (0, -1), (0, 1), (-1, 0)]

    # 1. Breadth-First Search (BFS)
    if algorithm == "BFS":
        queue = deque([(start, [start])])
        visited = {start}
        while queue:
            current, path = queue.popleft()
            explored.add(current)
            if current == goal:
                elapsed_ms = (time.perf_counter() - t0) * 1000.0
                return path, explored, elapsed_ms
            
            for dx, dy in directions:
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < cols and 0 <= neighbor[1] < rows and neighbor not in obstacles:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, path + [neighbor]))
                        
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        return None, explored, elapsed_ms

    # 2. Priority Queue Algorithms: A*, Dijkstra, Greedy
    tie_counter = 0
    h_start = heuristic(start, goal) if algorithm in ["A*", "Greedy"] else 0.0
    f_start = h_start if algorithm == "Greedy" else (0.0 if algorithm == "Dijkstra" else h_start)
    
    open_heap = [(f_start, 0.0, tie_counter, start, [start])]
    g_costs: Dict[Coord, float] = {start: 0.0}

    while open_heap:
        f, g, _, current, path = heapq.heappop(open_heap)
        
        if current in explored:
            continue
        explored.add(current)
        
        if current == goal:
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            return path, explored, elapsed_ms
        
        current_g = g_costs[current]
        
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            
            if not (0 <= neighbor[0] < cols and 0 <= neighbor[1] < rows):
                continue
            if neighbor in obstacles:
                continue
            
            tentative_g = current_g + 1.0
            
            if neighbor not in g_costs or tentative_g < g_costs[neighbor]:
                g_costs[neighbor] = tentative_g
                h_cost = heuristic(neighbor, goal)
                
                turn_penalty = 0.0
                if favor_straight and len(path) >= 2:
                    prev_dir = (current[0] - path[-2][0], current[1] - path[-2][1])
                    if (dx, dy) != prev_dir:
                        turn_penalty = 0.001

                if algorithm == "A*":
                    priority = tentative_g + h_cost + turn_penalty
                elif algorithm == "Dijkstra":
                    priority = tentative_g + turn_penalty
                else:  # Greedy
                    priority = h_cost + turn_penalty

                tie_counter += 1
                heapq.heappush(open_heap, (priority, tentative_g, tie_counter, neighbor, path + [neighbor]))
                
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return None, explored, elapsed_ms


def spacetime_astar_search(
    start: Coord,
    goal: Coord,
    obstacles: Set[Coord],
    vertex_reservations: Set[SpaceTimeState],
    swap_reservations: Set[Tuple[int, int, int, int, int]],
    cols: int,
    rows: int,
    max_time: int = 150,
    heuristic_name: str = "Manhattan"
) -> Tuple[Optional[List[Coord]], Set[Coord], int, float]:
    """
    Space-Time A* for Multi-Agent Pathfinding (MAPF).
    Explores state space (x, y, t) with 4-way moves + Wait action.
    """
    t0 = time.perf_counter()
    if start in obstacles or goal in obstacles:
        return None, set(), 0, (time.perf_counter() - t0) * 1000.0

    heuristic = HEURISTICS.get(heuristic_name, manhattan_distance)
    tie_counter = 0
    h_start = heuristic(start, goal)
    open_heap = [(h_start, 0, 0, tie_counter, start, [start])]
    
    visited_states: Set[SpaceTimeState] = set()
    explored_coords: Set[Coord] = set()
    
    actions = [(1, 0), (0, -1), (0, 1), (-1, 0), (0, 0)]
    
    while open_heap:
        f, g, t, _, current, path = heapq.heappop(open_heap)
        
        state = (current[0], current[1], t)
        if state in visited_states or t >= max_time:
            continue
        visited_states.add(state)
        explored_coords.add(current)
        
        if current == goal:
            waits = sum(1 for i in range(1, len(path)) if path[i] == path[i - 1])
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            return path, explored_coords, waits, elapsed_ms
        
        for dx, dy in actions:
            nxt = (current[0] + dx, current[1] + dy)
            nt = t + 1
            
            if not (0 <= nxt[0] < cols and 0 <= nxt[1] < rows):
                continue
            if nxt in obstacles:
                continue
            
            if (nxt[0], nxt[1], nt) in vertex_reservations:
                continue
            
            swap_key = (current[0], current[1], nxt[0], nxt[1], t)
            if swap_key in swap_reservations:
                continue
            
            new_g = t + 1
            new_h = heuristic(nxt, goal)
            wait_penalty = 0.05 if (dx, dy) == (0, 0) else 0.0
            new_f = new_g + new_h + wait_penalty
            
            tie_counter += 1
            next_state = (nxt[0], nxt[1], nt)
            if next_state not in visited_states:
                heapq.heappush(open_heap, (new_f, new_g, nt, tie_counter, nxt, path + [nxt]))
                
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return None, explored_coords, 0, elapsed_ms
