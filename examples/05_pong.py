"""
PyRay Example - Pong Game
A complete Pong game implementation in under 200 lines
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pyray

# Window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Game constants
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 80
PADDLE_SPEED = 5
BALL_SIZE = 10
BALL_SPEED = 5
WINNING_SCORE = 5

# Initialize window
pyray.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "PyRay - Pong Game")

# Set target FPS
pyray.set_target_fps(60)

# Initialize audio (optional)
pyray.init_audio_device()

# Game state
class GameState:
    def __init__(self):
        self.reset_game()
        
    def reset_game(self):
        # Paddle positions
        self.player1_y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.player2_y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        
        # Ball position and velocity
        self.ball_x = SCREEN_WIDTH // 2
        self.ball_y = SCREEN_HEIGHT // 2
        self.ball_vx = BALL_SPEED
        self.ball_vy = pyray.random_float(-3, 3)
        
        # Scores
        self.player1_score = 0
        self.player2_score = 0
        
        # Game state
        self.game_paused = False
        self.game_over = False
        self.winner = ""
    
    def reset_ball(self, direction=1):
        self.ball_x = SCREEN_WIDTH // 2
        self.ball_y = SCREEN_HEIGHT // 2
        self.ball_vx = BALL_SPEED * direction
        self.ball_vy = pyray.random_float(-3, 3)
    
    def update(self):
        if self.game_over or self.game_paused:
            return
        
        # Player 1 controls (W/S)
        if pyray.is_key_down(pyray.KEY_W):
            self.player1_y -= PADDLE_SPEED
        if pyray.is_key_down(pyray.KEY_S):
            self.player1_y += PADDLE_SPEED
        
        # Player 2 controls (Up/Down arrows)
        if pyray.is_key_down(pyray.KEY_UP):
            self.player2_y -= PADDLE_SPEED
        if pyray.is_key_down(pyray.KEY_DOWN):
            self.player2_y += PADDLE_SPEED
        
        # Keep paddles on screen
        self.player1_y = pyray.clamp(self.player1_y, 0, SCREEN_HEIGHT - PADDLE_HEIGHT)
        self.player2_y = pyray.clamp(self.player2_y, 0, SCREEN_HEIGHT - PADDLE_HEIGHT)
        
        # Update ball position
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy
        
        # Ball collision with top/bottom walls
        if self.ball_y - BALL_SIZE <= 0 or self.ball_y + BALL_SIZE >= SCREEN_HEIGHT:
            self.ball_vy *= -1
            self.ball_y = pyray.clamp(self.ball_y, BALL_SIZE, SCREEN_HEIGHT - BALL_SIZE)
        
        # Ball collision with paddles
        # Left paddle (Player 1)
        if (self.ball_x - BALL_SIZE <= 30 + PADDLE_WIDTH and 
            self.ball_x - BALL_SIZE >= 30 and
            self.ball_y >= self.player1_y and 
            self.ball_y <= self.player1_y + PADDLE_HEIGHT):
            self.ball_vx = abs(self.ball_vx)
            # Add spin based on where ball hits paddle
            hit_pos = (self.ball_y - self.player1_y) / PADDLE_HEIGHT
            self.ball_vy = (hit_pos - 0.5) * 8
        
        # Right paddle (Player 2)
        if (self.ball_x + BALL_SIZE >= SCREEN_WIDTH - 30 - PADDLE_WIDTH and 
            self.ball_x + BALL_SIZE <= SCREEN_WIDTH - 30 and
            self.ball_y >= self.player2_y and 
            self.ball_y <= self.player2_y + PADDLE_HEIGHT):
            self.ball_vx = -abs(self.ball_vx)
            # Add spin based on where ball hits paddle
            hit_pos = (self.ball_y - self.player2_y) / PADDLE_HEIGHT
            self.ball_vy = (hit_pos - 0.5) * 8
        
        # Score when ball goes off screen
        if self.ball_x < 0:
            self.player2_score += 1
            self.reset_ball(-1)
            if self.player2_score >= WINNING_SCORE:
                self.game_over = True
                self.winner = "Player 2"
        elif self.ball_x > SCREEN_WIDTH:
            self.player1_score += 1
            self.reset_ball(1)
            if self.player1_score >= WINNING_SCORE:
                self.game_over = True
                self.winner = "Player 1"
    
    def draw(self):
        # Draw center line
        for y in range(0, SCREEN_HEIGHT, 20):
            pyray.draw_rectangle(SCREEN_WIDTH // 2 - 2, y, 4, 10, pyray.LIGHTGRAY)
        
        # Draw paddles
        pyray.draw_rectangle(30, self.player1_y, PADDLE_WIDTH, PADDLE_HEIGHT, pyray.WHITE)
        pyray.draw_rectangle(SCREEN_WIDTH - 30 - PADDLE_WIDTH, self.player2_y, 
                            PADDLE_WIDTH, PADDLE_HEIGHT, pyray.WHITE)
        
        # Draw ball
        pyray.draw_circle(int(self.ball_x), int(self.ball_y), BALL_SIZE, pyray.WHITE)
        
        # Draw scores
        pyray.draw_text(str(self.player1_score), SCREEN_WIDTH // 2 - 50, 30, 40, pyray.WHITE)
        pyray.draw_text(str(self.player2_score), SCREEN_WIDTH // 2 + 30, 30, 40, pyray.WHITE)
        
        # Draw player labels
        pyray.draw_text("Player 1", 30, 10, 16, pyray.LIGHTGRAY)
        pyray.draw_text("Player 2", SCREEN_WIDTH - 100, 10, 16, pyray.LIGHTGRAY)
        
        # Draw controls
        pyray.draw_text("W/S", 30, SCREEN_HEIGHT - 25, 14, pyray.GRAY)
        pyray.draw_text("↑/↓", SCREEN_WIDTH - 50, SCREEN_HEIGHT - 25, 14, pyray.GRAY)

# Create game state
game = GameState()

# Main game loop
while not pyray.window_should_close():
    # Update
    
    # Toggle pause
    if pyray.is_key_pressed(pyray.KEY_SPACE):
        game.game_paused = not game.game_paused
    
    # Reset game
    if pyray.is_key_pressed(pyray.KEY_R):
        game.reset_game()
    
    # Update game
    game.update()
    
    # Draw
    pyray.begin_drawing()
    
    # Clear background
    pyray.clear_background(pyray.BLACK)
    
    # Draw game
    game.draw()
    
    # Draw UI
    if game.game_paused and not game.game_over:
        pyray.draw_text("PAUSED", SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2, 30, pyray.YELLOW)
        pyray.draw_text("Press SPACE to continue", SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 40, 16, pyray.LIGHTGRAY)
    
    if game.game_over:
        pyray.draw_text(f"{game.winner} Wins!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 30, pyray.GOLD)
        pyray.draw_text("Press R to play again", SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2, 16, pyray.LIGHTGRAY)
        pyray.draw_text("Press ESC to exit", SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 30, 16, pyray.LIGHTGRAY)
    
    if not game.game_over and not game.game_paused:
        pyray.draw_text("First to 5 wins! | SPACE: Pause | R: Reset", SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT - 25, 14, pyray.GRAY)
    
    # Show FPS
    fps = pyray.get_fps()
    pyray.draw_text(f"FPS: {fps}", 10, 10, 14, pyray.GREEN)
    
    pyray.end_drawing()

# Cleanup
pyray.close_audio_device()
pyray.close_window()
