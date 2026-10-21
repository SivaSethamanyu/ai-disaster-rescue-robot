"""
Advanced Simulation Engine for AI Disaster Rescue Robot.
Features:
- N-Agent Multi-Robot Support (Scout, Lifter, Medic)
- Smooth Sub-Pixel Continuous Coordinate Interpolation (LERP)
- Direction Heading Angles for Animated Heading Indicator
- Dynamic Earthquake Rubble Drop Events (Scenario 4)
- Comprehensive Algorithmic Metrics & Telemetry
"""

import math
import random
from typing import List, Tuple, Set, Dict, Optional
from config import CELL, COLS, ROWS, SCENARIOS, WIDTH, HEIGHT
from astar import Coord, ALGORITHMS, HEURISTICS
from multi_agent import MultiAgentCoordinator
from sound_effects import play_sound
from particles import ParticleManager


class RobotAgent:
    """Represents an autonomous multi-role rescue robot."""
    
    def __init__(self, robot_id: int, start_pos: Coord, name: str, role: str, color_tuple):
        self.id = robot_id
        self.name = name
        self.role = role
        self.start_pos = start_pos
        self.pos = start_pos
        self.prev_pos = start_pos
        self.color = color_tuple
        self.target: Optional[Coord] = None
        self.path: List[Coord] = [start_pos]
        self.path_index = 0
        self.trail: List[Coord] = [start_pos]
        self.explored_nodes: Set[Coord] = set()
        self.status = "IDLE"  # IDLE, MOVING, WAITING, RESCUED
        self.steps_taken = 0
        self.waits_taken = 0
        self.heading_angle = 0.0  # In radians

        # Continuous interpolation positions for smooth rendering
        self.render_x = float(start_pos[0])
        self.render_y = float(start_pos[1])

    def reset(self, new_start: Optional[Coord] = None):
        if new_start:
            self.start_pos = new_start
        self.pos = self.start_pos
        self.prev_pos = self.start_pos
        self.render_x = float(self.start_pos[0])
        self.render_y = float(self.start_pos[1])
        self.path = [self.start_pos]
        self.path_index = 0
        self.trail = [self.start_pos]
        self.explored_nodes.clear()
        self.status = "IDLE"
        self.steps_taken = 0
        self.waits_taken = 0
        self.heading_angle = 0.0


class Victim:
    """Represents a trapped disaster victim with AI multimodal biometric triage data."""
    
    def __init__(self, victim_id: int, pos: Coord, label: str):
        self.id = victim_id
        self.pos = pos
        self.label = label
        self.is_rescued = False
        self.rescued_by: Optional[int] = None
        self.init_biometrics()

    def init_biometrics(self):
        self.heart_rate = random.randint(118, 136)
        self.spo2 = random.randint(90, 93)
        self.core_temp = round(random.uniform(35.2, 35.8), 1)
        self.resp_rate = random.randint(20, 24)
        self.entrapment_depth = round(random.uniform(1.2, 2.4), 1)
        self.triage_level = "IMMEDIATE (RED TAG)"
        self.recommended_tool = "Hydraulic Jaws & Cervical Immobilizer"

    def reset(self):
        self.is_rescued = False
        self.rescued_by = None
        self.init_biometrics()

    def mark_rescued(self, robot_id: int):
        self.is_rescued = True
        self.rescued_by = robot_id
        self.heart_rate = 76
        self.spo2 = 99
        self.core_temp = 36.6
        self.resp_rate = 14
        self.triage_level = "STABILIZED (GREEN TAG)"
        self.recommended_tool = "Evacuated to Field Triage Hospital"


class RescueSimulation:
    """
    Main state manager for the Disaster Rescue Robot environment.
    """
    
    def __init__(self, scenario_id: int = 1):
        self.cols = COLS
        self.rows = ROWS
        self.coordinator = MultiAgentCoordinator(self.cols, self.rows)
        self.scenario_id = scenario_id
        self.obstacles: Set[Coord] = set()
        self.robots: List[RobotAgent] = []
        self.victims: List[Victim] = []
        
        # Simulation control states
        self.is_running = True
        self.is_paused = False
        self.mission_complete = False
        self.show_heatmap = False
        
        # Step timing & smooth interpolation
        self.step_timer = 0.0
        self.base_interval = 0.24  # Seconds per step at 1x
        self.speed_multiplier = 1.0
        self.lerp_factor = 0.0  # 0.0 to 1.0 between steps
        
        # Algorithm & Heuristic selection
        self.current_algorithm = "A*"
        self.current_heuristic = "Manhattan"
        self.fog_of_war_enabled = False
        self.particles = ParticleManager()
        
        # Telemetry metrics
        self.conflicts_avoided = 0
        self.total_compute_time_ms = 0.0
        self.pruning_ratio = 0.0
        self.total_explored_nodes = 0
        
        # Dynamic disaster event tracking
        self.dynamic_events_enabled = False
        self.dynamic_event_triggered = False

        # AI Mission Dispatcher & UAV Aerial Reconnaissance
        self.mission_time = 0.0
        self.ai_radio_comms: List[Tuple[str, str, str, Tuple[int, int, int]]] = []
        self.uav_x = 120.0
        self.uav_y = 90.0
        self.uav_vx = 60.0
        self.uav_vy = 35.0
        self.prop_spin = 0.0
        self.uav_comms_timer = 0.0
        self.selected_victim_id: Optional[int] = None

        self.load_scenario(self.scenario_id)

    def post_comms(self, sender: str, msg: str, color=(210, 230, 250)):
        """Posts a live tactical radio dispatch from AI Commander, UAV, or Robots."""
        mins = int(self.mission_time // 60)
        secs = int(self.mission_time % 60)
        timestamp = f"{mins:02d}:{secs:02d}"
        self.ai_radio_comms.append((timestamp, sender, msg, color))
        if len(self.ai_radio_comms) > 6:
            self.ai_radio_comms.pop(0)
        play_sound("radio")

    def cycle_algorithm(self):
        """Cycles between A*, Dijkstra, Greedy, and BFS for live comparative evaluation."""
        idx = ALGORITHMS.index(self.current_algorithm)
        self.current_algorithm = ALGORITHMS[(idx + 1) % len(ALGORITHMS)]
        self.replan_all()

    def cycle_heuristic(self):
        """Cycles between Manhattan, Euclidean, and Chebyshev metrics."""
        heur_list = list(HEURISTICS.keys())
        idx = heur_list.index(self.current_heuristic)
        self.current_heuristic = heur_list[(idx + 1) % len(heur_list)]
        self.replan_all()

    @property
    def step_interval(self) -> float:
        return self.base_interval / self.speed_multiplier

    def load_scenario(self, scenario_id: int):
        """Loads a specific scenario by ID (1, 2, 3, or 4)."""
        self.scenario_id = scenario_id
        config = SCENARIOS.get(scenario_id, SCENARIOS[1])
        
        self.obstacles = set(config["obstacles"])
        self.robots = [
            RobotAgent(
                r["id"], r["start"], r["name"], r.get("role", "Rescue"), r["color"]
            )
            for r in config["robots"]
        ]
        self.victims = [
            Victim(i, pos, f"V{i+1}") for i, pos in enumerate(config["victims"])
        ]
        self.dynamic_events_enabled = config.get("dynamic_events", False)
        self.dynamic_event_triggered = False
        
        self.replan_all()
        self.post_comms("AI-COMMAND", f"Sector {self.scenario_id} deployed ({len(self.obstacles)} rubble blocks).", (0, 220, 255))

    def add_debris_surge(self, count: int = 5):
        """Randomly drops a surge of new rubble blocks, prompting instant dynamic replanning."""
        robot_positions = {r.pos for r in self.robots}
        victim_positions = {v.pos for v in self.victims}
        reserved = robot_positions.union(victim_positions)
        
        candidates = [
            (c, r) for c in range(self.cols) for r in range(self.rows)
            if (c, r) not in self.obstacles and (c, r) not in reserved
        ]
        random.shuffle(candidates)
        
        added = 0
        for cand in candidates:
            if added >= count:
                break
            # Temporarily add and test if paths still exist
            self.obstacles.add(cand)
            # Verify paths
            valid = True
            for r in self.robots:
                if r.target:
                    from astar import astar_search
                    p, _, _ = astar_search(r.pos, r.target, self.obstacles, self.cols, self.rows)
                    if not p:
                        valid = False
                        break
            if valid:
                added += 1
            else:
                self.obstacles.remove(cand)
                
        if added > 0:
            play_sound("wait")
            for cand in candidates[:added]:
                self.particles.emit_collapse_debris(cand[0] * CELL + CELL // 2, cand[1] * CELL + CELL // 2)
            self.post_comms("SEISMIC", f"Tremor alert! {added} rubble blocks dropped. Online replanning.", (255, 130, 40))
            self.replan_from_current_positions()
        return added

    def generate_random_disaster(self, density: float = 0.28):
        """Generates challenging procedural disaster rubble with dense corridors."""
        self.scenario_id = 99
        self.obstacles.clear()
        
        r1_start = (1, random.randint(1, 4))
        r2_start = (1, random.randint(8, 11))
        v1_pos = (self.cols - 2, random.randint(1, 5))
        v2_pos = (self.cols - 2, random.randint(7, 11))
        
        reserved = {r1_start, r2_start, v1_pos, v2_pos}
        
        for c in range(self.cols):
            for r in range(self.rows):
                if (c, r) not in reserved:
                    if random.random() < density:
                        self.obstacles.add((c, r))
                        
        self.robots = [
            RobotAgent(0, r1_start, "Robot 1 (Scout)", "Scout", (35, 110, 240)),
            RobotAgent(1, r2_start, "Robot 2 (Lifter)", "Lifter", (245, 145, 35))
        ]
        self.victims = [
            Victim(0, v1_pos, "V1"),
            Victim(1, v2_pos, "V2")
        ]
        self.dynamic_events_enabled = False
        
        # Verify solvability: if blocked, remove blocking candidates
        from astar import astar_search
        p1, _, _ = astar_search(r1_start, v1_pos, self.obstacles, self.cols, self.rows)
        p2, _, _ = astar_search(r2_start, v2_pos, self.obstacles, self.cols, self.rows)
        
        if not p1 or not p2:
            # Clear 1-cell corridor for each
            for c in range(self.cols):
                self.obstacles.discard((c, r1_start[1]))
                self.obstacles.discard((c, r2_start[1]))
                
        self.replan_all()

    def replan_all(self):
        """Re-computes target allocation and multi-agent space-time paths."""
        config = SCENARIOS.get(self.scenario_id, {})
        robot_starts = [r.start_pos for r in self.robots]
        victim_positions = [v.pos for v in self.victims if not v.is_rescued]
        
        if not victim_positions:
            victim_positions = [v.pos for v in self.victims]
            
        explicit_assignment = config.get("target_assignment")
        if explicit_assignment and len(explicit_assignment) == len(self.robots):
            assignments = explicit_assignment
        else:
            assignments = self.coordinator.allocate_targets(robot_starts, victim_positions, self.obstacles)
        
        for r in self.robots:
            r.reset()
        for v in self.victims:
            v.reset()
            
        for r_id, target in assignments:
            if r_id < len(self.robots):
                self.robots[r_id].target = target

        plans = self.coordinator.plan_coordinated_paths(
            robot_starts, assignments, self.obstacles,
            algorithm=self.current_algorithm, heuristic_name=self.current_heuristic
        )
        
        self.conflicts_avoided = 0
        total_explored = set()
        self.total_compute_time_ms = self.coordinator.total_compute_time_ms
        
        for r_id, pdata in plans.items():
            if r_id < len(self.robots):
                self.robots[r_id].path = pdata["path"]
                self.robots[r_id].explored_nodes = pdata["explored"]
                total_explored.update(pdata["explored"])
                self.conflicts_avoided += pdata["conflicts_avoided"]

        # Calculate search space pruning efficiency
        total_grid_nodes = self.cols * self.rows
        self.total_explored_nodes = len(total_explored)
        self.pruning_ratio = max(0.0, 1.0 - (self.total_explored_nodes / total_grid_nodes)) * 100.0

        self.mission_complete = False
        self.step_timer = 0.0
        self.lerp_factor = 0.0

    def toggle_obstacle(self, coord: Coord):
        """Allows user to click on the grid to add/remove rubble dynamically."""
        robot_positions = {r.pos for r in self.robots}
        victim_positions = {v.pos for v in self.victims}
        if coord in robot_positions or coord in victim_positions:
            return

        if coord in self.obstacles:
            self.obstacles.remove(coord)
        else:
            self.obstacles.add(coord)
            
        self.replan_from_current_positions()

    def replan_from_current_positions(self):
        """Replans paths dynamically while maintaining current progress."""
        robot_positions = [r.pos for r in self.robots]
        victim_positions = [v.pos for v in self.victims if not v.is_rescued]
        
        if not victim_positions:
            return
            
        assignments = self.coordinator.allocate_targets(robot_positions, victim_positions, self.obstacles)
        for r_id, target in assignments:
            if r_id < len(self.robots):
                self.robots[r_id].target = target
            
        plans = self.coordinator.plan_coordinated_paths(
            robot_positions, assignments, self.obstacles,
            algorithm=self.current_algorithm, heuristic_name=self.current_heuristic
        )
        total_explored = set()
        self.total_compute_time_ms = self.coordinator.total_compute_time_ms
        
        for r_id, pdata in plans.items():
            if r_id < len(self.robots):
                self.robots[r_id].path = pdata["path"]
                self.robots[r_id].path_index = 0
                self.robots[r_id].explored_nodes = pdata["explored"]
                total_explored.update(pdata["explored"])

        total_grid_nodes = self.cols * self.rows
        self.total_explored_nodes = len(total_explored)
        self.pruning_ratio = max(0.0, 1.0 - (self.total_explored_nodes / total_grid_nodes)) * 100.0

    def update(self, dt: float):
        """Advances animation, smooth coordinate interpolation, UAV flight, and particle physics."""
        self.particles.update(dt)
        self.mission_time += dt
        self.prop_spin += dt * 38.0

        # Autonomous aerial reconnaissance drone smooth cruising
        self.uav_x += self.uav_vx * dt
        self.uav_y += self.uav_vy * dt
        if self.uav_x < 55:
            self.uav_x = 55
            self.uav_vx *= -1
        elif self.uav_x > WIDTH - 55:
            self.uav_x = WIDTH - 55
            self.uav_vx *= -1
        if self.uav_y < 45:
            self.uav_y = 45
            self.uav_vy *= -1
        elif self.uav_y > ROWS * CELL - 55:
            self.uav_y = ROWS * CELL - 55
            self.uav_vy *= -1

        # Periodic tactical UAV aerial telemetry broadcast
        if not self.mission_complete and not self.is_paused:
            self.uav_comms_timer += dt
            if self.uav_comms_timer >= 10.0:
                self.uav_comms_timer = 0.0
                unrescued = [v for v in self.victims if not v.is_rescued]
                if unrescued:
                    target_v = unrescued[0]
                    msgs = [
                        ("UAV-RECON", f"Aerial LiDAR locked on {target_v.label} at grid {target_v.pos}.", (0, 240, 255)),
                        ("UAV-RECON", "Thermal infrared scan confirms active vital signs.", (255, 180, 50)),
                        ("UAV-RECON", "Structural integrity assessment: No overhead collapse imminent.", (130, 230, 255)),
                        ("AI-COMMAND", f"Multi-Agent reservation table synced: 0 spatial conflicts.", (180, 220, 255))
                    ]
                    m = random.choice(msgs)
                    self.post_comms(m[0], m[1], m[2])
        
        if self.mission_complete or self.is_paused:
            return

        self.step_timer += dt
        self.lerp_factor = min(1.0, self.step_timer / self.step_interval)

        # Smooth continuous linear interpolation (LERP) between prev_pos and current pos
        for r in self.robots:
            r.render_x = r.prev_pos[0] + (r.pos[0] - r.prev_pos[0]) * self.lerp_factor
            r.render_y = r.prev_pos[1] + (r.pos[1] - r.prev_pos[1]) * self.lerp_factor

        if self.step_timer >= self.step_interval:
            self.step_timer = 0.0
            self.lerp_factor = 0.0
            self.step()

    def step(self):
        """Advances all robots one discrete step along their planned paths with collision safety."""
        if self.mission_complete:
            return

        # Check for dynamic falling debris in Scenario 4
        if self.dynamic_events_enabled and not self.dynamic_event_triggered:
            lead_step = self.robots[0].steps_taken
            if lead_step >= 6:
                # Trigger aftershock rubble collapse directly in corridor
                self.obstacles.add((8, 2))
                self.obstacles.add((8, 3))
                self.obstacles.add((8, 4))
                self.dynamic_event_triggered = True
                play_sound("wait")
                self.replan_from_current_positions()
                return

        all_completed = True
        
        # Check next intended positions
        next_positions = []
        for r in self.robots:
            if r.path_index < len(r.path) - 1:
                next_positions.append(r.path[r.path_index + 1])
                all_completed = False
            else:
                next_positions.append(r.pos)

        # Multi-Agent Runtime Conflict Check
        pos_list = [r.pos for r in self.robots]
        conflict_pair = self.coordinator.check_dynamic_conflict(pos_list, next_positions)
        if conflict_pair:
            # Lower priority robot yields
            low_idx = max(conflict_pair)
            next_positions[low_idx] = self.robots[low_idx].pos
            self.robots[low_idx].waits_taken += 1
            self.conflicts_avoided += 1
            self.post_comms("AI-SAFETY", f"{self.robots[low_idx].name} yielding 1 turn to clear junction.", (255, 205, 50))

        # Advance each robot
        for idx, r in enumerate(self.robots):
            r.prev_pos = r.pos
            if r.path_index < len(r.path) - 1:
                target_next = next_positions[idx]
                planned_next = r.path[r.path_index + 1]
                
                if target_next == r.pos and planned_next != r.pos:
                    # Dynamic runtime yield
                    r.status = "WAITING"
                    r.waits_taken += 1
                    play_sound("wait")
                else:
                    prev_pos = r.pos
                    r.path_index += 1
                    r.pos = target_next
                    
                    if target_next == prev_pos:
                        r.status = "WAITING"
                        r.waits_taken += 1
                        play_sound("wait")
                    else:
                        r.trail.append(r.pos)
                        r.steps_taken += 1
                        r.status = "MOVING"
                        # Update heading angle & emit tread dust
                        dx = r.pos[0] - prev_pos[0]
                        dy = r.pos[1] - prev_pos[1]
                        if dx != 0 or dy != 0:
                            r.heading_angle = math.atan2(dy, dx)
                        self.particles.emit_tread_dust(r.render_x * CELL + CELL // 2, r.render_y * CELL + CELL // 2, r.heading_angle)
            else:
                r.status = "RESCUED"

            # Check victim rescue
            for v in self.victims:
                if not v.is_rescued and r.pos == v.pos:
                    v.mark_rescued(r.id)
                    r.status = "RESCUED"
                    play_sound("rescue")
                    self.particles.emit_rescue_sparkles(v.pos[0] * CELL + CELL // 2, v.pos[1] * CELL + CELL // 2)
                    self.post_comms("MEDIC", f"Survivor {v.label} extracted! Biometrics stabilized.", (30, 235, 120))

        # Check mission completion
        rescued_count = sum(1 for v in self.victims if v.is_rescued)
        if rescued_count == len(self.victims) and not self.mission_complete:
            self.mission_complete = True
            for r in self.robots:
                r.status = "RESCUED"
            play_sound("victory")
            self.post_comms("AI-COMMAND", "Mission 100% Complete. All trapped civilians rescued.", (0, 240, 255))
        elif all_completed and not self.mission_complete:
            self.mission_complete = True
            play_sound("victory")
            self.post_comms("AI-COMMAND", "Mission 100% Complete. All trapped civilians rescued.", (0, 240, 255))

    def restart(self):
        """Restarts the current scenario from the beginning."""
        self.load_scenario(self.scenario_id)

    @property
    def victims_rescued_count(self) -> int:
        return sum(1 for v in self.victims if v.is_rescued)

    @property
    def progress_percent(self) -> int:
        if not self.victims:
            return 100
        return int((self.victims_rescued_count / len(self.victims)) * 100)
