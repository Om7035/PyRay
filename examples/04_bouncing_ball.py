"""
PyRay Example - Bouncing Ball
A simple bouncing ball animation with physics
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pyray
import random

# Window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize window
pyray.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "PyRay - Bouncing Ball")

# Set target FPS
pyray.set_target_fps(60)

# Ball class
class Ball:
    def __init__(self, x, y, radius, color):
        self.position = pyray.Vector2(x, y)
        self.velocity = pyray.Vector2(
            pyray.random_float(-5, 5),
            pyray.random_float(-5, 5)
        )
        self.radius = radius
        self.color = color
        self.gravity = 0.5
        self.damping = 0.98
        self.trail = []
        self.max_trail_length = 20
    
    def update(self):
        # Add gravity
        self.velocity.y += self.gravity
        
        # Apply damping
        self.velocity.x *= self.damping
        self.velocity.y *= self.damping
        
        # Update position
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        
        # Add to trail
        self.trail.append(pyray.Vector2(self.position.x, self.position.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        
        # Bounce off walls
        if self.position.x - self.radius <= 0 or self.position.x + self.radius >= SCREEN_WIDTH:
            self.velocity.x *= -0.9
            self.position.x = pyray.clamp(self.position.x, self.radius, SCREEN_WIDTH - self.radius)
        
        if self.position.y - self.radius <= 0 or self.position.y + self.radius >= SCREEN_HEIGHT:
            self.velocity.y *= -0.9
            self.position.y = pyray.clamp(self.position.y, self.radius, SCREEN_HEIGHT - self.radius)
            
            # Add some randomness when bouncing
            if abs(self.velocity.y) < 1:
                self.velocity.x += pyray.random_float(-2, 2)
    
    def draw(self):
        # Draw trail
        for i, pos in enumerate(self.trail):
            alpha = i / len(self.trail) if self.trail else 1
            faded_color = pyray.fade(self.color, alpha * 0.3)
            trail_radius = self.radius * (i / len(self.trail)) if self.trail else self.radius
            pyray.draw_circle(int(pos.x), int(pos.y), trail_radius, faded_color)
        
        # Draw ball
        pyray.draw_circle(int(self.position.x), int(self.position.y), self.radius, self.color)
        
        # Draw highlight
        highlight_x = int(self.position.x - self.radius * 0.3)
        highlight_y = int(self.position.y - self.radius * 0.3)
        highlight_radius = self.radius * 0.3
        pyray.draw_circle(highlight_x, highlight_y, highlight_radius, pyray.fade(pyray.WHITE, 0.5))

# Create balls
balls = []
colors = [pyray.RED, pyray.GREEN, pyray.BLUE, pyray.YELLOW, pyray.PURPLE, pyray.ORANGE, pyray.PINK]

# Create initial balls
for _ in range(5):
    ball = Ball(
        pyray.random_int(50, SCREEN_WIDTH - 50),
        pyray.random_int(50, SCREEN_HEIGHT // 2),
        pyray.random_int(15, 30),
        random.choice(colors)
    )
    balls.append(ball)

# Main game loop
while not pyray.window_should_close():
    # Update
    for ball in balls:
        ball.update()
    
    # Add new ball on mouse click
    if pyray.is_mouse_button_pressed(pyray.MOUSE_BUTTON_LEFT):
        mouse_x = pyray.get_mouse_x()
        mouse_y = pyray.get_mouse_y()
        new_ball = Ball(mouse_x, mouse_y, pyray.random_int(15, 30), random.choice(colors))
        balls.append(new_ball)
    
    # Remove balls with right click
    if pyray.is_mouse_button_pressed(pyray.MOUSE_BUTTON_RIGHT) and balls:
        balls.pop()
    
    # Clear all balls with C
    if pyray.is_key_pressed(pyray.KEY_C):
        balls.clear()
    
    # Draw
    pyray.begin_drawing()
    
    # Clear background
    pyray.clear_background(pyray.BLACK)
    
    # Draw grid
    for x in range(0, SCREEN_WIDTH, 50):
        pyray.draw_line(x, 0, x, SCREEN_HEIGHT, pyray.fade(pyray.DARKGRAY, 0.3))
    for y in range(0, SCREEN_HEIGHT, 50):
        pyray.draw_line(0, y, SCREEN_WIDTH, y, pyray.fade(pyray.DARKGRAY, 0.3))
    
    # Draw balls
    for ball in balls:
        ball.draw()
    
    # Draw UI
    pyray.draw_text("Bouncing Balls Physics Demo", 10, 10, 20, pyray.WHITE)
    pyray.draw_text(f"Balls: {len(balls)}", 10, 35, 16, pyray.LIGHTGRAY)
    pyray.draw_text("Left Click: Add ball | Right Click: Remove ball | C: Clear all", 10, SCREEN_HEIGHT - 25, 14, pyray.GRAY)
    
    # Show FPS
    fps = pyray.get_fps()
    pyray.draw_text(f"FPS: {fps}", SCREEN_WIDTH - 80, 10, 16, pyray.GREEN)
    
    pyray.end_drawing()

# Cleanup
pyray.close_window()
