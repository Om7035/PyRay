"""
Tetris Game - PyRay Implementation
Classic Tetris with modern effects
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
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
CELL_SIZE = 25
BOARD_X = (SCREEN_WIDTH - BOARD_WIDTH * CELL_SIZE) // 2
BOARD_Y = 50

# Tetromino shapes
SHAPES = [
    # I
    [[1, 1, 1, 1]],
    # O
    [[1, 1],
     [1, 1]],
    # T
    [[0, 1, 0],
     [1, 1, 1]],
    # S
    [[0, 1, 1],
     [1, 1, 0]],
    # Z
    [[1, 1, 0],
     [0, 1, 1]],
    # J
    [[1, 0, 0],
     [1, 1, 1]],
    # L
    [[0, 0, 1],
     [1, 1, 1]]
]

# Colors for each shape
SHAPE_COLORS = [
    pyray.CYAN,     # I
    pyray.YELLOW,   # O
    pyray.PURPLE,   # T
    pyray.GREEN,    # S
    pyray.RED,      # Z
    pyray.BLUE,     # J
    pyray.ORANGE    # L
]

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    PAUSED = 3

class Tetromino:
    def __init__(self, shape_index):
        self.shape_index = shape_index
        self.shape = [row[:] for row in SHAPES[shape_index]]
        self.color = SHAPE_COLORS[shape_index]
        self.x = BOARD_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        
    def rotate(self):
        """Rotate the shape 90 degrees clockwise"""
        rotated = [[self.shape[j][i] for j in range(len(self.shape)-1, -1, -1)]
                   for i in range(len(self.shape[0]))]
        return rotated
        
    def get_blocks(self):
        """Get the positions of all blocks in the tetromino"""
        blocks = []
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    blocks.append((self.x + x, self.y + y))
        return blocks

class TetrisGame:
    def __init__(self):
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_piece = None
        self.next_piece_index = random.randint(0, len(SHAPES) - 1)
        self.state = GameState.MENU
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.high_score = 0
        self.drop_timer = 0
        self.drop_speed = 1.0  # Seconds between drops
        self.particles = []
        self.line_clear_animation = []
        
    def reset(self):
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.spawn_piece()
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.drop_timer = 0
        self.drop_speed = 1.0
        self.particles = []
        self.line_clear_animation = []
        
    def spawn_piece(self):
        self.current_piece = Tetromino(self.next_piece_index)
        self.next_piece_index = random.randint(0, len(SHAPES) - 1)
        
        # Check if spawn position is blocked (game over)
        if self.check_collision():
            self.state = GameState.GAME_OVER
            if self.score > self.high_score:
                self.high_score = self.score
                
    def check_collision(self, dx=0, dy=0, rotated_shape=None):
        """Check if the current piece would collide at the given offset"""
        shape = rotated_shape if rotated_shape else self.current_piece.shape
        
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.current_piece.x + x + dx
                    new_y = self.current_piece.y + y + dy
                    
                    # Check boundaries
                    if new_x < 0 or new_x >= BOARD_WIDTH or new_y >= BOARD_HEIGHT:
                        return True
                        
                    # Check board collision
                    if new_y >= 0 and self.board[new_y][new_x]:
                        return True
                        
        return False
        
    def lock_piece(self):
        """Lock the current piece to the board"""
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    board_x = self.current_piece.x + x
                    board_y = self.current_piece.y + y
                    if board_y >= 0:
                        self.board[board_y][board_x] = self.current_piece.shape_index + 1
                        
        # Check for completed lines
        self.check_lines()
        
        # Spawn new piece
        self.spawn_piece()
        
    def check_lines(self):
        """Check for and clear completed lines"""
        lines_to_clear = []
        
        for y in range(BOARD_HEIGHT):
            if all(self.board[y]):
                lines_to_clear.append(y)
                
        if lines_to_clear:
            # Add to animation list
            self.line_clear_animation = lines_to_clear[:]
            
            # Create particles for cleared lines
            for y in lines_to_clear:
                for x in range(BOARD_WIDTH):
                    px = BOARD_X + x * CELL_SIZE + CELL_SIZE // 2
                    py = BOARD_Y + y * CELL_SIZE + CELL_SIZE // 2
                    for _ in range(3):
                        self.particles.append(LineParticle(px, py))
                        
            # Clear lines
            for y in lines_to_clear:
                del self.board[y]
                self.board.insert(0, [0 for _ in range(BOARD_WIDTH)])
                
            # Update score
            lines = len(lines_to_clear)
            self.lines_cleared += lines
            self.score += [0, 100, 300, 500, 800][lines] * self.level
            
            # Update level
            self.level = min(10, self.lines_cleared // 10 + 1)
            self.drop_speed = max(0.1, 1.0 - (self.level - 1) * 0.1)
            
    def move(self, dx):
        """Move the current piece horizontally"""
        if not self.check_collision(dx=dx):
            self.current_piece.x += dx
            
    def rotate(self):
        """Rotate the current piece"""
        rotated = self.current_piece.rotate()
        
        # Try to rotate
        if not self.check_collision(rotated_shape=rotated):
            self.current_piece.shape = rotated
        # Wall kick - try moving left or right
        elif not self.check_collision(dx=-1, rotated_shape=rotated):
            self.current_piece.x -= 1
            self.current_piece.shape = rotated
        elif not self.check_collision(dx=1, rotated_shape=rotated):
            self.current_piece.x += 1
            self.current_piece.shape = rotated
            
    def drop(self):
        """Drop the current piece one row"""
        if not self.check_collision(dy=1):
            self.current_piece.y += 1
            return True
        else:
            self.lock_piece()
            return False
            
    def hard_drop(self):
        """Drop the piece all the way down"""
        drops = 0
        while not self.check_collision(dy=1):
            self.current_piece.y += 1
            drops += 1
        self.score += drops * 2
        self.lock_piece()
        
    def update(self, dt):
        if self.state == GameState.PLAYING:
            # Handle input
            if pyray.is_key_pressed(pyray.KEY_LEFT) or pyray.is_key_pressed(pyray.KEY_A):
                self.move(-1)
            if pyray.is_key_pressed(pyray.KEY_RIGHT) or pyray.is_key_pressed(pyray.KEY_D):
                self.move(1)
            if pyray.is_key_pressed(pyray.KEY_UP) or pyray.is_key_pressed(pyray.KEY_W):
                self.rotate()
            if pyray.is_key_down(pyray.KEY_DOWN) or pyray.is_key_down(pyray.KEY_S):
                if self.drop():
                    self.score += 1
                    self.drop_timer = 0
            if pyray.is_key_pressed(pyray.KEY_SPACE):
                self.hard_drop()
            if pyray.is_key_pressed(pyray.KEY_P):
                self.state = GameState.PAUSED
                
            # Auto drop
            self.drop_timer += dt
            if self.drop_timer >= self.drop_speed:
                self.drop_timer = 0
                self.drop()
                
        elif self.state == GameState.MENU:
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
                
        # Update particles
        self.particles = [p for p in self.particles if p.update(dt)]
        
        # Clear line animation
        if self.line_clear_animation:
            self.line_clear_animation = []
            
    def draw(self):
        # Draw board background
        pyray.draw_rectangle(BOARD_X - 2, BOARD_Y - 2, 
                            BOARD_WIDTH * CELL_SIZE + 4, 
                            BOARD_HEIGHT * CELL_SIZE + 4, 
                            pyray.DARKGRAY)
        pyray.draw_rectangle(BOARD_X, BOARD_Y, 
                            BOARD_WIDTH * CELL_SIZE, 
                            BOARD_HEIGHT * CELL_SIZE, 
                            pyray.Color(30, 30, 40))
                            
        # Draw grid
        for x in range(BOARD_WIDTH + 1):
            pyray.draw_line(BOARD_X + x * CELL_SIZE, BOARD_Y,
                          BOARD_X + x * CELL_SIZE, BOARD_Y + BOARD_HEIGHT * CELL_SIZE,
                          pyray.Color(50, 50, 60))
        for y in range(BOARD_HEIGHT + 1):
            pyray.draw_line(BOARD_X, BOARD_Y + y * CELL_SIZE,
                          BOARD_X + BOARD_WIDTH * CELL_SIZE, BOARD_Y + y * CELL_SIZE,
                          pyray.Color(50, 50, 60))
                          
        if self.state == GameState.PLAYING or self.state == GameState.PAUSED:
            # Draw board pieces
            for y, row in enumerate(self.board):
                for x, cell in enumerate(row):
                    if cell:
                        color = SHAPE_COLORS[cell - 1]
                        px = BOARD_X + x * CELL_SIZE
                        py = BOARD_Y + y * CELL_SIZE
                        pyray.draw_rectangle(px + 1, py + 1, CELL_SIZE - 2, CELL_SIZE - 2, color)
                        
            # Draw ghost piece (preview where it will land)
            if self.current_piece:
                ghost_y = self.current_piece.y
                while not self.check_collision(dy=ghost_y - self.current_piece.y + 1):
                    ghost_y += 1
                    
                for y, row in enumerate(self.current_piece.shape):
                    for x, cell in enumerate(row):
                        if cell:
                            px = BOARD_X + (self.current_piece.x + x) * CELL_SIZE
                            py = BOARD_Y + (ghost_y + y) * CELL_SIZE
                            ghost_color = pyray.fade(self.current_piece.color, 0.3)
                            pyray.draw_rectangle(px + 1, py + 1, CELL_SIZE - 2, CELL_SIZE - 2, ghost_color)
                            
            # Draw current piece
            if self.current_piece:
                for y, row in enumerate(self.current_piece.shape):
                    for x, cell in enumerate(row):
                        if cell:
                            px = BOARD_X + (self.current_piece.x + x) * CELL_SIZE
                            py = BOARD_Y + (self.current_piece.y + y) * CELL_SIZE
                            pyray.draw_rectangle(px + 1, py + 1, CELL_SIZE - 2, CELL_SIZE - 2, 
                                               self.current_piece.color)
                                               
            # Draw next piece preview
            next_x = BOARD_X + BOARD_WIDTH * CELL_SIZE + 50
            next_y = BOARD_Y + 50
            pyray.draw_text("NEXT", next_x, next_y - 30, 20, pyray.WHITE)
            pyray.draw_rectangle(next_x - 10, next_y - 10, 100, 100, pyray.Color(40, 40, 50))
            
            next_shape = SHAPES[self.next_piece_index]
            next_color = SHAPE_COLORS[self.next_piece_index]
            for y, row in enumerate(next_shape):
                for x, cell in enumerate(row):
                    if cell:
                        px = next_x + x * 20
                        py = next_y + y * 20
                        pyray.draw_rectangle(px, py, 18, 18, next_color)
                        
            # Draw particles
            for particle in self.particles:
                particle.draw()
                
            # Draw UI
            ui_x = 50
            pyray.draw_text("TETRIS", ui_x, 50, 36, pyray.WHITE)
            pyray.draw_text(f"Score: {self.score}", ui_x, 100, 20, pyray.YELLOW)
            pyray.draw_text(f"Lines: {self.lines_cleared}", ui_x, 130, 18, pyray.LIGHTGRAY)
            pyray.draw_text(f"Level: {self.level}", ui_x, 155, 18, pyray.LIGHTGRAY)
            pyray.draw_text(f"High Score: {self.high_score}", ui_x, 185, 16, pyray.GREEN)
            
            # Draw controls
            control_y = 250
            pyray.draw_text("Controls:", ui_x, control_y, 16, pyray.WHITE)
            pyray.draw_text("← → Move", ui_x, control_y + 25, 14, pyray.LIGHTGRAY)
            pyray.draw_text("↑ Rotate", ui_x, control_y + 45, 14, pyray.LIGHTGRAY)
            pyray.draw_text("↓ Soft Drop", ui_x, control_y + 65, 14, pyray.LIGHTGRAY)
            pyray.draw_text("Space: Hard Drop", ui_x, control_y + 85, 14, pyray.LIGHTGRAY)
            pyray.draw_text("P: Pause", ui_x, control_y + 105, 14, pyray.LIGHTGRAY)
            
            if self.state == GameState.PAUSED:
                pyray.draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, pyray.fade(pyray.BLACK, 0.5))
                pyray.draw_text("PAUSED", SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 20, 30, pyray.YELLOW)
                pyray.draw_text("Press P to continue", SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 20, 16, pyray.WHITE)
                
        elif self.state == GameState.MENU:
            pyray.draw_text("TETRIS", SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 100, 48, pyray.CYAN)
            pyray.draw_text("Press ENTER or SPACE to start", SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2, 18, pyray.WHITE)
            pyray.draw_text("Use Arrow Keys to play", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, 16, pyray.LIGHTGRAY)
            pyray.draw_text(f"High Score: {self.high_score}", SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 80, 20, pyray.YELLOW)
            
        elif self.state == GameState.GAME_OVER:
            pyray.draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, pyray.fade(pyray.BLACK, 0.7))
            pyray.draw_text("GAME OVER", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 36, pyray.RED)
            pyray.draw_text(f"Final Score: {self.score}", SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, 24, pyray.WHITE)
            pyray.draw_text("Press ENTER to play again", SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 40, 18, pyray.LIGHTGRAY)
            pyray.draw_text("Press ESC for menu", SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 65, 18, pyray.LIGHTGRAY)

class LineParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-150, 150)
        self.vy = random.uniform(-200, -50)
        self.life = 1.0
        self.color = pyray.Color(
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
        
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 300 * dt  # Gravity
        self.life -= dt * 1.5
        return self.life > 0
        
    def draw(self):
        if self.life > 0:
            color = pyray.fade(self.color, self.life)
            size = int(4 * self.life)
            pyray.draw_rectangle(int(self.x) - size//2, int(self.y) - size//2, size, size, color)

# Initialize PyRay
pyray.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "PyRay Tetris")
pyray.set_target_fps(60)

# Create game
game = TetrisGame()

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
