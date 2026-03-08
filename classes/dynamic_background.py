"""Dynamic background with parallax stars and comet effects."""

import random
import math
import pygame
from .constants import WIDTH, HEIGHT


class Star:
    """A single star with parallax motion."""
    
    def __init__(self, layer):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.layer = layer  # 0=far, 1=mid, 2=close
        
        # Layer determines size, speed, and brightness
        if layer == 0:
            self.size = 1
            self.speed = 0.5
            self.base_brightness = random.randint(80, 120)
        elif layer == 1:
            self.size = random.randint(1, 2)
            self.speed = 1.5
            self.base_brightness = random.randint(140, 180)
        else:
            self.size = random.randint(2, 3)
            self.speed = 3.0
            self.base_brightness = random.randint(200, 255)
        
        self.brightness = self.base_brightness
        self.twinkle_phase = random.uniform(0, 2 * math.pi)
        self.twinkle_speed = random.uniform(2, 5)
    
    def update(self, speed_multiplier=1.0):
        self.y += self.speed * speed_multiplier
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)
        
        # Twinkle effect
        self.twinkle_phase += 0.1
        twinkle = math.sin(self.twinkle_phase * self.twinkle_speed) * 30
        self.brightness = max(50, min(255, int(self.base_brightness + twinkle)))
    
    def draw(self, surface):
        color = (self.brightness, self.brightness, self.brightness + 20)
        color = tuple(min(255, c) for c in color)
        if self.size == 1:
            surface.set_at((int(self.x), int(self.y)), color)
        else:
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)


class Comet:
    """A comet with trailing tail effect."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        # Start from top or sides
        side = random.choice(['top', 'left', 'right'])
        if side == 'top':
            self.x = random.randint(0, WIDTH)
            self.y = -50
            self.vx = random.uniform(-2, 2)
            self.vy = random.uniform(4, 8)
        elif side == 'left':
            self.x = -50
            self.y = random.randint(0, HEIGHT // 2)
            self.vx = random.uniform(3, 6)
            self.vy = random.uniform(2, 5)
        else:
            self.x = WIDTH + 50
            self.y = random.randint(0, HEIGHT // 2)
            self.vx = random.uniform(-6, -3)
            self.vy = random.uniform(2, 5)
        
        self.active = True
        self.tail_length = random.randint(15, 30)
        self.trail = []
        self.color = random.choice([
            (200, 220, 255),  # Blue-white
            (255, 240, 200),  # Warm white
            (180, 200, 255),  # Cool blue
        ])
        self.size = random.randint(3, 5)
    
    def update(self, speed_multiplier=1.0):
        if not self.active:
            return
        
        # Store trail position
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.tail_length:
            self.trail.pop(0)
        
        self.x += self.vx * speed_multiplier
        self.y += self.vy * speed_multiplier
        
        # Deactivate when off screen
        if self.y > HEIGHT + 100 or self.x < -100 or self.x > WIDTH + 100:
            self.active = False
    
    def draw(self, surface):
        if not self.active:
            return
        
        # Draw tail (gradient fade)
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)) * 0.6)
            size = max(1, int(self.size * (i / len(self.trail))))
            fade_color = tuple(int(c * (i / len(self.trail))) for c in self.color)
            pygame.draw.circle(surface, fade_color, (int(tx), int(ty)), size)
        
        # Draw comet head with glow
        glow_size = self.size + 3
        glow_color = tuple(min(255, c + 50) for c in self.color)
        pygame.draw.circle(surface, glow_color, (int(self.x), int(self.y)), glow_size)
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.size)


class Nebula:
    """Subtle nebula/dust cloud effect."""
    
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-200, HEIGHT)
        self.radius = random.randint(100, 200)
        self.color = random.choice([
            (40, 20, 60),   # Purple
            (20, 30, 50),   # Blue
            (50, 20, 30),   # Red
        ])
        self.alpha = random.randint(15, 30)
        self.speed = 0.2
    
    def update(self, speed_multiplier=1.0):
        self.y += self.speed * speed_multiplier
        if self.y > HEIGHT + self.radius:
            self.y = -self.radius * 2
            self.x = random.randint(0, WIDTH)
    
    def draw(self, surface):
        # Create a temporary surface for the nebula with alpha
        nebula_surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        for r in range(self.radius, 0, -10):
            alpha = int(self.alpha * (r / self.radius))
            color = (*self.color, alpha)
            pygame.draw.circle(nebula_surf, color, (self.radius, self.radius), r)
        surface.blit(nebula_surf, (int(self.x - self.radius), int(self.y - self.radius)))


class DynamicBackground:
    """Manages the dynamic space background with stars and comets."""
    
    def __init__(self):
        # Create star layers
        self.stars = []
        for _ in range(150):  # Far stars
            self.stars.append(Star(0))
        for _ in range(80):   # Mid stars
            self.stars.append(Star(1))
        for _ in range(30):   # Close stars
            self.stars.append(Star(2))
        
        # Create nebulae
        self.nebulae = [Nebula() for _ in range(3)]
        
        # Comet pool
        self.comets = []
        self.comet_timer = 0
        self.comet_interval = 180  # Frames between potential comet spawns
        
        # Background gradient colors
        self.bg_colors = [
            ((5, 5, 15), (15, 10, 30)),      # Deep space purple
            ((5, 10, 20), (10, 20, 35)),     # Deep space blue
            ((10, 5, 15), (25, 15, 35)),     # Nebula purple
            ((5, 15, 20), (15, 30, 40)),     # Teal space
        ]
        self.current_bg_index = 0
        self.next_bg_index = 1
        self.bg_transition = 0.0
        self.bg_transition_speed = 0.0005
        
        # Pre-render base surface for performance
        self.base_surface = pygame.Surface((WIDTH, HEIGHT))
        self._render_gradient()
    
    def _render_gradient(self):
        """Render vertical gradient background."""
        top_color = self._lerp_color(
            self.bg_colors[self.current_bg_index][0],
            self.bg_colors[self.next_bg_index][0],
            self.bg_transition
        )
        bottom_color = self._lerp_color(
            self.bg_colors[self.current_bg_index][1],
            self.bg_colors[self.next_bg_index][1],
            self.bg_transition
        )
        
        for y in range(HEIGHT):
            t = y / HEIGHT
            color = self._lerp_color(top_color, bottom_color, t)
            pygame.draw.line(self.base_surface, color, (0, y), (WIDTH, y))
    
    def _lerp_color(self, c1, c2, t):
        """Linear interpolation between two colors."""
        return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
    
    def update(self, score=0):
        """Update all background elements."""
        # Speed multiplier based on score
        speed_mult = 1.0
        if score > 3000:
            speed_mult = 1.5
        if score > 10000:
            speed_mult = 2.0
        if score > 15000:
            speed_mult = 2.5
        
        # Update stars
        for star in self.stars:
            star.update(speed_mult)
        
        # Update nebulae
        for nebula in self.nebulae:
            nebula.update(speed_mult)
        
        # Update comets
        for comet in self.comets:
            comet.update(speed_mult)
        self.comets = [c for c in self.comets if c.active]
        
        # Spawn new comets
        self.comet_timer += 1
        if self.comet_timer >= self.comet_interval:
            self.comet_timer = 0
            if random.random() < 0.3 and len(self.comets) < 3:
                self.comets.append(Comet())
        
        # Update background gradient transition
        self.bg_transition += self.bg_transition_speed
        if self.bg_transition >= 1.0:
            self.bg_transition = 0.0
            self.current_bg_index = self.next_bg_index
            self.next_bg_index = (self.next_bg_index + 1) % len(self.bg_colors)
        
        # Re-render gradient (only occasionally for performance)
        if random.random() < 0.05:
            self._render_gradient()
    
    def draw(self, surface):
        """Draw the complete background."""
        # Draw base gradient
        surface.blit(self.base_surface, (0, 0))
        
        # Draw nebulae (behind stars)
        for nebula in self.nebulae:
            nebula.draw(surface)
        
        # Draw stars by layer (far to close)
        for star in sorted(self.stars, key=lambda s: s.layer):
            star.draw(surface)
        
        # Draw comets
        for comet in self.comets:
            comet.draw(surface)
