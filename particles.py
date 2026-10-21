"""
Advanced Particle and Visual Effects System for AI Disaster Rescue Robot.
Features:
- Tank tread dust and smoke puffs
- Concrete rubble explosion & debris shards
- Rescued survivor sparkle bursts
- Earthquake tremor screen-shake physics
- Ambient atmospheric disaster dust motes
"""

import math
import random
from typing import List, Tuple
import pygame


class Particle:
    """Represents an individual physical particle."""
    
    def __init__(self, x: float, y: float, vx: float, vy: float, color, size: float, lifetime: float, is_cross: bool = False):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.max_life = lifetime
        self.life = lifetime
        self.is_cross = is_cross

    def update(self, dt: float) -> bool:
        self.x += self.vx * dt
        self.y += self.vy * dt
        # Gentle air resistance & gravity
        self.vx *= 0.94
        self.vy += 12.0 * dt
        self.life -= dt
        return self.life > 0

    def draw(self, surface: pygame.Surface):
        if self.life <= 0:
            return
        ratio = max(0.0, min(1.0, self.life / self.max_life))
        alpha = int(255 * ratio)
        cur_size = max(1, int(self.size * (0.6 + 0.4 * ratio)))

        p_surf = pygame.Surface((cur_size * 2 + 4, cur_size * 2 + 4), pygame.SRCALPHA)
        col = (self.color[0], self.color[1], self.color[2], alpha)
        
        if self.is_cross:
            # Floating medical cross (+)
            c = cur_size + 2
            pygame.draw.rect(p_surf, col, (c - 1, c - cur_size, 3, cur_size * 2))
            pygame.draw.rect(p_surf, col, (c - cur_size, c - 1, cur_size * 2, 3))
        else:
            pygame.draw.circle(p_surf, col, (cur_size + 2, cur_size + 2), cur_size)
            
        surface.blit(p_surf, (int(self.x - cur_size - 2), int(self.y - cur_size - 2)))


class ParticleManager:
    """Manages particle emitters, ambient atmospheric effects, and camera screen-shake."""
    
    def __init__(self):
        self.particles: List[Particle] = []
        self.shake_timer = 0.0
        self.shake_intensity = 0.0

    def trigger_shake(self, duration: float = 0.35, intensity: float = 4.0):
        """Triggers an earthquake camera shake effect."""
        self.shake_timer = duration
        self.shake_intensity = intensity

    def get_shake_offset(self) -> Tuple[int, int]:
        """Calculates current camera tremor offset."""
        if self.shake_timer > 0:
            dx = random.randint(-int(self.shake_intensity), int(self.shake_intensity))
            dy = random.randint(-int(self.shake_intensity), int(self.shake_intensity))
            return (dx, dy)
        return (0, 0)

    def emit_tread_dust(self, x: float, y: float, heading_angle: float):
        """Emits subtle dust puffs behind moving caterpillar tracks."""
        rear_angle = heading_angle + math.pi
        for _ in range(2):
            spread = random.uniform(-0.5, 0.5)
            speed = random.uniform(8.0, 25.0)
            vx = math.cos(rear_angle + spread) * speed
            vy = math.sin(rear_angle + spread) * speed
            dust_col = random.choice([(190, 185, 175), (170, 165, 155), (210, 205, 195)])
            self.particles.append(Particle(
                x + random.uniform(-4, 4),
                y + random.uniform(-4, 4),
                vx, vy,
                dust_col,
                random.uniform(2.5, 4.5),
                random.uniform(0.3, 0.55)
            ))

    def emit_collapse_debris(self, x: float, y: float):
        """Emits an explosion of concrete shards and gray dust when rubble collapses."""
        self.trigger_shake(0.3, 4.5)
        # Smoke dust cloud
        for _ in range(16):
            ang = random.uniform(0, 2 * math.pi)
            spd = random.uniform(15.0, 60.0)
            col = random.choice([(140, 145, 155), (110, 115, 125), (175, 180, 190)])
            self.particles.append(Particle(
                x, y,
                math.cos(ang) * spd,
                math.sin(ang) * spd,
                col,
                random.uniform(3.5, 7.0),
                random.uniform(0.4, 0.8)
            ))
        # Concrete rock chips
        for _ in range(8):
            ang = random.uniform(0, 2 * math.pi)
            spd = random.uniform(30.0, 85.0)
            col = random.choice([(70, 75, 85), (175, 75, 40)]) # rock + rebar
            self.particles.append(Particle(
                x, y,
                math.cos(ang) * spd,
                math.sin(ang) * spd,
                col,
                random.uniform(2.0, 3.5),
                random.uniform(0.5, 0.9)
            ))

    def emit_rescue_sparkles(self, x: float, y: float):
        """Emits glowing medical crosses and emerald sparkles when a survivor is rescued."""
        for _ in range(14):
            ang = random.uniform(0, 2 * math.pi)
            spd = random.uniform(20.0, 70.0)
            col = random.choice([(30, 215, 110), (0, 255, 170), (255, 255, 200)])
            self.particles.append(Particle(
                x, y,
                math.cos(ang) * spd,
                math.sin(ang) * spd - 25.0, # Float upward
                col,
                random.uniform(3.0, 5.0),
                random.uniform(0.6, 1.1),
                is_cross=random.random() < 0.5
            ))

    def update(self, dt: float):
        if self.shake_timer > 0:
            self.shake_timer -= dt
            if self.shake_timer <= 0:
                self.shake_intensity = 0.0

        # Update all active particles
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, surface: pygame.Surface):
        for p in self.particles:
            p.draw(surface)
