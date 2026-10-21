"""
AI Disaster Rescue Robot Using A* and Multi-Agent Planning
==========================================================
Course Case Study Project - VIT Vellore
Presented by: Haritha (Register Number: 24BCE0412)
Department of Computer Science and Engineering

Elite Features & Realistic Effects:
- 3D Fractured Concrete Rubble with Drop Shadows, Jagged Cracks & Exposed Rebar
- Human Survivors with Waving SOS Distress Animation & Biometric Beacons
- Search-and-Rescue Tracked Rovers with Rotating Turret & Headlight Beam Projection
- Autonomous Aerial UAV Reconnaissance Drone Cruising Overhead with Spotlight
- FLIR Thermal Infrared Vision Mode ('I' / 'T' key)
- Multimodal AI Survivor Triage Scanner with Live Patient Biometrics ('C' key)
- Live Tactical AI Radio Communications Feed Banner
- Dynamic Tread Dust & Rubble Collapse Particle Physics System
- Earthquake Tremor Camera Shake & Aftershock Rubble Surges ('D' key)
- Live Multi-Algorithm Benchmark Switcher ('A' key: A*, Dijkstra, Greedy, BFS)
- Multiple Heuristics Switcher ('M' key: Manhattan, Euclidean, Chebyshev)
- Dynamic Fog of War & LiDAR Reconnaissance Scanner Mode ('F' key)
- Mini-Radar Sonar Sweep with Live Victim Transponder Blips
- Real-Time Victim Biometric Heartbeat EKG Vital Signs Monitor
- Comprehensive On-Screen Help & Legend Modal Overlay ('F1' key)
"""

import sys
import math
import random
import pygame
from config import (
    CELL, COLS, ROWS, PANEL, WIDTH, HEIGHT,
    THEME_CLASSIC, THEME_TACTICAL, THEME_THERMAL, SCENARIOS, SPEED_PRESETS,
    COLOR_VICTIM, COLOR_RESCUED, COLOR_WARNING, COLOR_CYAN,
    COLOR_R1_SCOUT, COLOR_R2_LIFTER, COLOR_R3_MEDIC
)
from simulation import RescueSimulation
from astar import ALGORITHMS, HEURISTICS
import sound_effects


def draw_realistic_rubble(surface, x, y, size, is_dark, is_thermal=False):
    """Renders 3D fractured concrete rubble with cracks, shadows, rebar, or FLIR cold signature."""
    if is_thermal:
        base_col = (26, 18, 42)
        top_bevel = (45, 30, 72)
        bot_bevel = (16, 10, 28)
        crack_col = (10, 6, 18)
        rebar_col = (70, 40, 105)
    elif is_dark:
        base_col = (48, 55, 68)
        top_bevel = (78, 88, 105)
        bot_bevel = (25, 30, 40)
        crack_col = (15, 20, 28)
        rebar_col = (160, 70, 40)
    else:
        base_col = (145, 150, 160)
        top_bevel = (185, 190, 200)
        bot_bevel = (95, 100, 110)
        crack_col = (65, 70, 80)
        rebar_col = (175, 75, 40)

    # 1. Drop shadow
    shadow_rect = pygame.Rect(x + 3, y + 3, size - 4, size - 4)
    pygame.draw.rect(surface, (0, 0, 0, 70 if is_thermal else 50), shadow_rect, border_radius=4)

    # 2. Main concrete block
    block_rect = pygame.Rect(x + 2, y + 2, size - 4, size - 4)
    pygame.draw.rect(surface, base_col, block_rect, border_radius=4)

    # 3. 3D Bevel edges (light source top-left)
    pygame.draw.line(surface, top_bevel, (x + 3, y + 3), (x + size - 3, y + 3), 2)
    pygame.draw.line(surface, top_bevel, (x + 3, y + 3), (x + 3, y + size - 3), 2)
    pygame.draw.line(surface, bot_bevel, (x + 3, y + size - 3), (x + size - 3, y + size - 3), 2)
    pygame.draw.line(surface, bot_bevel, (x + size - 3, y + 3), (x + size - 3, y + size - 3), 2)

    # 4. Crack variation
    var = (x * 7 + y * 13) % 3
    if var == 0:
        pygame.draw.lines(surface, crack_col, False, [
            (x + 8, y + 8), (x + 18, y + 20), (x + 24, y + 16), (x + 32, y + 28)
        ], 2)
        pygame.draw.line(surface, crack_col, (x + 18, y + 20), (x + 15, y + 32), 2)
    elif var == 1:
        pygame.draw.lines(surface, crack_col, False, [
            (x + 10, y + 32), (x + 20, y + 18), (x + 28, y + 24), (x + 32, y + 10)
        ], 2)
    else:
        pygame.draw.line(surface, crack_col, (x + 6, y + 14), (x + 32, y + 26), 2)
        pygame.draw.line(surface, crack_col, (x + 20, y + 6), (x + 16, y + 34), 2)

    # 5. Exposed rusted iron rebar
    if (x + y) % 2 == 0:
        pygame.draw.line(surface, rebar_col, (x + 5, y + 6), (x + 1, y + 1), 2)

    # 6. Concrete pebbles
    pygame.draw.circle(surface, bot_bevel, (x + size - 8, y + 8), 2)
    pygame.draw.circle(surface, top_bevel, (x + 8, y + size - 8), 2)

    if is_thermal and (x * 3 + y) % 7 == 0:
        pygame.draw.circle(surface, (50, 80, 140), (x + size // 2, y + size // 2), 2)


def draw_realistic_person(surface, cx, cy, label, is_rescued, pulse_timer, font, is_thermal=False):
    """Renders a trapped disaster victim with waving arms, high-vis jacket, or FLIR thermal heat signature."""
    # 1. Ground shadow
    pygame.draw.ellipse(surface, (0, 0, 0, 60), (cx - 8, cy + 10, 16, 5))

    if is_thermal:
        # Thermal Infrared Heat Aura
        if not is_rescued:
            aura_r = int(16 + 3 * math.sin(pulse_timer * 3.5))
            aura_surf = pygame.Surface((aura_r * 2 + 4, aura_r * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(aura_surf, (255, 60, 20, 55), (aura_r + 2, aura_r + 2), aura_r)
            pygame.draw.circle(aura_surf, (255, 160, 30, 75), (aura_r + 2, aura_r + 2), max(1, aura_r - 4))
            surface.blit(aura_surf, (cx - aura_r - 2, cy - aura_r - 2))
            skin_col = (255, 235, 80)     # Hot head ~37.2 C
            jacket_col = (255, 75, 25)    # Core body ~36.8 C
            pants_col = (210, 45, 65)     # Lower limbs ~35.5 C
        else:
            pygame.draw.circle(surface, (40, 220, 180), (cx, cy), 18, 2)
            skin_col = (100, 240, 210)
            jacket_col = (30, 195, 145)
            pants_col = (25, 140, 110)
    else:
        # 2. Biometric distress radar pulse
        if not is_rescued:
            pulse_r = int(14 + 4 * math.sin(pulse_timer * 3.0))
            sonar_surf = pygame.Surface((pulse_r * 2 + 4, pulse_r * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(sonar_surf, (235, 55, 60, 50), (pulse_r + 2, pulse_r + 2), pulse_r, 1)
            pygame.draw.circle(sonar_surf, (235, 55, 60, 25), (pulse_r + 2, pulse_r + 2), max(1, pulse_r - 4), 1)
            surface.blit(sonar_surf, (cx - pulse_r - 2, cy - pulse_r - 2))
        else:
            pygame.draw.circle(surface, (30, 185, 95), (cx, cy), 18, 2)

        skin_col = (255, 210, 175)
        hair_col = (75, 45, 25)
        jacket_col = (35, 180, 85) if is_rescued else (235, 60, 45)
        pants_col = (45, 65, 105)

    # Legs & Shoes
    pygame.draw.line(surface, pants_col, (cx - 3, cy + 4), (cx - 4, cy + 11), 3)
    pygame.draw.line(surface, pants_col, (cx + 3, cy + 4), (cx + 4, cy + 11), 3)
    pygame.draw.circle(surface, (30, 30, 35) if not is_thermal else pants_col, (cx - 4, cy + 12), 2)
    pygame.draw.circle(surface, (30, 30, 35) if not is_thermal else pants_col, (cx + 4, cy + 12), 2)

    # Torso
    pygame.draw.rect(surface, jacket_col, (cx - 5, cy - 4, 10, 9), border_radius=2)
    if not is_rescued and not is_thermal:
        pygame.draw.line(surface, (255, 255, 180), (cx - 5, cy), (cx + 4, cy), 2)

    # Arms
    if not is_rescued:
        sway = int(2.5 * math.sin(pulse_timer * 4.0))
        pygame.draw.line(surface, jacket_col, (cx - 5, cy - 2), (cx - 10, cy - 8 + sway), 2)
        pygame.draw.line(surface, jacket_col, (cx + 5, cy - 2), (cx + 10, cy - 8 - sway), 2)
        pygame.draw.circle(surface, skin_col, (cx - 10, cy - 8 + sway), 2)
        pygame.draw.circle(surface, skin_col, (cx + 10, cy - 8 - sway), 2)
    else:
        pygame.draw.line(surface, jacket_col, (cx - 5, cy - 2), (cx - 7, cy + 5), 2)
        pygame.draw.line(surface, jacket_col, (cx + 5, cy - 2), (cx + 7, cy + 5), 2)

    # Head & Hair
    pygame.draw.circle(surface, skin_col, (cx, cy - 9), 5)
    if not is_thermal:
        pygame.draw.arc(surface, (75, 45, 25), (cx - 5, cy - 15, 10, 8), 0, math.pi, 2)

    # Badge above head (or Thermal temp in thermal mode)
    if is_thermal:
        temp_str = "37.2°C" if not is_rescued else "36.6°C"
        t_col = (255, 220, 80) if not is_rescued else (50, 240, 180)
        temp_surf = font.render(temp_str, True, t_col)
        surface.blit(temp_surf, temp_surf.get_rect(center=(cx, cy - 18)))
    else:
        if not is_rescued:
            pygame.draw.rect(surface, (230, 35, 35), (cx - 1, cy - 19, 3, 7))
            pygame.draw.rect(surface, (230, 35, 35), (cx - 3, cy - 17, 7, 3))
        else:
            pygame.draw.line(surface, (30, 185, 95), (cx - 3, cy - 16), (cx, cy - 13), 2)
            pygame.draw.line(surface, (30, 185, 95), (cx, cy - 13), (cx + 4, cy - 18), 2)


def draw_robot_rover(surface, cx, cy, angle, base_color, robot_id, status, is_dark, font, is_thermal=False):
    """Renders a tracked search-and-rescue rover with headlights, rotating turret, and thermal signatures."""
    # 1. Project search headlight beam cone
    beam_len = 55
    beam_spread = 0.42  # radians
    beam_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    p0 = (cx, cy)
    p1 = (cx + math.cos(angle - beam_spread) * beam_len, cy + math.sin(angle - beam_spread) * beam_len)
    p2 = (cx + math.cos(angle + beam_spread) * beam_len, cy + math.sin(angle + beam_spread) * beam_len)
    
    if is_thermal:
        beam_col = (0, 230, 255, 35)
    elif is_dark:
        beam_col = (255, 250, 190, 45)
    else:
        beam_col = (255, 245, 170, 25)
        
    pygame.draw.polygon(beam_surf, beam_col, [p0, p1, p2])
    surface.blit(beam_surf, (0, 0))

    # 2. Build Rover Sprite Surface (Local Coordinates: Facing UP)
    w, h = 42, 42
    bot_surf = pygame.Surface((w, h), pygame.SRCALPHA)
    bcx, bcy = w // 2, h // 2

    if is_thermal:
        tread_col = (130, 50, 80)     # Warm friction tracks
        wheel_col = (175, 70, 95)
        chassis_col = (245, 120, 30)   # Hot engine compartment
        core_col = (255, 240, 140)     # Battery core
    else:
        tread_col = (28, 30, 36)
        wheel_col = (75, 80, 92)
        chassis_col = base_color
        core_col = (0, 235, 255)

    # Tracks
    pygame.draw.rect(bot_surf, tread_col, (bcx - 14, bcy - 13, 6, 26), border_radius=2)
    pygame.draw.rect(bot_surf, tread_col, (bcx + 8, bcy - 13, 6, 26), border_radius=2)

    for dy in [-9, -3, 3, 9]:
        pygame.draw.circle(bot_surf, wheel_col, (bcx - 11, bcy + dy), 2)
        pygame.draw.circle(bot_surf, wheel_col, (bcx + 11, bcy + dy), 2)

    # Center Chassis
    pygame.draw.rect(bot_surf, chassis_col, (bcx - 8, bcy - 11, 16, 22), border_radius=3)
    pygame.draw.rect(bot_surf, (255, 255, 255), (bcx - 8, bcy - 11, 16, 22), 1, border_radius=3)

    # Turret
    pygame.draw.circle(bot_surf, (38, 42, 50) if not is_thermal else (180, 60, 40), (bcx, bcy), 6)
    pygame.draw.circle(bot_surf, core_col, (bcx, bcy - 2), 3)

    # Searchlights / Thermal Emitters
    light_col = (0, 240, 255) if is_thermal else (255, 245, 180)
    pygame.draw.circle(bot_surf, light_col, (bcx - 5, bcy - 10), 2)
    pygame.draw.circle(bot_surf, light_col, (bcx + 5, bcy - 10), 2)

    # Antenna
    pygame.draw.line(bot_surf, (150, 160, 175), (bcx + 4, bcy + 3), (bcx + 7, bcy + 9), 1)
    pygame.draw.circle(bot_surf, (255, 55, 55), (bcx + 7, bcy + 9), 2)

    deg = -math.degrees(angle) - 90
    rot_surf = pygame.transform.rotate(bot_surf, deg)
    rot_rect = rot_surf.get_rect(center=(int(cx), int(cy)))
    surface.blit(rot_surf, rot_rect)

    # Floating Identification Badge
    badge_label = f"R{robot_id + 1}"
    badge_surf = font.render(badge_label, True, (255, 255, 255))
    badge_bg = pygame.Rect(int(cx - 10), int(cy - 24), 20, 12)
    pygame.draw.rect(surface, base_color if not is_thermal else (200, 80, 20), badge_bg, border_radius=3)
    pygame.draw.rect(surface, (255, 255, 255), badge_bg, 1, border_radius=3)
    surface.blit(badge_surf, badge_surf.get_rect(center=badge_bg.center))


def draw_uav_drone(surface, x, y, prop_spin, is_dark, is_thermal, font):
    """Renders an autonomous aerial quadcopter reconnaissance drone with spotlight."""
    cx, cy = int(x), int(y)
    
    # 1. Soft aerial searchlight spotlight cast on ground
    spot_radius = 48
    spot_surf = pygame.Surface((spot_radius * 2, spot_radius * 2), pygame.SRCALPHA)
    spot_col = (0, 220, 255, 28) if (is_dark or is_thermal) else (255, 245, 180, 22)
    pygame.draw.circle(spot_surf, spot_col, (spot_radius, spot_radius), spot_radius)
    pygame.draw.circle(spot_surf, (spot_col[0], spot_col[1], spot_col[2], spot_col[3] + 15), (spot_radius, spot_radius), spot_radius // 2)
    surface.blit(spot_surf, (cx - spot_radius, cy - spot_radius))

    # 2. Drone Frame (X-configuration arms)
    arm_len = 14
    arm_col = (40, 45, 55) if not is_thermal else (80, 60, 110)
    for dx, dy in [(-arm_len, -arm_len), (arm_len, -arm_len), (-arm_len, arm_len), (arm_len, arm_len)]:
        pygame.draw.line(surface, arm_col, (cx, cy), (cx + dx, cy + dy), 2)
        pygame.draw.circle(surface, (25, 28, 35), (cx + dx, cy + dy), 3)

    # 3. 4 Animated Spinning Propellers
    prop_r = 7
    for dx, dy in [(-arm_len, -arm_len), (arm_len, -arm_len), (-arm_len, arm_len), (arm_len, arm_len)]:
        px = cx + dx
        py = cy + dy
        p_surf = pygame.Surface((prop_r * 2 + 2, prop_r * 2 + 2), pygame.SRCALPHA)
        pygame.draw.circle(p_surf, (200, 220, 255, 80), (prop_r + 1, prop_r + 1), prop_r, 1)
        ang = prop_spin + (dx * 1.5)
        bx = int(math.cos(ang) * prop_r)
        by = int(math.sin(ang) * prop_r)
        pygame.draw.line(surface, (220, 240, 255), (px - bx, py - by), (px + bx, py + by), 2)

    # 4. Central Fuselage & Gimbal Camera
    body_col = (20, 25, 35) if not is_thermal else (140, 40, 80)
    pygame.draw.circle(surface, body_col, (cx, cy), 6)
    pygame.draw.circle(surface, (0, 240, 255), (cx, cy), 3)

    # 5. Dual Navigation Strobes
    strobe_on = (int(prop_spin * 2) % 2 == 0)
    if strobe_on:
        pygame.draw.circle(surface, (255, 30, 30), (cx - arm_len, cy - arm_len), 2)
        pygame.draw.circle(surface, (30, 255, 60), (cx + arm_len, cy - arm_len), 2)

    # 6. Floating Callout Tag
    tag_surf = font.render("UAV-RECON", True, (0, 240, 255))
    surface.blit(tag_surf, (cx - 24, cy - 24))


def draw_ai_radio_ticker(surface, sim, font_mono, is_dark):
    """Draws a sleek, tactical live AI radio communications bar across the top of the grid."""
    if not sim.ai_radio_comms:
        return
        
    bar_rect = pygame.Rect(10, 6, WIDTH - 20, 22)
    bg_col = (12, 16, 24, 215) if is_dark else (240, 246, 255, 215)
    ticker_surf = pygame.Surface((bar_rect.w, bar_rect.h), pygame.SRCALPHA)
    ticker_surf.fill(bg_col)
    surface.blit(ticker_surf, bar_rect.topleft)
    pygame.draw.rect(surface, (0, 210, 255, 120), bar_rect, 1, border_radius=4)

    ts, sender, msg, col = sim.ai_radio_comms[-1]
    lead_txt = font_mono.render(f"📡 AI-SAR NET [{ts}] {sender}: ", True, (0, 230, 255))
    surface.blit(lead_txt, (18, 9))
    
    lead_w = lead_txt.get_width()
    msg_txt = font_mono.render(msg, True, col if is_dark else (20, 30, 45))
    surface.blit(msg_txt, (18 + lead_w, 9))


def draw_ekg_pulse(surface, x, y, w, h, t, is_critical=True):
    """Draws an animated oscilloscope heartbeat monitor line."""
    pygame.draw.rect(surface, (15, 20, 28), (x, y, w, h), border_radius=3)
    pygame.draw.rect(surface, (35, 45, 60), (x, y, w, h), 1, border_radius=3)
    pts = []
    col = (235, 60, 50) if is_critical else (30, 200, 95)
    speed = 90.0 if is_critical else 55.0
    for i in range(w):
        phase = (i - t * speed) % w
        val = 0
        if 18 <= phase < 22:
            val = 2
        elif 22 <= phase < 28:
            val = -h // 2 + 2
        elif 28 <= phase < 34:
            val = h // 2 - 2
        elif 34 <= phase < 38:
            val = -2
        py = y + h // 2 + val
        pts.append((x + i, py))
    if len(pts) > 1:
        pygame.draw.lines(surface, col, False, pts, 1)


def draw_radar_sweep(surface, cx, cy, radius, angle, is_dark, victims):
    """Draws an animated rotating radar sweep with survivor blips."""
    radar_col = (0, 220, 255, 70) if is_dark else (0, 140, 220, 50)
    pygame.draw.circle(surface, radar_col, (cx, cy), radius, 1)
    pygame.draw.circle(surface, radar_col, (cx, cy), radius // 2, 1)

    end_x = cx + math.cos(angle) * radius
    end_y = cy + math.sin(angle) * radius
    sweep_col = (0, 235, 255, 190) if is_dark else (0, 150, 240, 160)
    pygame.draw.line(surface, sweep_col, (cx, cy), (int(end_x), int(end_y)), 2)

    for v in victims:
        if not v.is_rescued:
            bx = cx + (v.pos[0] - 9) * 1.4
            by = cy + (v.pos[1] - 6) * 1.4
            pygame.draw.circle(surface, (255, 55, 55), (int(bx), int(by)), 2)


def draw_rounded_button(surface, rect, text, font, bg_color, text_color, border_color=None):
    """Draws an interactive modern UI button with rounded corners."""
    pygame.draw.rect(surface, bg_color, rect, border_radius=6)
    if border_color:
        pygame.draw.rect(surface, border_color, rect, 2, border_radius=6)
    txt_surf = font.render(text, True, text_color)
    surface.blit(txt_surf, txt_surf.get_rect(center=rect.center))


def draw_ai_triage_modal(surface, sim, font_title, font_bold, font_small, font_mono):
    """Renders the AI Multimodal Survivor Triage Scanner overlay with diagnostic biometrics."""
    mw, mh = 620, 420
    mx = (WIDTH - mw) // 2
    my = (HEIGHT - mh) // 2
    modal_rect = pygame.Rect(mx, my, mw, mh)

    dim_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dim_surf.fill((8, 12, 18, 220))
    surface.blit(dim_surf, (0, 0))

    pygame.draw.rect(surface, (16, 22, 34), modal_rect, border_radius=8)
    pygame.draw.rect(surface, (0, 210, 255), modal_rect, 2, border_radius=8)

    title = font_title.render("AI MULTIMODAL SURVIVOR TRIAGE SCANNER (v3.4-SAR)", True, (0, 230, 255))
    sub = font_small.render("Real-Time Autonomous Bio-Telemetry, Acoustic Sensing & Entrapment Analytics", True, (160, 185, 215))
    surface.blit(title, (mx + 20, my + 14))
    surface.blit(sub, (mx + 20, my + 36))
    pygame.draw.line(surface, (35, 55, 80), (mx + 20, my + 54), (mx + mw - 20, my + 54), 1)

    v_idx = sim.selected_victim_id if (sim.selected_victim_id is not None and sim.selected_victim_id < len(sim.victims)) else 0
    victim = sim.victims[v_idx] if sim.victims else None

    # Victim Selection Tabs
    tab_x = mx + 20
    for idx, v in enumerate(sim.victims):
        is_sel = (idx == v_idx)
        tab_bg = (0, 140, 200) if is_sel else (25, 34, 50)
        tab_rect = pygame.Rect(tab_x, my + 62, 110, 26)
        pygame.draw.rect(surface, tab_bg, tab_rect, border_radius=4)
        if is_sel:
            pygame.draw.rect(surface, (0, 240, 255), tab_rect, 1, border_radius=4)
        status_sym = " [OK]" if v.is_rescued else " [!]"
        t_surf = font_bold.render(f"{v.label}{status_sym}", True, (255, 255, 255) if is_sel else (150, 175, 200))
        surface.blit(t_surf, t_surf.get_rect(center=tab_rect.center))
        tab_x += 120

    if not victim:
        return

    # Left Column: Vitals Card
    vitals_rect = pygame.Rect(mx + 20, my + 98, 270, 265)
    pygame.draw.rect(surface, (22, 30, 46), vitals_rect, border_radius=6)
    pygame.draw.rect(surface, (45, 60, 85), vitals_rect, 1, border_radius=6)

    v_title = font_bold.render(f"PATIENT BIOMETRICS - {victim.label}", True, (0, 220, 255))
    surface.blit(v_title, (mx + 30, my + 108))

    draw_ekg_pulse(surface, mx + 30, my + 128, 250, 36, sim.mission_time * 2.0, is_critical=not victim.is_rescued)

    vitals_data = [
        ("Heart Rate:", f"{victim.heart_rate} BPM", (255, 70, 60) if not victim.is_rescued else (50, 230, 120)),
        ("Blood Oxygen (SpO2):", f"{victim.spo2}%", (255, 180, 50) if not victim.is_rescued else (50, 230, 120)),
        ("Core Body Temp:", f"{victim.core_temp} °C", (255, 210, 80) if not victim.is_rescued else (50, 230, 120)),
        ("Respiration Rate:", f"{victim.resp_rate} /min", (220, 235, 250)),
        ("Status:", "STABILIZED" if victim.is_rescued else "TRAPPED UNDER DEBRIS", (50, 230, 120) if victim.is_rescued else (255, 80, 60)),
        ("Rescued By:", f"Robot {victim.rescued_by + 1}" if victim.is_rescued else "Awaiting Infiltration", (0, 210, 255))
    ]

    vy = my + 172
    for label, val, val_col in vitals_data:
        surface.blit(font_small.render(label, True, (160, 180, 205)), (mx + 30, vy))
        surface.blit(font_bold.render(val, True, val_col), (mx + 175, vy))
        vy += 24

    # Right Column: Entrapment Analytics & Multi-Agent Tactical Response
    tactical_rect = pygame.Rect(mx + 305, my + 98, 295, 265)
    pygame.draw.rect(surface, (22, 30, 46), tactical_rect, border_radius=6)
    pygame.draw.rect(surface, (45, 60, 85), tactical_rect, 1, border_radius=6)

    t_title = font_bold.render("AI ENTRAPMENT & RESCUE PROTOCOL", True, (255, 200, 50))
    surface.blit(t_title, (mx + 315, my + 108))

    ai_data = [
        ("Location Grid:", f"({victim.pos[0]}, {victim.pos[1]}) in Disaster Zone"),
        ("Overhead Load:", f"{victim.entrapment_depth} m Reinforced Concrete"),
        ("Acoustic Sensor:", "Distress Tapping & Weak Pulse" if not victim.is_rescued else "Clear Vocalization"),
        ("AI Triage Tag:", victim.triage_level),
        ("Required Equipment:", victim.recommended_tool),
        ("Allocated Agent:", f"Robot 1 (Scout) -> Leading Route"),
        ("Multi-Agent ETA:", "0s (RESCUED)" if victim.is_rescued else f"{len(sim.robots[0].path) * 0.25:.1f}s via A* Space-Time")
    ]

    ay = my + 132
    for label, val in ai_data:
        is_tag = (label == "AI Triage Tag:")
        t_col = (255, 60, 60) if (is_tag and not victim.is_rescued) else (50, 230, 120) if is_tag else (225, 235, 250)
        surface.blit(font_small.render(label, True, (160, 180, 205)), (mx + 315, ay))
        surface.blit(font_bold.render(val, True, t_col), (mx + 315, ay + 14))
        ay += 32

    # Modal Footer
    footer_txt = font_bold.render("Press 'C' or Click to Close  |  Multimodal Fused Confidence: 97.4%", True, (0, 220, 255))
    surface.blit(footer_txt, footer_txt.get_rect(center=(mx + mw // 2, my + mh - 22)))


def draw_help_modal(surface, font_title, font_bold, font_small):
    """Renders a comprehensive translucent help & legend overlay."""
    modal_surf = pygame.Surface((WIDTH - 60, HEIGHT - 70), pygame.SRCALPHA)
    modal_surf.fill((16, 22, 32, 245))
    m_rect = pygame.Rect(30, 20, WIDTH - 60, HEIGHT - 70)
    surface.blit(modal_surf, (30, 20))
    pygame.draw.rect(surface, (0, 210, 255), m_rect, 2, border_radius=8)

    title = font_title.render("AI DISASTER RESCUE ROBOT - CONTROLS & ARCHITECTURE", True, (0, 220, 255))
    surface.blit(title, (50, 32))

    guide_lines = [
        ("KEY / SHORTCUT", "ACTION / DEMONSTRATION FEATURE"),
        ("R / Restart Button", "Restart Mission from the beginning"),
        ("SPACE / Pause Button", "Pause / Resume simulation execution"),
        ("S", "Single Step Mode: advance exactly 1 grid step for step-by-step viva explanation"),
        ("A / Algo Button", "Cycle Search Algorithm: A*  -->  Dijkstra  -->  Greedy Best-First  -->  BFS"),
        ("M", "Cycle Distance Metric: Manhattan (L1)  -->  Euclidean (L2)  -->  Chebyshev"),
        ("D / + Debris Button", "Trigger Debris Surge: drops 5 new rubble blocks with live online replanning"),
        ("C / Triage Button", "Toggle AI Multimodal Survivor Triage Scanner modal with live biometrics"),
        ("I / FLIR Button", "Toggle Military FLIR Thermal Infrared Vision mode"),
        ("T / Theme Button", "Cycle Themes: Classic White  -->  Tactical Dark  -->  FLIR Thermal"),
        ("F / Fog Button", "Toggle Fog of War (LiDAR Reconnaissance Mode)"),
        ("H", "Toggle A* Explored Nodes Heatmap (proves 85%+ search space pruning)"),
        ("1 - 5", "Load Pre-Configured Scenarios (1: Slide, 2: Chokepoint, 3: Swarm, 4: Tremor, 5: 71-Block Maze)"),
        ("Left Click", "Click any open cell to toggle rubble, or click a victim to open AI Triage"),
        ("P", "Save high-resolution screenshot to disaster_rescue_simulation.png"),
        ("F1", "Toggle this Help & Legend modal overlay")
    ]

    y_pos = 65
    for col1, col2 in guide_lines:
        is_header = (col1 == "KEY / SHORTCUT")
        col_color = (255, 220, 50) if is_header else (255, 255, 255)
        txt1 = font_bold.render(col1, True, col_color)
        txt2 = font_small.render(col2, True, (210, 225, 240) if not is_header else col_color)
        surface.blit(txt1, (50, y_pos))
        surface.blit(txt2, (220, y_pos + 1))
        y_pos += 24

    footer = font_bold.render("Press F1 or Click to Close Help Guide", True, (0, 220, 255))
    surface.blit(footer, footer.get_rect(center=(WIDTH // 2, HEIGHT - 32)))


def main():
    pygame.init()
    sound_effects.init_audio()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AI Disaster Rescue Robot (A* & Multi-Agent Planning)")
    clock = pygame.time.Clock()

    world_surf = pygame.Surface((WIDTH, ROWS * CELL))

    # Typography
    font_title = pygame.font.SysFont("Arial", 16, bold=True)
    font_bold = pygame.font.SysFont("Arial", 12, bold=True)
    font_regular = pygame.font.SysFont("Arial", 12)
    font_small = pygame.font.SysFont("Arial", 11)
    font_mono = pygame.font.SysFont("Consolas", 11)
    font_robot = pygame.font.SysFont("Arial", 10, bold=True)

    # State
    themes = [THEME_CLASSIC, THEME_TACTICAL, THEME_THERMAL]
    current_theme_idx = 0
    sim = RescueSimulation(scenario_id=1)
    show_help = False
    show_triage = False

    # 3x3 Button Grid Layout in Bottom Dashboard Panel
    panel_y = ROWS * CELL
    btn_w = 98
    btn_h = 28
    col1_x = 396
    col2_x = 502
    col3_x = 608

    row1_y = panel_y + 12
    row2_y = panel_y + 46
    row3_y = panel_y + 80

    algo_btn_rect     = pygame.Rect(col1_x, row1_y, btn_w, btn_h)
    theme_btn_rect    = pygame.Rect(col2_x, row1_y, btn_w, btn_h)
    restart_btn_rect  = pygame.Rect(col3_x, row1_y, btn_w, btn_h)

    debris_btn_rect   = pygame.Rect(col1_x, row2_y, btn_w, btn_h)
    flir_btn_rect     = pygame.Rect(col2_x, row2_y, btn_w, btn_h)
    pause_btn_rect    = pygame.Rect(col3_x, row2_y, btn_w, btn_h)

    fog_btn_rect      = pygame.Rect(col1_x, row3_y, btn_w, btn_h)
    triage_btn_rect   = pygame.Rect(col2_x, row3_y, btn_w, btn_h)
    scenario_btn_rect = pygame.Rect(col3_x, row3_y, btn_w, btn_h)

    pulse_timer = 0.0

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        pulse_timer += dt * 3.5

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    show_help = not show_help
                elif event.key == pygame.K_ESCAPE:
                    show_help = False
                    show_triage = False
                elif event.key == pygame.K_c:
                    show_triage = not show_triage
                    if show_triage and sim.victims:
                        sim.post_comms("AI-TRIAGE", f"Biometrics linked for {sim.victims[sim.selected_victim_id or 0].label}.", (0, 240, 255))
                elif event.key == pygame.K_r:
                    sim.restart()
                elif event.key == pygame.K_SPACE:
                    sim.is_paused = not sim.is_paused
                elif event.key == pygame.K_s:
                    sim.is_paused = True
                    sim.step()
                elif event.key == pygame.K_a:
                    sim.cycle_algorithm()
                elif event.key == pygame.K_m:
                    sim.cycle_heuristic()
                elif event.key == pygame.K_d:
                    sim.add_debris_surge(5)
                elif event.key == pygame.K_f:
                    sim.fog_of_war_enabled = not sim.fog_of_war_enabled
                elif event.key == pygame.K_h:
                    sim.show_heatmap = not sim.show_heatmap
                elif event.key == pygame.K_t:
                    current_theme_idx = (current_theme_idx + 1) % len(themes)
                elif event.key == pygame.K_i:
                    # Direct FLIR Thermal toggle
                    if current_theme_idx == 2:
                        current_theme_idx = 1
                    else:
                        current_theme_idx = 2
                elif event.key == pygame.K_n:
                    sim.generate_random_disaster()
                elif event.key == pygame.K_p:
                    pygame.image.save(screen, "disaster_rescue_simulation.png")
                    print("Screenshot captured to disaster_rescue_simulation.png")
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    s_id = event.key - pygame.K_0
                    sim.load_scenario(s_id)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # If modals are active, handle modal clicks
                if show_help:
                    show_help = False
                    continue

                if show_triage:
                    # Check victim tab clicks inside triage modal
                    mw, mh = 620, 420
                    modal_x = (WIDTH - mw) // 2
                    modal_y = (HEIGHT - mh) // 2
                    tab_x = modal_x + 20
                    clicked_tab = False
                    for idx in range(len(sim.victims)):
                        t_rect = pygame.Rect(tab_x, modal_y + 62, 110, 26)
                        if t_rect.collidepoint(mx, my):
                            sim.selected_victim_id = idx
                            clicked_tab = True
                            break
                        tab_x += 120
                    if not clicked_tab:
                        show_triage = False
                    continue

                # UI Button Interactions in Bottom Panel
                if algo_btn_rect.collidepoint(mx, my):
                    sim.cycle_algorithm()
                elif theme_btn_rect.collidepoint(mx, my):
                    current_theme_idx = (current_theme_idx + 1) % len(themes)
                elif restart_btn_rect.collidepoint(mx, my):
                    sim.restart()
                elif debris_btn_rect.collidepoint(mx, my):
                    sim.add_debris_surge(5)
                elif flir_btn_rect.collidepoint(mx, my):
                    current_theme_idx = 2 if current_theme_idx != 2 else 1
                elif pause_btn_rect.collidepoint(mx, my):
                    sim.is_paused = not sim.is_paused
                elif fog_btn_rect.collidepoint(mx, my):
                    sim.fog_of_war_enabled = not sim.fog_of_war_enabled
                elif triage_btn_rect.collidepoint(mx, my):
                    show_triage = not show_triage
                elif scenario_btn_rect.collidepoint(mx, my):
                    next_s = (sim.scenario_id % len(SCENARIOS)) + 1
                    sim.load_scenario(next_s)
                elif my < ROWS * CELL:
                    grid_c = mx // CELL
                    grid_r = my // CELL
                    # Check if clicked on a victim to inspect biometrics
                    victim_clicked = False
                    for idx, v in enumerate(sim.victims):
                        if v.pos == (grid_c, grid_r):
                            sim.selected_victim_id = idx
                            show_triage = True
                            victim_clicked = True
                            sim.post_comms("AI-TRIAGE", f"Manual uplink: {v.label} vitals retrieved.", (0, 240, 255))
                            break
                    if not victim_clicked:
                        sim.toggle_obstacle((grid_c, grid_r))

        # Update Simulation with continuous coordinate interpolation, UAV & particle physics
        sim.update(dt)

        # ---------------- RENDERING ----------------
        theme = themes[current_theme_idx]
        is_dark = (current_theme_idx >= 1)
        is_thermal = (current_theme_idx == 2)
        screen.fill(theme["bg"])
        world_surf.fill(theme["bg"])

        # 1. Draw A* Search Explored Nodes Heatmap (if enabled)
        if sim.show_heatmap:
            heat_colors = [theme["heatmap_r1"], theme["heatmap_r2"], theme["heatmap_r3"]]
            for idx, r in enumerate(sim.robots):
                h_col = heat_colors[idx % len(heat_colors)]
                for (ec, er) in r.explored_nodes:
                    if (ec, er) not in sim.obstacles:
                        h_rect = pygame.Rect(ec * CELL, er * CELL, CELL, CELL)
                        pygame.draw.rect(world_surf, h_col, h_rect)

        # 2. Draw Floor Grid
        for c in range(COLS + 1):
            pygame.draw.line(world_surf, theme["grid_line"], (c * CELL, 0), (c * CELL, ROWS * CELL), 1)
        for r in range(ROWS + 1):
            pygame.draw.line(world_surf, theme["grid_line"], (0, r * CELL), (COLS * CELL, r * CELL), 1)

        # 3. Draw Realistic Fractured Concrete Rubble Obstacles
        for (oc, orow) in sim.obstacles:
            draw_realistic_rubble(world_surf, oc * CELL, orow * CELL, CELL, is_dark, is_thermal)

        # 4. Draw Planned & Traversed Path Lines
        for r in sim.robots:
            if len(r.trail) > 1:
                pts = [(p[0] * CELL + CELL // 2, p[1] * CELL + CELL // 2) for p in r.trail]
                pygame.draw.lines(world_surf, r.color if not is_thermal else (255, 120, 40), False, pts, 4)

            if len(r.path) > r.path_index:
                future_pts = [(r.render_x * CELL + CELL // 2, r.render_y * CELL + CELL // 2)]
                future_pts += [(p[0] * CELL + CELL // 2, p[1] * CELL + CELL // 2) for p in r.path[r.path_index + 1:]]
                if len(future_pts) > 1:
                    faded = (min(255, r.color[0] + 50), min(255, r.color[1] + 50), min(255, r.color[2] + 50))
                    if is_thermal:
                        faded = (255, 180, 80)
                    pygame.draw.lines(world_surf, faded, False, future_pts, 2)

        # 5. Draw Realistic Persons (Trapped Victims with Waving Distress SOS or Thermal Glow)
        for v in sim.victims:
            vx = v.pos[0] * CELL + CELL // 2
            vy = v.pos[1] * CELL + CELL // 2
            draw_realistic_person(world_surf, vx, vy, v.label, v.is_rescued, pulse_timer, font_small, is_thermal)

        # 6. Draw Realistic Search & Rescue Robots (Tracked Rovers with Headlights)
        for r in sim.robots:
            rx = r.render_x * CELL + CELL // 2
            ry = r.render_y * CELL + CELL // 2
            draw_robot_rover(world_surf, rx, ry, r.heading_angle, r.color, r.id, r.status, is_dark, font_robot, is_thermal)

        # 7. Draw Active Particle Systems (Tread dust, debris explosions, rescue sparkles)
        sim.particles.draw(world_surf)

        # 8. Draw Autonomous Aerial Reconnaissance Drone Cruising Overhead
        draw_uav_drone(world_surf, sim.uav_x, sim.uav_y, sim.prop_spin, is_dark, is_thermal, font_small)

        # 9. Dynamic Fog of War & Reconnaissance Scanner Mode (if enabled)
        if sim.fog_of_war_enabled:
            dark_overlay = pygame.Surface((WIDTH, ROWS * CELL), pygame.SRCALPHA)
            dark_overlay.fill((10, 14, 22, 220))
            for r in sim.robots:
                rx = int(r.render_x * CELL + CELL // 2)
                ry = int(r.render_y * CELL + CELL // 2)
                pygame.draw.circle(dark_overlay, (0, 0, 0, 0), (rx, ry), 130)
            # UAV also provides a reconnaissance circle
            pygame.draw.circle(dark_overlay, (0, 0, 0, 0), (int(sim.uav_x), int(sim.uav_y)), 90)
            world_surf.blit(dark_overlay, (0, 0))

        # 10. Tactical Radar Scanner Sweep in Upper Right
        draw_radar_sweep(world_surf, WIDTH - 35, 38, 25, pulse_timer * 1.5, is_dark, sim.victims)

        # 11. Live AI Radio Communications Ticker Banner across top
        draw_ai_radio_ticker(world_surf, sim, font_mono, is_dark)

        # 12. Blit World Surface onto Screen with Earthquake Tremor Shake Offset
        shake_dx, shake_dy = sim.particles.get_shake_offset()
        screen.blit(world_surf, (shake_dx, shake_dy))

        # 13. Bottom Rescue Mission Dashboard Panel
        dash_rect = pygame.Rect(0, panel_y, WIDTH, PANEL)
        pygame.draw.rect(screen, theme["panel_bg"], dash_rect)
        pygame.draw.line(screen, theme["panel_border"], (0, panel_y), (WIDTH, panel_y), 2)

        # Left Column: Mission Status, Progress & EKG Monitor
        screen.blit(font_title.render("RESCUE MISSION DASHBOARD", True, theme["text_dark"]), (14, panel_y + 8))

        rescued_count = sim.victims_rescued_count
        total_victims = len(sim.victims)
        resc_str = f"Victims: {rescued_count}/{total_victims} Rescued"
        screen.blit(font_bold.render(resc_str, True, theme["text_dark"]), (14, panel_y + 32))

        prog_percent = sim.progress_percent
        bar_x, bar_y, bar_w, bar_h = 14, panel_y + 54, 110, 12
        pygame.draw.rect(screen, theme["border_light"], (bar_x, bar_y, bar_w, bar_h), border_radius=4)
        fill_w = int((bar_w * prog_percent) / 100)
        if fill_w > 0:
            pygame.draw.rect(screen, COLOR_RESCUED, (bar_x, bar_y, fill_w, bar_h), border_radius=4)
        pygame.draw.rect(screen, theme["panel_border"], (bar_x, bar_y, bar_w, bar_h), 1, border_radius=4)
        screen.blit(font_mono.render(f"{prog_percent}%", True, theme["text_dark"]), (bar_x + bar_w + 6, bar_y - 1))

        all_rescued = (rescued_count == total_victims)
        draw_ekg_pulse(screen, 14, panel_y + 74, 90, 20, pulse_timer, is_critical=not all_rescued)
        ekg_bpm = "75 BPM (STABLE)" if all_rescued else "135 BPM (CRITICAL)"
        ekg_col = COLOR_RESCUED if all_rescued else COLOR_VICTIM
        screen.blit(font_mono.render(f"💓 {ekg_bpm}", True, ekg_col), (110, panel_y + 78))

        scen_info = SCENARIOS.get(sim.scenario_id, {})
        scen_name = scen_info.get("name", "Custom")
        scen_diff = scen_info.get("difficulty", "Normal")
        screen.blit(font_small.render(f"Sector: {scen_name} ({scen_diff})", True, theme["text_muted"]), (14, panel_y + 104))

        # Middle Column: High-Level Algorithmic Telemetry & Benchmark
        mid_x = 210
        card_w = 175
        card_rect = pygame.Rect(mid_x, panel_y + 8, card_w, PANEL - 16)
        pygame.draw.rect(screen, theme["card_bg"], card_rect, border_radius=6)
        pygame.draw.rect(screen, theme["panel_border"], card_rect, 1, border_radius=6)

        screen.blit(font_bold.render("AI TELEMETRY & BENCHMARK", True, theme["text_dark"]), (mid_x + 8, panel_y + 12))
        screen.blit(font_mono.render(f"Algorithm: {sim.current_algorithm}", True, COLOR_CYAN), (mid_x + 8, panel_y + 32))
        screen.blit(font_mono.render(f"Metric: {sim.current_heuristic}", True, theme["text_muted"]), (mid_x + 8, panel_y + 50))
        screen.blit(font_mono.render(f"Prune: {sim.pruning_ratio:.1f}% ({sim.total_explored_nodes}/{COLS*ROWS})", True, theme["text_muted"]), (mid_x + 8, panel_y + 68))
        screen.blit(font_mono.render(f"Compute Time: {sim.total_compute_time_ms:.2f}ms", True, theme["text_muted"]), (mid_x + 8, panel_y + 86))
        screen.blit(font_mono.render(f"Space-Time Yields: {sim.conflicts_avoided}", True, COLOR_WARNING if sim.conflicts_avoided > 0 else COLOR_RESCUED), (mid_x + 8, panel_y + 104))

        # Right Side 3x3 Button Grid
        btn_bg = theme["card_bg"]
        btn_border = theme["panel_border"]
        btn_txt_col = theme["text_dark"]

        # Row 1
        draw_rounded_button(screen, algo_btn_rect, f"ALGO: {sim.current_algorithm}", font_small, btn_bg, COLOR_CYAN, btn_border)
        theme_names = ["CLASSIC", "TACTICAL", "FLIR IR"]
        draw_rounded_button(screen, theme_btn_rect, f"THEME: {theme_names[current_theme_idx]}", font_small, btn_bg, btn_txt_col, btn_border)
        draw_rounded_button(screen, restart_btn_rect, "RESTART (R)", font_bold, COLOR_R1_SCOUT, (255, 255, 255))

        # Row 2
        draw_rounded_button(screen, debris_btn_rect, "+ DEBRIS (D)", font_small, btn_bg, (240, 130, 30), btn_border)
        flir_col = (255, 140, 30) if is_thermal else btn_txt_col
        draw_rounded_button(screen, flir_btn_rect, "FLIR IR (I)", font_small, btn_bg, flir_col, btn_border)
        pause_txt = "RESUME" if sim.is_paused else "PAUSE"
        draw_rounded_button(screen, pause_btn_rect, pause_txt, font_small, btn_bg, btn_txt_col, btn_border)

        # Row 3
        fog_txt = "FOG: ON" if sim.fog_of_war_enabled else "FOG: OFF"
        fog_col = COLOR_RESCUED if sim.fog_of_war_enabled else theme["text_muted"]
        draw_rounded_button(screen, fog_btn_rect, fog_txt, font_small, btn_bg, fog_col, btn_border)
        triage_col = (0, 230, 255) if show_triage else btn_txt_col
        draw_rounded_button(screen, triage_btn_rect, "TRIAGE (C)", font_small, btn_bg, triage_col, btn_border)
        draw_rounded_button(screen, scenario_btn_rect, f"Sector {sim.scenario_id}", font_bold, btn_bg, btn_txt_col, btn_border)

        # 14. Modals Overlays (Help & AI Triage)
        if show_triage:
            draw_ai_triage_modal(screen, sim, font_title, font_bold, font_small, font_mono)
        elif show_help:
            draw_help_modal(screen, font_title, font_bold, font_small)

        # Buffer flip
        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
