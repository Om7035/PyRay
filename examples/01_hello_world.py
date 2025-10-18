"""
PyRay Example - Hello World
The simplest PyRay program - creates a window and displays text
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pyray

# Window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

# Initialize window
pyray.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "PyRay - Hello World")

# Set target FPS
pyray.set_target_fps(60)

# Main game loop
while not pyray.window_should_close():
    # Draw
    pyray.begin_drawing()
    
    # Clear background
    pyray.clear_background(pyray.WHITE)
    
    # Draw text
    pyray.draw_text("Hello, PyRay!", 290, 200, 30, pyray.BLACK)
    pyray.draw_text("Welcome to Python Game Development!", 180, 250, 20, pyray.DARKGRAY)
    
    # Show FPS
    fps = pyray.get_fps()
    pyray.draw_text(f"FPS: {fps}", 10, 10, 20, pyray.GREEN)
    
    pyray.end_drawing()

# Cleanup
pyray.close_window()
