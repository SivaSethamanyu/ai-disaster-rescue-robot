"""
High-Level Configuration Module for AI Disaster Rescue Robot.
Features dense debris layouts, multi-agent swarm configurations,
and extreme difficulty disaster ruins.
"""

# Grid & Screen Dimensions
CELL = 40
COLS = 18
ROWS = 13
PANEL = 130  # Expanded for high-level telemetry and status cards

WIDTH = COLS * CELL           # 18 * 40 = 720
HEIGHT = ROWS * CELL + PANEL  # 13 * 40 + 130 = 650

# --- COLOR PALETTES ---
THEME_CLASSIC = {
    "name": "Classic Presentation",
    "bg": (250, 252, 255),
    "grid_line": (225, 230, 238),
    "rubble_fill": (165, 170, 178),
    "rubble_border": (110, 118, 128),
    "rubble_cross": (95, 102, 112),
    "panel_bg": (225, 239, 255),
    "panel_border": (195, 215, 238),
    "card_bg": (240, 246, 255),
    "text_dark": (30, 38, 52),
    "text_muted": (100, 110, 125),
    "border_light": (185, 202, 222),
    "heatmap_r1": (210, 230, 255),
    "heatmap_r2": (255, 235, 210),
    "heatmap_r3": (215, 245, 225)
}

THEME_TACTICAL = {
    "name": "Tactical Command Center",
    "bg": (18, 22, 30),
    "grid_line": (32, 40, 52),
    "rubble_fill": (45, 52, 65),
    "rubble_border": (70, 80, 98),
    "rubble_cross": (85, 96, 115),
    "panel_bg": (12, 16, 22),
    "panel_border": (38, 48, 65),
    "card_bg": (24, 30, 42),
    "text_dark": (235, 242, 255),
    "text_muted": (140, 155, 175),
    "border_light": (50, 65, 88),
    "heatmap_r1": (35, 75, 130),
    "heatmap_r2": (130, 80, 35),
    "heatmap_r3": (35, 120, 80)
}

THEME_THERMAL = {
    "name": "FLIR Thermal Vision",
    "bg": (16, 12, 28),
    "grid_line": (34, 25, 50),
    "rubble_fill": (30, 22, 48),
    "rubble_border": (60, 42, 88),
    "rubble_cross": (78, 54, 110),
    "panel_bg": (10, 8, 18),
    "panel_border": (48, 32, 72),
    "card_bg": (22, 16, 35),
    "text_dark": (255, 235, 215),
    "text_muted": (185, 150, 195),
    "border_light": (68, 48, 95),
    "heatmap_r1": (160, 45, 125),
    "heatmap_r2": (220, 125, 35),
    "heatmap_r3": (35, 185, 140)
}

# Agent Colors
COLOR_R1_SCOUT = (35, 110, 240)    # Blue (Agent 1: Scout)
COLOR_R2_LIFTER = (245, 145, 35)   # Orange (Agent 2: Lifter)
COLOR_R3_MEDIC = (0, 185, 130)     # Emerald Green (Agent 3: Medic)

COLOR_VICTIM = (235, 55, 60)       # Emergency Crimson
COLOR_RESCUED = (30, 185, 95)      # Safety Green
COLOR_WARNING = (255, 200, 40)     # Conflict / Hazard Yellow
COLOR_CYAN = (0, 210, 255)         # Telemetry highlight

# Simulation Speeds
SPEED_PRESETS = [0.5, 1.0, 2.0, 4.0]
DEFAULT_STEP_INTERVAL = 0.22  # Base seconds per grid step

# High-Difficulty Predefined Disaster Scenarios
SCENARIOS = {
    1: {
        "name": "1. Heavy Debris Collapse",
        "difficulty": "Moderate",
        "description": "Reinforced presentation scenario with extra cross-beams and structural rubble (38 blocks).",
        "num_robots": 2,
        "robots": [
            {"id": 0, "name": "Robot 1 (Scout)", "role": "Scout", "start": (1, 2), "color": COLOR_R1_SCOUT},
            {"id": 1, "name": "Robot 2 (Lifter)", "role": "Lifter", "start": (1, 10), "color": COLOR_R2_LIFTER}
        ],
        "victims": [(16, 3), (16, 9)],
        "target_assignment": [(0, (16, 3)), (1, (16, 9))],
        "obstacles": [
            # Pillar 1 (col 3)
            (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 7), (3, 8), (3, 9), (3, 10),
            # Cross debris from pillar 1
            (4, 3), (5, 3), (4, 8), (5, 8),
            # Pillar 2 (col 9)
            (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10), (9, 11),
            # Additional debris around center
            (8, 5), (10, 5), (8, 9), (10, 9),
            # Pillar 3 (col 15)
            (15, 1), (15, 2), (15, 4), (15, 5), (15, 6), (15, 7), (15, 8), (15, 10), (15, 11),
            # Collapse near targets
            (14, 2), (14, 10)
        ],
        "dynamic_events": False
    },
    2: {
        "name": "2. High-Conflict Chokepoints",
        "difficulty": "Hard",
        "description": "Severely constricted corridors forcing robots into space-time queueing and detours (48 blocks).",
        "num_robots": 2,
        "robots": [
            {"id": 0, "name": "Robot 1 (Scout)", "role": "Scout", "start": (2, 6), "color": COLOR_R1_SCOUT},
            {"id": 1, "name": "Robot 2 (Lifter)", "role": "Lifter", "start": (8, 1), "color": COLOR_R2_LIFTER}
        ],
        "victims": [(15, 6), (8, 11)],
        "target_assignment": [(0, (15, 6)), (1, (8, 11))],
        "obstacles": [
            # Narrow perpendicular corridor forcing intersection at (8, 6)
            (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (9, 4), (10, 4), (11, 4), (12, 4), (13, 4), (14, 4),
            (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (9, 5), (10, 5), (11, 5), (12, 5), (13, 5), (14, 5),
            (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (9, 7), (10, 7), (11, 7), (12, 7), (13, 7), (14, 7),
            (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (9, 8), (10, 8), (11, 8), (12, 8), (13, 8), (14, 8),
            # Vertical chokepoint barriers
            (6, 1), (6, 2), (6, 3), (10, 1), (10, 2), (10, 3),
            (6, 9), (6, 10), (6, 11), (10, 9), (10, 10), (10, 11)
        ],
        "dynamic_events": False
    },
    3: {
        "name": "3. Tri-Agent Dense Ruins",
        "difficulty": "Extreme",
        "description": "Collapsed complex with 63 rubble blocks; Scout, Lifter, and Medic navigate narrow passages.",
        "num_robots": 3,
        "robots": [
            {"id": 0, "name": "Agent 1 (Scout)", "role": "Scout", "start": (1, 1), "color": COLOR_R1_SCOUT},
            {"id": 1, "name": "Agent 2 (Lifter)", "role": "Lifter", "start": (1, 6), "color": COLOR_R2_LIFTER},
            {"id": 2, "name": "Agent 3 (Medic)", "role": "Medic", "start": (1, 11), "color": COLOR_R3_MEDIC}
        ],
        "victims": [(16, 2), (16, 6), (16, 10)],
        "target_assignment": [(0, (16, 2)), (1, (16, 6)), (2, (16, 10))],
        "obstacles": [
            # Heavy collapsed multi-sector building (63 blocks)
            (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11),
            (4, 2), (5, 2), (4, 10), (5, 10),
            (6, 0), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (6, 12),
            (7, 4), (8, 4), (7, 8), (8, 8),
            (9, 0), (9, 1), (9, 2), (9, 4), (9, 5), (9, 7), (9, 8), (9, 10), (9, 11), (9, 12),
            (10, 2), (11, 2), (10, 10), (11, 10),
            (12, 0), (12, 2), (12, 3), (12, 4), (12, 5), (12, 7), (12, 8), (12, 9), (12, 10), (12, 12),
            (15, 0), (15, 1), (15, 3), (15, 4), (15, 5), (15, 7), (15, 8), (15, 9), (15, 11), (15, 12)
        ],
        "dynamic_events": False
    },
    4: {
        "name": "4. Tremor Surge & Rubble Collapse",
        "difficulty": "Dynamic Hard",
        "description": "Active aftershocks drop secondary rubble during execution; robots dynamically reroute in real time.",
        "num_robots": 2,
        "robots": [
            {"id": 0, "name": "Robot 1 (Scout)", "role": "Scout", "start": (1, 2), "color": COLOR_R1_SCOUT},
            {"id": 1, "name": "Robot 2 (Lifter)", "role": "Lifter", "start": (1, 10), "color": COLOR_R2_LIFTER}
        ],
        "victims": [(16, 4), (16, 8)],
        "target_assignment": [(0, (16, 4)), (1, (16, 8))],
        "obstacles": [
            (3, 1), (3, 2), (3, 3), (3, 4), (3, 8), (3, 9), (3, 10), (3, 11),
            (5, 5), (5, 6), (5, 7),
            (8, 1), (8, 2), (8, 9), (8, 10), (8, 11),
            (11, 3), (11, 4), (11, 5), (11, 7), (11, 8), (11, 9),
            (14, 1), (14, 2), (14, 5), (14, 6), (14, 7), (14, 10), (14, 11)
        ],
        "dynamic_events": True
    },
    5: {
        "name": "5. Catastrophic Labyrinth (71 Blocks)",
        "difficulty": "MAXIMUM",
        "description": "Extreme structural failure: 71 rubble blockages forming a complex serpentine maze of collapsed voids.",
        "num_robots": 2,
        "robots": [
            {"id": 0, "name": "Robot 1 (Scout)", "role": "Scout", "start": (1, 2), "color": COLOR_R1_SCOUT},
            {"id": 1, "name": "Robot 2 (Lifter)", "role": "Lifter", "start": (1, 10), "color": COLOR_R2_LIFTER}
        ],
        "victims": [(16, 2), (16, 10)],
        "target_assignment": [(0, (16, 2)), (1, (16, 10))],
        "obstacles": [
            # 71 rubble blockages verified for intricate multi-winding paths
            (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11),
            (4, 2), (5, 2), (4, 10), (5, 10),
            (6, 0), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (6, 12),
            (7, 4), (8, 4), (7, 8), (8, 8),
            (9, 0), (9, 1), (9, 2), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 10), (9, 11), (9, 12),
            (10, 2), (11, 2), (10, 10), (11, 10),
            (12, 0), (12, 2), (12, 3), (12, 4), (12, 5), (12, 6), (12, 8), (12, 9), (12, 10), (12, 12),
            (15, 0), (15, 1), (15, 3), (15, 4), (15, 5), (15, 6), (15, 7), (15, 8), (15, 9), (15, 11), (15, 12),
            (14, 5), (14, 6), (14, 7), (16, 5), (16, 6), (16, 7)
        ],
        "dynamic_events": False
    }
}
