"""
PyRay Example - Input Handling
Demonstrates keyboard and mouse input handling
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pyray

# Window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize window
pyray.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "PyRay - Input Handling")

# Set target FPS
pyray.set_target_fps(60)

# Ball position and properties
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_radius = 20
ball_speed = 5
ball_color = pyray.RED

# Text to display
last_key = "None"
mouse_clicks = 0

# Main game loop
while not pyray.window_should_close():
    # Update
    
    # Keyboard input - move ball with arrow keys or WASD
    if pyray.is_key_down(pyray.KEY_RIGHT) or pyray.is_key_down(pyray.KEY_D):
        ball_x += ball_speed
    if pyray.is_key_down(pyray.KEY_LEFT) or pyray.is_key_down(pyray.KEY_A):
        ball_x -= ball_speed
    if pyray.is_key_down(pyray.KEY_DOWN) or pyray.is_key_down(pyray.KEY_S):
        ball_y += ball_speed
    if pyray.is_key_down(pyray.KEY_UP) or pyray.is_key_down(pyray.KEY_W):
        ball_y -= ball_speed
    
    # Keep ball on screen
    ball_x = pyray.clamp(ball_x, ball_radius, SCREEN_WIDTH - ball_radius)
    ball_y = pyray.clamp(ball_y, ball_radius, SCREEN_HEIGHT - ball_radius)
    
    # Change color with space
    if pyray.is_key_pressed(pyray.KEY_SPACE):
        if ball_color == pyray.RED:
            ball_color = pyray.GREEN
        elif ball_color == pyray.GREEN:
            ball_color = pyray.BLUE
        else:
            ball_color = pyray.RED
    
    # Reset position with R
    if pyray.is_key_pressed(pyray.KEY_R):
        ball_x = SCREEN_WIDTH // 2
        ball_y = SCREEN_HEIGHT // 2
    
    # Track last key pressed
    key = pyray.get_key_pressed()
    if key > 0:
        last_key = f"Key code: {key}"
    
    # Mouse input
    mouse_x = pyray.get_mouse_x()
    mouse_y = pyray.get_mouse_y()
    
    # Move ball to mouse on click
    if pyray.is_mouse_button_pressed(pyray.MOUSE_BUTTON_LEFT):
        ball_x = mouse_x
        ball_y = mouse_y
        mouse_clicks += 1
    
    # Change ball size with mouse wheel
    wheel = pyray.get_mouse_wheel_move()
    if wheel != 0:
        ball_radius += int(wheel * 5)
        ball_radius = pyray.clamp(ball_radius, 10, 50)
    
    # Draw
    pyray.begin_drawing()
    
    # Clear background
    pyray.clear_background(pyray.WHITE)
    
    # Draw title
    pyray.draw_text("Input Handling Demo", 250, 20, 25, pyray.DARKGRAY)
    
    # Draw instructions
    pyray.draw_text("Controls:", 20, 60, 20, pyray.BLACK)
    pyray.draw_text("- Arrow Keys or WASD: Move ball", 20, 90, 16, pyray.DARKGRAY)
    pyray.draw_text("- Space: Change color", 20, 110, 16, pyray.DARKGRAY)
    pyray.draw_text("- R: Reset position", 20, 130, 16, pyray.DARKGRAY)
    pyray.draw_text("- Left Click: Move ball to mouse", 20, 150, 16, pyray.DARKGRAY)
    pyray.draw_text("- Mouse Wheel: Change ball size", 20, 170, 16, pyray.DARKGRAY)
    pyray.draw_text("- ESC: Exit", 20, 190, 16, pyray.DARKGRAY)
    
    # Draw input status
    pyray.draw_text("Input Status:", 500, 60, 20, pyray.BLACK)
    pyray.draw_text(f"Mouse: ({mouse_x}, {mouse_y})", 500, 90, 16, pyray.DARKGRAY)
    pyray.draw_text(f"Last key: {last_key}", 500, 110, 16, pyray.DARKGRAY)
    pyray.draw_text(f"Mouse clicks: {mouse_clicks}", 500, 130, 16, pyray.DARKGRAY)
    pyray.draw_text(f"Ball size: {ball_radius}", 500, 150, 16, pyray.DARKGRAY)
    
    # Draw the ball
    pyray.draw_circle(ball_x, ball_y, ball_radius, ball_color)
    
    # Draw crosshair at mouse position
    pyray.draw_line(mouse_x - 10, mouse_y, mouse_x + 10, mouse_y, pyray.GRAY)
    pyray.draw_line(mouse_x, mouse_y - 10, mouse_x, mouse_y + 10, pyray.GRAY)
    
    # Show FPS
    fps = pyray.get_fps()
    pyray.draw_text(f"FPS: {fps}", 10, 10, 20, pyray.GREEN)
    
    pyray.end_drawing()

# Cleanup
pyray.close_window()
