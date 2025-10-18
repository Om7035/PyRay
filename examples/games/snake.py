"""
Snake Game - PyRay Implementation
Classic snake game with modern graphics
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pyray
import random
from enum import Enum

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    PAUSED = 3

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        # Start in the center
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        self.segments = [
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y)
        ]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.grow_count = 0
        
    def update(self):
        # Update direction
        self.direction = self.next_direction
        
        # Calculate new head position
        head = self.segments[0]
        dx, dy = self.direction.value
        new_head = (head[0] + dx, head[1] + dy)
        
        # Insert new head
        self.segments.insert(0, new_head)
        
        # Remove tail if not growing
        if self.grow_count > 0:
            self.grow_count -= 1
        else:
            self.segments.pop()
            
    def grow(self, amount=1):
        self.grow_count += amount
        
    def set_direction(self, new_direction):
        # Prevent going back into itself
        dx1, dy1 = self.direction.value
        dx2, dy2 = new_direction.value
        if dx1 + dx2 != 0 or dy1 + dy2 != 0:
            self.next_direction = new_direction
            
    def check_self_collision(self):
        head = self.segments[0]
        return head in self.segments[1:]
        
    def check_wall_collision(self):
        head = self.segments[0]
        return head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn()
        
    def spawn(self, avoid_positions=None):
        """Spawn food at a random position, avoiding given positions"""
        if avoid_positions is None:
            avoid_positions = []
            
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in avoid_positions:
                self.position = (x, y)
                break

class SnakeGame:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.state = GameState.MENU
        self.score = 0
        self.high_score = 0
        self.move_timer = 0
        self.move_delay = 0.1  # Seconds between moves
        self.particles = []
        
    def reset(self):
        self.snake.reset()
        self.food.spawn(self.snake.segments)
        self.score = 0
        self.move_timer = 0
        self.particles = []
        
    def update(self, dt):
        if self.state == GameState.PLAYING:
            # Handle input
            if pyray.is_key_pressed(pyray.KEY_UP) or pyray.is_key_pressed(pyray.KEY_W):
                self.snake.set_direction(Direction.UP)
            elif pyray.is_key_pressed(pyray.KEY_DOWN) or pyray.is_key_pressed(pyray.KEY_S):
                self.snake.set_direction(Direction.DOWN)
            elif pyray.is_key_pressed(pyray.KEY_LEFT) or pyray.is_key_pressed(pyray.KEY_A):
                self.snake.set_direction(Direction.LEFT)
            elif pyray.is_key_pressed(pyray.KEY_RIGHT) or pyray.is_key_pressed(pyray.KEY_D):
                self.snake.set_direction(Direction.RIGHT)
                
            # Pause
            if pyray.is_key_pressed(pyray.KEY_P) or pyray.is_key_pressed(pyray.KEY_SPACE):
                self.state = GameState.PAUSED
                
            # Update snake movement
            self.move_timer += dt
            if self.move_timer >= self.move_delay:
                self.move_timer = 0
                self.snake.update()
                
                # Check food collision
                if self.snake.segments[0] == self.food.position:
                    self.score += 10
                    self.snake.grow(3)
                    self.food.spawn(self.snake.segments)
                    # Create particles at food position
                    for _ in range(10):
                        self.particles.append(FoodParticle(
                            self.food.position[0] * GRID_SIZE + GRID_SIZE // 2,
                            self.food.position[1] * GRID_SIZE + GRID_SIZE // 2
                        ))
                    # Speed up slightly
                    self.move_delay = max(0.05, self.move_delay - 0.002)
                    
                # Check collisions
                if self.snake.check_self_collision() or self.snake.check_wall_collision():
                    self.state = GameState.GAME_OVER
                    if self.score > self.high_score:
                        self.high_score = self.score
                        
        elif self.state == GameState.MENU:
            if pyray.is_key_pressed(pyray.KEY_ENTER) or pyray.is_key_pressed(pyray.KEY_SPACE):
                self.reset()
                self.state = GameState.PLAYING
                
        elif self.state == GameState.PAUSED:
            if pyray.is_key_pressed(pyray.KEY_P) or pyray.is_key_pressed(pyray.KEY_SPACE):
                self.state = GameState.PLAYING
                
        elif self.state == GameState.GAME_OVER:
            if pyray.is_key_pressed(pyray.KEY_ENTER) or pyray.is_key_pressed(pyray.KEY_SPACE):
                self.reset()
                self.state = GameState.PLAYING
            elif pyray.is_key_pressed(pyray.KEY_ESCAPE):
                self.state = GameState.MENU
                
        # Update particles
        self.particles = [p for p in self.particles if p.update(dt)]
                
    def draw(self):
        # Draw grid background
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pyray.draw_line(x, 0, x, SCREEN_HEIGHT, pyray.Color(40, 40, 40))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pyray.draw_line(0, y, SCREEN_WIDTH, y, pyray.Color(40, 40, 40))
            
        if self.state == GameState.PLAYING or self.state == GameState.PAUSED:
            # Draw snake
            for i, segment in enumerate(self.snake.segments):
                x = segment[0] * GRID_SIZE
                y = segment[1] * GRID_SIZE
                
                if i == 0:  # Head
                    pyray.draw_rectangle(x + 2, y + 2, GRID_SIZE - 4, GRID_SIZE - 4, pyray.GREEN)
                    # Draw eyes
                    eye_size = 3
                    if self.snake.direction == Direction.RIGHT:
                        pyray.draw_circle(x + GRID_SIZE - 6, y + 6, eye_size, pyray.WHITE)
                        pyray.draw_circle(x + GRID_SIZE - 6, y + GRID_SIZE - 6, eye_size, pyray.WHITE)
                    elif self.snake.direction == Direction.LEFT:
                        pyray.draw_circle(x + 6, y + 6, eye_size, pyray.WHITE)
                        pyray.draw_circle(x + 6, y + GRID_SIZE - 6, eye_size, pyray.WHITE)
                    elif self.snake.direction == Direction.UP:
                        pyray.draw_circle(x + 6, y + 6, eye_size, pyray.WHITE)
                        pyray.draw_circle(x + GRID_SIZE - 6, y + 6, eye_size, pyray.WHITE)
                    else:  # DOWN
                        pyray.draw_circle(x + 6, y + GRID_SIZE - 6, eye_size, pyray.WHITE)
                        pyray.draw_circle(x + GRID_SIZE - 6, y + GRID_SIZE - 6, eye_size, pyray.WHITE)
                else:  # Body
                    color = pyray.fade(pyray.DARKGREEN, 0.8 - (i / len(self.snake.segments)) * 0.3)
                    pyray.draw_rectangle(x + 3, y + 3, GRID_SIZE - 6, GRID_SIZE - 6, color)
                    
            # Draw food
            fx = self.food.position[0] * GRID_SIZE
            fy = self.food.position[1] * GRID_SIZE
            pyray.draw_circle(fx + GRID_SIZE // 2, fy + GRID_SIZE // 2, GRID_SIZE // 2 - 2, pyray.RED)
            
            # Draw particles
            for particle in self.particles:
                particle.draw()
                
            # Draw score
            pyray.draw_text(f"Score: {self.score}", 10, 10, 24, pyray.WHITE)
            pyray.draw_text(f"High Score: {self.high_score}", 10, 40, 18, pyray.LIGHTGRAY)
            
            if self.state == GameState.PAUSED:
                pyray.draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, pyray.fade(pyray.BLACK, 0.5))
                pyray.draw_text("PAUSED", SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 20, 30, pyray.YELLOW)
                pyray.draw_text("Press P or Space to continue", SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20, 16, pyray.WHITE)
                
        elif self.state == GameState.MENU:
            pyray.draw_text("SNAKE", SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 100, 48, pyray.GREEN)
            pyray.draw_text("Press ENTER or SPACE to start", SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2, 18, pyray.WHITE)
            pyray.draw_text("Use Arrow Keys or WASD to move", SCREEN_WIDTH // 2 - 145, SCREEN_HEIGHT // 2 + 40, 16, pyray.LIGHTGRAY)
            pyray.draw_text("P or Space to pause", SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 60, 16, pyray.LIGHTGRAY)
            pyray.draw_text(f"High Score: {self.high_score}", SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 100, 20, pyray.YELLOW)
            
        elif self.state == GameState.GAME_OVER:
            pyray.draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, pyray.fade(pyray.BLACK, 0.7))
            pyray.draw_text("GAME OVER", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 36, pyray.RED)
            pyray.draw_text(f"Final Score: {self.score}", SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, 24, pyray.WHITE)
            pyray.draw_text("Press ENTER to play again", SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 40, 18, pyray.LIGHTGRAY)
            pyray.draw_text("Press ESC for menu", SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 65, 18, pyray.LIGHTGRAY)

class FoodParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-100, 100)
        self.vy = random.uniform(-100, 100)
        self.life = 1.0
        self.color = pyray.Color(
            random.randint(200, 255),
            random.randint(0, 100),
            0
        )
        
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt * 2
        return self.life > 0
        
    def draw(self):
        if self.life > 0:
            color = pyray.fade(self.color, self.life)
            pyray.draw_circle(int(self.x), int(self.y), 3, color)

# Initialize PyRay
pyray.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "PyRay Snake Game")
pyray.set_target_fps(60)

# Create game
game = SnakeGame()

# Main loop
while not pyray.window_should_close():
    dt = pyray.get_frame_time()
    
    # Update
    game.update(dt)
    
    # Draw
    pyray.begin_drawing()
    pyray.clear_background(pyray.Color(20, 20, 30))
    
    game.draw()
    
    # Show FPS
    fps = pyray.get_fps()
    pyray.draw_text(f"FPS: {fps}", SCREEN_WIDTH - 80, 10, 14, pyray.GREEN)
    
    pyray.end_drawing()

# Cleanup
pyray.close_window()
