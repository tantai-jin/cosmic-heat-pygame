import pygame
import random
import math
from classes.constants import WIDTH, HEIGHT


class Star:
    """A single star with parallax movement and twinkling effect."""
    
    def __init__(self, layer):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.layer = layer  # 0=far, 1=mid, 2=near
        
        # Size and speed based on layer (parallax)
        if layer == 0:
            self.size = random.randint(1, 2)
            self.speed = random.uniform(0.3, 0.6)
            self.base_brightness = random.randint(80, 120)
        elif layer == 1:
            self.size = random.randint(1, 3)
            self.speed = random.uniform(0.8, 1.5)
            self.base_brightness = random.randint(120, 180)
        else:
            self.size = random.randint(2, 4)
            self.speed = random.uniform(2.0, 3.5)
            self.base_brightness = random.randint(180, 255)
        
        # Twinkling effect
        self.twinkle_phase = random.uniform(0, 2 * math.pi)
        self.twinkle_speed = random.uniform(0.05, 0.15)
        
        # Color variation (white to blue-ish)
        self.color_type = random.choice(['white', 'blue', 'yellow'])
    
    def update(self, speed_multiplier=1.0):
        self.y += self.speed * speed_multiplier
        self.twinkle_phase += self.twinkle_speed
        
        if self.y > HEIGHT:
            self.y = -self.size
            self.x = random.randint(0, WIDTH)
    
    def draw(self, surface):
        # Calculate twinkling brightness
        twinkle = math.sin(self.twinkle_phase) * 40
        brightness = max(0, min(255, int(self.base_brightness + twinkle)))
        
        # Get color based on type
        if self.color_type == 'white':
            color = (brightness, brightness, brightness)
        elif self.color_type == 'blue':
            color = (int(brightness * 0.7), int(brightness * 0.8), brightness)
        else:  # yellow
            color = (brightness, brightness, int(brightness * 0.7))
        
        if self.size <= 2:
            surface.set_at((int(self.x), int(self.y)), color)
            if self.size == 2:
                surface.set_at((int(self.x) + 1, int(self.y)), color)
        else:
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size // 2)


class Comet:
    """A comet with a glowing trail effect."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        # Start from random edge position
        side = random.choice(['top', 'top-left', 'top-right'])
        
        if side == 'top':
            self.x = random.randint(100, WIDTH - 100)
            self.y = -50
            self.vx = random.uniform(-1, 1)
            self.vy = random.uniform(4, 8)
        elif side == 'top-left':
            self.x = -50
            self.y = random.randint(-50, HEIGHT // 3)
            self.vx = random.uniform(3, 6)
            self.vy = random.uniform(3, 6)
        else:
            self.x = WIDTH + 50
            self.y = random.randint(-50, HEIGHT // 3)
            self.vx = random.uniform(-6, -3)
            self.vy = random.uniform(3, 6)
        
        # Trail positions
        self.trail = []
        self.trail_length = random.randint(15, 30)
        self.active = True
        
        # Comet properties
        self.size = random.randint(3, 6)
        self.core_color = (255, 255, 255)
        self.glow_color = random.choice([
            (100, 150, 255),  # Blue
            (255, 200, 100),  # Gold
            (200, 255, 200),  # Green-ish
        ])
    
    def update(self, speed_multiplier=1.0):
        if not self.active:
            return
        
        # Store current position in trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)
        
        # Move comet
        self.x += self.vx * speed_multiplier
        self.y += self.vy * speed_multiplier
        
        # Check if offscreen
        if self.y > HEIGHT + 100 or self.x < -100 or self.x > WIDTH + 100:
            self.active = False
    
    def draw(self, surface):
        if not self.active:
            return
        
        # Draw trail with fading effect
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)) * 0.6)
            trail_size = max(1, int(self.size * (i / len(self.trail))))
            
            # Create a small surface for the trail segment with alpha
            if trail_size > 0:
                glow_r = int(self.glow_color[0] * (i / len(self.trail)))
                glow_g = int(self.glow_color[1] * (i / len(self.trail)))
                glow_b = int(self.glow_color[2] * (i / len(self.trail)))
                pygame.draw.circle(surface, (glow_r, glow_g, glow_b), 
                                 (int(tx), int(ty)), trail_size)
        
        # Draw comet core with glow
        pygame.draw.circle(surface, self.glow_color, (int(self.x), int(self.y)), self.size + 2)
        pygame.draw.circle(surface, self.core_color, (int(self.x), int(self.y)), self.size)


class ShootingStar:
    """Fast-moving shooting star effect."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-100, -10)
        
        # Diagonal movement (mostly down, slightly sideways)
        angle = random.uniform(math.pi / 6, math.pi / 3)  # 30-60 degrees
        if random.random() < 0.5:
            angle = math.pi - angle  # Sometimes go other direction
        
        speed = random.uniform(10, 20)
        self.vx = math.cos(angle) * speed
        self.vy = abs(math.sin(angle)) * speed
        
        self.trail = []
        self.trail_length = random.randint(8, 15)
        self.active = True
        self.brightness = 255
    
    def update(self, speed_multiplier=1.0):
        if not self.active:
            return
        
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)
        
        self.x += self.vx * speed_multiplier
        self.y += self.vy * speed_multiplier
        
        if self.y > HEIGHT + 50 or self.x < -50 or self.x > WIDTH + 50:
            self.active = False
    
    def draw(self, surface):
        if not self.active or len(self.trail) < 2:
            return
        
        # Draw trail as lines with fading
        for i in range(len(self.trail) - 1):
            alpha = int(255 * (i / len(self.trail)))
            color = (alpha, alpha, alpha)
            pygame.draw.line(surface, color, 
                           (int(self.trail[i][0]), int(self.trail[i][1])),
                           (int(self.trail[i + 1][0]), int(self.trail[i + 1][1])), 1)
        
        # Draw bright head
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), 2)


class Nebula:
    """Distant nebula effect for atmosphere."""
    
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(80, 200)
        self.color = random.choice([
            (30, 20, 60),   # Purple
            (20, 40, 60),   # Blue
            (40, 20, 30),   # Red-ish
        ])
        self.alpha = random.randint(15, 35)
        self.speed = random.uniform(0.1, 0.3)
        self.pulse_phase = random.uniform(0, 2 * math.pi)
        self.pulse_speed = random.uniform(0.01, 0.03)
    
    def update(self, speed_multiplier=1.0):
        self.y += self.speed * speed_multiplier
        self.pulse_phase += self.pulse_speed
        
        if self.y > HEIGHT + self.size:
            self.y = -self.size
            self.x = random.randint(0, WIDTH)
    
    def draw(self, surface):
        # Pulsing size effect
        pulse = math.sin(self.pulse_phase) * 10
        current_size = int(self.size + pulse)
        
        # Create nebula effect using multiple overlapping circles
        for i in range(3, 0, -1):
            r = current_size // i
            alpha = self.alpha // i
            color = (
                min(255, self.color[0] + 10 * (3 - i)),
                min(255, self.color[1] + 10 * (3 - i)),
                min(255, self.color[2] + 10 * (3 - i))
            )
            nebula_surface = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(nebula_surface, (*color, alpha), (r, r), r)
            surface.blit(nebula_surface, (int(self.x) - r, int(self.y) - r))


class DynamicBackground:
    """Manages the complete dynamic background system."""
    
    def __init__(self):
        # Create stars in different layers for parallax
        self.stars = []
        for _ in range(100):  # Far layer
            self.stars.append(Star(0))
        for _ in range(60):   # Mid layer
            self.stars.append(Star(1))
        for _ in range(30):   # Near layer
            self.stars.append(Star(2))
        
        # Comets and shooting stars (spawned dynamically)
        self.comets = []
        self.shooting_stars = []
        self.comet_spawn_timer = 0
        self.shooting_star_spawn_timer = 0
        
        # Nebulae (background atmosphere)
        self.nebulae = [Nebula() for _ in range(3)]
        
        # Speed multiplier increases with score
        self.speed_multiplier = 1.0
        
        # Pre-render the base background
        self.base_surface = pygame.Surface((WIDTH, HEIGHT))
        self.base_surface.fill((5, 5, 15))  # Deep space color
    
    def update(self, score=0):
        # Adjust speed based on score
        if score > 15000:
            self.speed_multiplier = 2.5
        elif score > 10000:
            self.speed_multiplier = 2.0
        elif score > 3000:
            self.speed_multiplier = 1.5
        else:
            self.speed_multiplier = 1.0
        
        # Update stars
        for star in self.stars:
            star.update(self.speed_multiplier)
        
        # Update nebulae
        for nebula in self.nebulae:
            nebula.update(self.speed_multiplier)
        
        # Update and clean up comets
        for comet in self.comets[:]:
            comet.update(self.speed_multiplier)
            if not comet.active:
                self.comets.remove(comet)
        
        # Update and clean up shooting stars
        for ss in self.shooting_stars[:]:
            ss.update(self.speed_multiplier)
            if not ss.active:
                self.shooting_stars.remove(ss)
        
        # Spawn new comets
        self.comet_spawn_timer += 1
        if self.comet_spawn_timer > 180 and len(self.comets) < 3:  # Every ~3 seconds
            if random.random() < 0.02:  # Low chance per frame
                self.comets.append(Comet())
                self.comet_spawn_timer = 0
        
        # Spawn shooting stars
        self.shooting_star_spawn_timer += 1
        if self.shooting_star_spawn_timer > 60 and len(self.shooting_stars) < 5:
            if random.random() < 0.03:
                self.shooting_stars.append(ShootingStar())
                self.shooting_star_spawn_timer = 0
    
    def draw(self, surface):
        # Draw base space color
        surface.blit(self.base_surface, (0, 0))
        
        # Draw nebulae first (background)
        for nebula in self.nebulae:
            nebula.draw(surface)
        
        # Draw stars (sorted by layer for proper parallax)
        for star in sorted(self.stars, key=lambda s: s.layer):
            star.draw(surface)
        
        # Draw comets
        for comet in self.comets:
            comet.draw(surface)
        
        # Draw shooting stars
        for ss in self.shooting_stars:
            ss.draw(surface)
