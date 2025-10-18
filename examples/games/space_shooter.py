"""
Space Shooter Game - PyRay Implementation
A complete vertical scrolling shooter with enemies, power-ups, and boss battles
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pyray
import random
import math
from enum import Enum
from typing import List, Optional

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    PAUSED = 3
    VICTORY = 4

class EntityType(Enum):
    PLAYER = 0
    ENEMY = 1
    BULLET = 2
    ENEMY_BULLET = 3
    POWERUP = 4
    EXPLOSION = 5

class PowerUpType(Enum):
    HEALTH = 0
    RAPID_FIRE = 1
    TRIPLE_SHOT = 2
    SHIELD = 3

class Entity:
    """Base class for all game entities"""
    def __init__(self, x: float, y: float, width: int, height: int, entity_type: EntityType):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = entity_type
        self.active = True
        self.health = 1
        
    def get_rect(self):
        return (self.x - self.width//2, self.y - self.height//2, self.width, self.height)
    
    def collides_with(self, other: 'Entity') -> bool:
        if not self.active or not other.active:
            return False
        
        # Simple AABB collision
        x1, y1, w1, h1 = self.get_rect()
        x2, y2, w2, h2 = other.get_rect()
        
        return (x1 < x2 + w2 and x1 + w1 > x2 and 
                y1 < y2 + h2 and y1 + h1 > y2)
    
    def update(self, dt: float):
        pass
    
    def draw(self):
        pass

class Player(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, 40, 40, EntityType.PLAYER)
        self.speed = 300
        self.health = 100
        self.max_health = 100
        self.fire_cooldown = 0
        self.fire_rate = 0.2  # Seconds between shots
        self.power_up_timer = 0
        self.current_power_up = None
        self.shield_active = False
        self.triple_shot = False
        self.rapid_fire = False
        
    def update(self, dt: float):
        # Movement
        if pyray.is_key_down(pyray.KEY_LEFT) or pyray.is_key_down(pyray.KEY_A):
            self.x -= self.speed * dt
        if pyray.is_key_down(pyray.KEY_RIGHT) or pyray.is_key_down(pyray.KEY_D):
            self.x += self.speed * dt
        if pyray.is_key_down(pyray.KEY_UP) or pyray.is_key_down(pyray.KEY_W):
            self.y -= self.speed * dt
        if pyray.is_key_down(pyray.KEY_DOWN) or pyray.is_key_down(pyray.KEY_S):
            self.y += self.speed * dt
            
        # Keep player on screen
        self.x = pyray.clamp(self.x, self.width//2, SCREEN_WIDTH - self.width//2)
        self.y = pyray.clamp(self.y, self.height//2, SCREEN_HEIGHT - self.height//2)
        
        # Update fire cooldown
        if self.fire_cooldown > 0:
            self.fire_cooldown -= dt
            
        # Update power-up timer
        if self.power_up_timer > 0:
            self.power_up_timer -= dt
            if self.power_up_timer <= 0:
                self.current_power_up = None
                self.shield_active = False
                self.triple_shot = False
                self.rapid_fire = False
                self.fire_rate = 0.2
                
    def fire(self) -> List['Bullet']:
        if self.fire_cooldown <= 0:
            bullets = []
            
            if self.triple_shot:
                # Triple shot pattern
                bullets.append(Bullet(self.x - 10, self.y - self.height//2, -5, -400))
                bullets.append(Bullet(self.x, self.y - self.height//2, 0, -400))
                bullets.append(Bullet(self.x + 10, self.y - self.height//2, 5, -400))
            else:
                # Single shot
                bullets.append(Bullet(self.x, self.y - self.height//2, 0, -400))
                
            self.fire_cooldown = self.fire_rate
            return bullets
        return []
    
    def apply_power_up(self, power_up_type: PowerUpType):
        self.current_power_up = power_up_type
        self.power_up_timer = 5.0  # 5 seconds duration
        
        if power_up_type == PowerUpType.HEALTH:
            self.health = min(self.max_health, self.health + 30)
        elif power_up_type == PowerUpType.RAPID_FIRE:
            self.rapid_fire = True
            self.fire_rate = 0.1
        elif power_up_type == PowerUpType.TRIPLE_SHOT:
            self.triple_shot = True
        elif power_up_type == PowerUpType.SHIELD:
            self.shield_active = True
            
    def take_damage(self, damage: int):
        if not self.shield_active:
            self.health -= damage
            if self.health <= 0:
                self.active = False
                
    def draw(self):
        if self.active:
            # Draw ship (triangle)
            v1 = pyray.Vector2(self.x, self.y - self.height//2)
            v2 = pyray.Vector2(self.x - self.width//2, self.y + self.height//2)
            v3 = pyray.Vector2(self.x + self.width//2, self.y + self.height//2)
            
            color = pyray.CYAN if not self.shield_active else pyray.BLUE
            pyray.draw_triangle(v1, v2, v3, color)
            
            # Draw shield
            if self.shield_active:
                pyray.draw_circle_lines(int(self.x), int(self.y), self.width, pyray.fade(pyray.SKYBLUE, 0.5))

class Enemy(Entity):
    def __init__(self, x: float, y: float, enemy_type: int = 0):
        super().__init__(x, y, 30, 30, EntityType.ENEMY)
        self.enemy_type = enemy_type
        self.speed = 100 + enemy_type * 50
        self.health = 1 + enemy_type * 2
        self.fire_cooldown = 0
        self.fire_rate = 2.0 - enemy_type * 0.3
        self.movement_pattern = random.choice(['straight', 'sine', 'zigzag'])
        self.time = 0
        self.score_value = 10 + enemy_type * 10
        
    def update(self, dt: float):
        self.time += dt
        
        # Movement patterns
        if self.movement_pattern == 'straight':
            self.y += self.speed * dt
        elif self.movement_pattern == 'sine':
            self.y += self.speed * dt
            self.x += math.sin(self.time * 3) * 100 * dt
        elif self.movement_pattern == 'zigzag':
            self.y += self.speed * dt
            self.x += math.cos(self.time * 5) * 150 * dt
            
        # Keep in bounds horizontally
        self.x = pyray.clamp(self.x, self.width//2, SCREEN_WIDTH - self.width//2)
        
        # Remove if off screen
        if self.y > SCREEN_HEIGHT + self.height:
            self.active = False
            
        # Update fire cooldown
        if self.fire_cooldown > 0:
            self.fire_cooldown -= dt
            
    def fire(self) -> Optional['Bullet']:
        if self.fire_cooldown <= 0 and self.y < SCREEN_HEIGHT - 100:
            self.fire_cooldown = self.fire_rate
            return Bullet(self.x, self.y + self.height//2, 0, 200, is_enemy=True)
        return None
    
    def take_damage(self, damage: int):
        self.health -= damage
        if self.health <= 0:
            self.active = False
            
    def draw(self):
        if self.active:
            color = [pyray.RED, pyray.ORANGE, pyray.PURPLE][self.enemy_type % 3]
            pyray.draw_rectangle(int(self.x - self.width//2), int(self.y - self.height//2),
                                self.width, self.height, color)
            # Draw health bar for tougher enemies
            if self.enemy_type > 0:
                bar_width = self.width
                bar_height = 4
                health_pct = self.health / (1 + self.enemy_type * 2)
                pyray.draw_rectangle(int(self.x - bar_width//2), int(self.y - self.height//2 - 8),
                                    int(bar_width * health_pct), bar_height, pyray.GREEN)

class Bullet(Entity):
    def __init__(self, x: float, y: float, vx: float, vy: float, is_enemy: bool = False):
        super().__init__(x, y, 4, 10, EntityType.ENEMY_BULLET if is_enemy else EntityType.BULLET)
        self.vx = vx
        self.vy = vy
        self.is_enemy = is_enemy
        self.damage = 10
        
    def update(self, dt: float):
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Remove if off screen
        if self.y < -self.height or self.y > SCREEN_HEIGHT + self.height:
            self.active = False
        if self.x < -self.width or self.x > SCREEN_WIDTH + self.width:
            self.active = False
            
    def draw(self):
        if self.active:
            color = pyray.YELLOW if not self.is_enemy else pyray.MAGENTA
            pyray.draw_rectangle(int(self.x - self.width//2), int(self.y - self.height//2),
                                self.width, self.height, color)

class PowerUp(Entity):
    def __init__(self, x: float, y: float, power_type: PowerUpType):
        super().__init__(x, y, 20, 20, EntityType.POWERUP)
        self.power_type = power_type
        self.speed = 50
        self.time = 0
        
    def update(self, dt: float):
        self.time += dt
        self.y += self.speed * dt
        # Wobble effect
        self.x += math.sin(self.time * 5) * 30 * dt
        
        # Remove if off screen
        if self.y > SCREEN_HEIGHT + self.height:
            self.active = False
            
    def draw(self):
        if self.active:
            colors = {
                PowerUpType.HEALTH: pyray.GREEN,
                PowerUpType.RAPID_FIRE: pyray.YELLOW,
                PowerUpType.TRIPLE_SHOT: pyray.ORANGE,
                PowerUpType.SHIELD: pyray.BLUE
            }
            color = colors.get(self.power_type, pyray.WHITE)
            pyray.draw_circle(int(self.x), int(self.y), 10, color)
            # Draw icon
            if self.power_type == PowerUpType.HEALTH:
                pyray.draw_text("+", int(self.x - 5), int(self.y - 8), 16, pyray.WHITE)
            elif self.power_type == PowerUpType.RAPID_FIRE:
                pyray.draw_text("R", int(self.x - 5), int(self.y - 8), 16, pyray.BLACK)
            elif self.power_type == PowerUpType.TRIPLE_SHOT:
                pyray.draw_text("3", int(self.x - 5), int(self.y - 8), 16, pyray.BLACK)
            elif self.power_type == PowerUpType.SHIELD:
                pyray.draw_text("S", int(self.x - 5), int(self.y - 8), 16, pyray.WHITE)

class Explosion:
    def __init__(self, x: float, y: float, size: float = 20):
        self.x = x
        self.y = y
        self.size = size
        self.max_size = size * 3
        self.life = 1.0
        self.active = True
        
    def update(self, dt: float):
        self.life -= dt * 3
        self.size += dt * 100
        if self.life <= 0:
            self.active = False
            
    def draw(self):
        if self.active:
            alpha = max(0, self.life)
            color = pyray.fade(pyray.ORANGE, alpha)
            pyray.draw_circle(int(self.x), int(self.y), self.size, color)
            inner_color = pyray.fade(pyray.YELLOW, alpha * 1.5)
            pyray.draw_circle(int(self.x), int(self.y), self.size * 0.6, inner_color)

class StarField:
    def __init__(self, count: int = 100):
        self.stars = []
        for _ in range(count):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(50, 200),
                'size': random.uniform(1, 3)
            })
            
    def update(self, dt: float):
        for star in self.stars:
            star['y'] += star['speed'] * dt
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = 0
                star['x'] = random.randint(0, SCREEN_WIDTH)
                
    def draw(self):
        for star in self.stars:
            alpha = star['size'] / 3
            color = pyray.fade(pyray.WHITE, alpha)
            pyray.draw_circle(int(star['x']), int(star['y']), star['size'], color)

class SpaceShooterGame:
    def __init__(self):
        self.state = GameState.MENU
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.enemies: List[Enemy] = []
        self.bullets: List[Bullet] = []
        self.power_ups: List[PowerUp] = []
        self.explosions: List[Explosion] = []
        self.starfield = StarField()
        
        self.score = 0
        self.high_score = 0
        self.wave = 1
        self.enemies_spawned = 0
        self.enemies_per_wave = 10
        self.spawn_timer = 0
        self.spawn_delay = 1.0
        
    def reset(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.enemies.clear()
        self.bullets.clear()
        self.power_ups.clear()
        self.explosions.clear()
        self.score = 0
        self.wave = 1
        self.enemies_spawned = 0
        self.spawn_timer = 0
        
    def spawn_enemy(self):
        x = random.randint(30, SCREEN_WIDTH - 30)
        y = -30
        enemy_type = min(2, (self.wave - 1) // 3)  # Harder enemies in later waves
        self.enemies.append(Enemy(x, y, enemy_type))
        self.enemies_spawned += 1
        
    def spawn_power_up(self, x: float, y: float):
        if random.random() < 0.2:  # 20% chance
            power_type = random.choice(list(PowerUpType))
            self.power_ups.append(PowerUp(x, y, power_type))
            
    def update(self, dt: float):
        if self.state == GameState.PLAYING:
            # Update starfield
            self.starfield.update(dt)
            
            # Update player
            self.player.update(dt)
            
            # Player shooting
            if (pyray.is_key_down(pyray.KEY_SPACE) or 
                pyray.is_mouse_button_down(pyray.MOUSE_BUTTON_LEFT)):
                new_bullets = self.player.fire()
                self.bullets.extend(new_bullets)
                
            # Spawn enemies
            if self.enemies_spawned < self.enemies_per_wave * self.wave:
                self.spawn_timer += dt
                if self.spawn_timer >= self.spawn_delay:
                    self.spawn_timer = 0
                    self.spawn_enemy()
                    self.spawn_delay = max(0.3, 1.0 - self.wave * 0.1)
                    
            # Check for wave completion
            if self.enemies_spawned >= self.enemies_per_wave * self.wave and len(self.enemies) == 0:
                self.wave += 1
                self.enemies_spawned = 0
                self.spawn_timer = 0
                
            # Update enemies
            for enemy in self.enemies[:]:
                enemy.update(dt)
                if not enemy.active:
                    self.enemies.remove(enemy)
                    if enemy.health <= 0:  # Destroyed, not just off-screen
                        self.score += enemy.score_value
                        self.explosions.append(Explosion(enemy.x, enemy.y))
                        self.spawn_power_up(enemy.x, enemy.y)
                else:
                    # Enemy shooting
                    bullet = enemy.fire()
                    if bullet:
                        self.bullets.append(bullet)
                        
            # Update bullets
            for bullet in self.bullets[:]:
                bullet.update(dt)
                if not bullet.active:
                    self.bullets.remove(bullet)
                    
            # Update power-ups
            for power_up in self.power_ups[:]:
                power_up.update(dt)
                if not power_up.active:
                    self.power_ups.remove(power_up)
                    
            # Update explosions
            for explosion in self.explosions[:]:
                explosion.update(dt)
                if not explosion.active:
                    self.explosions.remove(explosion)
                    
            # Check collisions
            self.check_collisions()
            
            # Check game over
            if not self.player.active:
                self.state = GameState.GAME_OVER
                if self.score > self.high_score:
                    self.high_score = self.score
                    
            # Pause
            if pyray.is_key_pressed(pyray.KEY_P):
                self.state = GameState.PAUSED
                
        elif self.state == GameState.MENU:
            self.starfield.update(dt)
            if pyray.is_key_pressed(pyray.KEY_ENTER) or pyray.is_key_pressed(pyray.KEY_SPACE):
                self.reset()
                self.state = GameState.PLAYING
                
        elif self.state == GameState.PAUSED:
            if pyray.is_key_pressed(pyray.KEY_P):
                self.state = GameState.PLAYING
                
        elif self.state == GameState.GAME_OVER:
            if pyray.is_key_pressed(pyray.KEY_ENTER) or pyray.is_key_pressed(pyray.KEY_SPACE):
                self.reset()
                self.state = GameState.PLAYING
            elif pyray.is_key_pressed(pyray.KEY_ESCAPE):
                self.state = GameState.MENU
                
    def check_collisions(self):
        # Player bullets vs enemies
        for bullet in self.bullets[:]:
            if not bullet.is_enemy and bullet.active:
                for enemy in self.enemies:
                    if enemy.active and bullet.collides_with(enemy):
                        bullet.active = False
                        enemy.take_damage(1)
                        break
                        
        # Enemy bullets vs player
        for bullet in self.bullets[:]:
            if bullet.is_enemy and bullet.active:
                if bullet.collides_with(self.player):
                    bullet.active = False
                    self.player.take_damage(bullet.damage)
                    self.explosions.append(Explosion(bullet.x, bullet.y, 10))
                    
        # Enemies vs player
        for enemy in self.enemies:
            if enemy.active and enemy.collides_with(self.player):
                enemy.active = False
                self.player.take_damage(20)
                self.explosions.append(Explosion(enemy.x, enemy.y))
                
        # Power-ups vs player
        for power_up in self.power_ups[:]:
            if power_up.active and power_up.collides_with(self.player):
                power_up.active = False
                self.player.apply_power_up(power_up.power_type)
                self.score += 50
                
    def draw(self):
        # Draw starfield
        self.starfield.draw()
        
        if self.state == GameState.PLAYING or self.state == GameState.PAUSED:
            # Draw game entities
            self.player.draw()
            
            for enemy in self.enemies:
                enemy.draw()
                
            for bullet in self.bullets:
                bullet.draw()
                
            for power_up in self.power_ups:
                power_up.draw()
                
            for explosion in self.explosions:
                explosion.draw()
                
            # Draw UI
            pyray.draw_text(f"Score: {self.score}", 10, 10, 20, pyray.WHITE)
            pyray.draw_text(f"Wave: {self.wave}", 10, 35, 18, pyray.LIGHTGRAY)
            pyray.draw_text(f"High Score: {self.high_score}", 10, 60, 16, pyray.YELLOW)
            
            # Draw health bar
            bar_width = 200
            bar_height = 20
            bar_x = SCREEN_WIDTH - bar_width - 10
            bar_y = 10
            health_pct = max(0, self.player.health / self.player.max_health)
            
            pyray.draw_rectangle(bar_x, bar_y, bar_width, bar_height, pyray.DARKGRAY)
            pyray.draw_rectangle(bar_x, bar_y, int(bar_width * health_pct), bar_height, pyray.GREEN)
            pyray.draw_text("Health", bar_x - 60, bar_y + 2, 16, pyray.WHITE)
            
            # Draw power-up indicator
            if self.player.current_power_up:
                power_text = {
                    PowerUpType.RAPID_FIRE: "Rapid Fire",
                    PowerUpType.TRIPLE_SHOT: "Triple Shot",
                    PowerUpType.SHIELD: "Shield"
                }.get(self.player.current_power_up, "")
                if power_text:
                    pyray.draw_text(f"Power: {power_text} ({self.player.power_up_timer:.1f}s)",
                                   SCREEN_WIDTH - 200, 40, 14, pyray.CYAN)
                    
            if self.state == GameState.PAUSED:
                pyray.draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, pyray.fade(pyray.BLACK, 0.5))
                pyray.draw_text("PAUSED", SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 20, 30, pyray.YELLOW)
                pyray.draw_text("Press P to continue", SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 20, 16, pyray.WHITE)
                
        elif self.state == GameState.MENU:
            pyray.draw_text("SPACE SHOOTER", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, 36, pyray.CYAN)
            pyray.draw_text("Press ENTER or SPACE to start", SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2, 18, pyray.WHITE)
            pyray.draw_text("Arrow Keys/WASD: Move", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, 16, pyray.LIGHTGRAY)
            pyray.draw_text("Space/Click: Shoot", SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 + 60, 16, pyray.LIGHTGRAY)
            pyray.draw_text("P: Pause", SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 + 80, 16, pyray.LIGHTGRAY)
            pyray.draw_text(f"High Score: {self.high_score}", SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 120, 20, pyray.YELLOW)
            
        elif self.state == GameState.GAME_OVER:
            pyray.draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, pyray.fade(pyray.BLACK, 0.7))
            pyray.draw_text("GAME OVER", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 36, pyray.RED)
            pyray.draw_text(f"Final Score: {self.score}", SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, 24, pyray.WHITE)
            pyray.draw_text(f"Waves Survived: {self.wave}", SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 30, 20, pyray.LIGHTGRAY)
            pyray.draw_text("Press ENTER to play again", SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 70, 18, pyray.LIGHTGRAY)
            pyray.draw_text("Press ESC for menu", SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 95, 18, pyray.LIGHTGRAY)

# Initialize PyRay
pyray.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "PyRay Space Shooter")
pyray.set_target_fps(60)

# Create game
game = SpaceShooterGame()

# Main loop
while not pyray.window_should_close():
    dt = pyray.get_frame_time()
    
    # Update
    game.update(dt)
    
    # Draw
    pyray.begin_drawing()
    pyray.clear_background(pyray.Color(10, 10, 20))
    
    game.draw()
    
    # Show FPS
    fps = pyray.get_fps()
    pyray.draw_text(f"FPS: {fps}", SCREEN_WIDTH - 80, SCREEN_HEIGHT - 20, 14, pyray.GREEN)
    
    pyray.end_drawing()

# Cleanup
pyray.close_window()
