"""
PyRay + Matplotlib Integration Example
Live charts and data visualization in games
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pyray
from pyray.bridges.matplotlib import (
    create_fps_chart,
    create_performance_chart,
    live_chart_overlay,
    figure_to_texture
)
import random
import math

# Window settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Initialize PyRay
pyray.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "PyRay + Matplotlib: Live Charts")
pyray.set_target_fps(60)

# Create charts
fps_chart = create_fps_chart(history_size=120)
perf_chart = create_performance_chart()

# Custom chart for game data
game_data = []
enemy_counts = []
score_history = []
time_counter = 0

def update_game_chart(fig, ax):
    """Update custom game statistics chart"""
    ax.plot(enemy_counts[-60:], 'r-', label='Enemies', linewidth=2)
    ax.plot([s/100 for s in score_history[-60:]], 'g-', label='Score/100', linewidth=2)
    ax.set_ylim(0, 20)
    ax.set_xlim(0, 60)
    ax.set_title("Game Stats", fontsize=10)
    ax.set_ylabel("Count", fontsize=8)
    ax.legend(loc='upper right', fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#00000000')

game_chart = live_chart_overlay(update_game_chart, 300, 200)

# Particle system for visual interest
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = 1.0
        self.color = pyray.Color(
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
    
    def update(self, dt):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # Gravity
        self.life -= dt * 0.5
        
    def draw(self):
        if self.life > 0:
            alpha = int(255 * self.life)
            color = pyray.fade(self.color, self.life)
            pyray.draw_circle(int(self.x), int(self.y), 3, color)

particles = []
enemies = []
score = 0
show_charts = True

# Enemy class
class Enemy:
    def __init__(self):
        self.x = random.randint(50, SCREEN_WIDTH - 50)
        self.y = random.randint(50, SCREEN_HEIGHT - 200)
        self.radius = random.randint(10, 30)
        self.color = pyray.Color(255, random.randint(0, 100), 0)
        self.speed = random.uniform(0.5, 2.0)
        self.direction = random.uniform(0, math.pi * 2)
        
    def update(self):
        self.x += math.cos(self.direction) * self.speed
        self.y += math.sin(self.direction) * self.speed
        
        # Bounce off walls
        if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
            self.direction = math.pi - self.direction
        if self.y <= self.radius or self.y >= SCREEN_HEIGHT - 200 - self.radius:
            self.direction = -self.direction
            
        # Keep in bounds
        self.x = pyray.clamp(self.x, self.radius, SCREEN_WIDTH - self.radius)
        self.y = pyray.clamp(self.y, self.radius, SCREEN_HEIGHT - 200 - self.radius)
        
    def draw(self):
        pyray.draw_circle(int(self.x), int(self.y), self.radius, self.color)

# Spawn initial enemies
for _ in range(5):
    enemies.append(Enemy())

# Main loop
while not pyray.window_should_close():
    # Update
    dt = pyray.get_frame_time()
    time_counter += dt
    
    # Toggle charts
    if pyray.is_key_pressed(pyray.KEY_SPACE):
        show_charts = not show_charts
    
    # Spawn enemies with E
    if pyray.is_key_pressed(pyray.KEY_E):
        enemies.append(Enemy())
        
    # Clear enemies with C
    if pyray.is_key_pressed(pyray.KEY_C):
        score += len(enemies) * 10
        enemies.clear()
    
    # Update enemies
    for enemy in enemies:
        enemy.update()
    
    # Click to destroy enemies and create particles
    if pyray.is_mouse_button_pressed(pyray.MOUSE_BUTTON_LEFT):
        mouse_x = pyray.get_mouse_x()
        mouse_y = pyray.get_mouse_y()
        
        # Check collision with enemies
        enemies_to_remove = []
        for enemy in enemies:
            dist = math.sqrt((enemy.x - mouse_x)**2 + (enemy.y - mouse_y)**2)
            if dist <= enemy.radius:
                enemies_to_remove.append(enemy)
                score += enemy.radius
                # Create explosion particles
                for _ in range(10):
                    particles.append(Particle(enemy.x, enemy.y))
        
        for enemy in enemies_to_remove:
            enemies.remove(enemy)
    
    # Update particles
    particles_to_remove = []
    for particle in particles:
        particle.update(dt)
        if particle.life <= 0:
            particles_to_remove.append(particle)
    
    for particle in particles_to_remove:
        particles.remove(particle)
    
    # Update game data for charts
    enemy_counts.append(len(enemies))
    score_history.append(score)
    if len(enemy_counts) > 120:
        enemy_counts.pop(0)
    if len(score_history) > 120:
        score_history.pop(0)
    
    # Update chart textures
    if show_charts:
        fps_texture = fps_chart.update()
        perf_texture = perf_chart.update()
        game_texture = game_chart.update()
    
    # Draw
    pyray.begin_drawing()
    pyray.clear_background(pyray.Color(20, 20, 30))
    
    # Draw game area background
    pyray.draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - 200, pyray.Color(30, 30, 40))
    
    # Draw enemies
    for enemy in enemies:
        enemy.draw()
    
    # Draw particles
    for particle in particles:
        particle.draw()
    
    # Draw UI background
    pyray.draw_rectangle(0, SCREEN_HEIGHT - 200, SCREEN_WIDTH, 200, pyray.Color(40, 40, 50))
    
    # Draw charts if enabled
    if show_charts:
        # FPS chart (top-right)
        pyray.draw_texture(fps_texture, SCREEN_WIDTH - 210, 10, pyray.WHITE)
        
        # Performance chart (middle-right)
        pyray.draw_texture(perf_texture, SCREEN_WIDTH - 260, 170, pyray.WHITE)
        
        # Game stats chart (bottom)
        pyray.draw_texture(game_texture, 10, SCREEN_HEIGHT - 190, pyray.WHITE)
    
    # Draw text UI
    pyray.draw_text("Matplotlib Live Charts Demo", 10, 10, 24, pyray.WHITE)
    pyray.draw_text(f"Score: {score}", 10, 40, 20, pyray.YELLOW)
    pyray.draw_text(f"Enemies: {len(enemies)}", 10, 65, 18, pyray.LIGHTGRAY)
    pyray.draw_text(f"Particles: {len(particles)}", 10, 85, 18, pyray.LIGHTGRAY)
    
    # Draw controls
    control_y = SCREEN_HEIGHT - 190
    pyray.draw_text("Controls:", 350, control_y + 10, 16, pyray.WHITE)
    pyray.draw_text("Click: Destroy enemies", 350, control_y + 30, 14, pyray.LIGHTGRAY)
    pyray.draw_text("E: Spawn enemy", 350, control_y + 50, 14, pyray.LIGHTGRAY)
    pyray.draw_text("C: Clear all enemies", 350, control_y + 70, 14, pyray.LIGHTGRAY)
    pyray.draw_text("Space: Toggle charts", 350, control_y + 90, 14, pyray.LIGHTGRAY)
    pyray.draw_text("ESC: Exit", 350, control_y + 110, 14, pyray.LIGHTGRAY)
    
    if not show_charts:
        pyray.draw_text("Charts Hidden (Press Space)", SCREEN_WIDTH - 250, 10, 16, pyray.YELLOW)
    
    pyray.end_drawing()

# Cleanup
fps_chart.close()
perf_chart.close()
game_chart.close()
pyray.close_window()
