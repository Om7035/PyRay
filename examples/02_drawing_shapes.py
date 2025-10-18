"""
PyRay Example - Drawing Shapes
Demonstrates drawing various 2D shapes with PyRay
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pyray

# Window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize window
pyray.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "PyRay - Drawing Shapes")

# Set target FPS
pyray.set_target_fps(60)

# Main game loop
while not pyray.window_should_close():
    # Draw
    pyray.begin_drawing()
    
    # Clear background
    pyray.clear_background(pyray.LIGHTGRAY)
    
    # Draw title
    pyray.draw_text("PyRay - Drawing Shapes", 250, 20, 25, pyray.DARKGRAY)
    
    # Draw filled shapes
    pyray.draw_text("Filled Shapes", 100, 80, 20, pyray.BLACK)
    
    # Rectangle
    pyray.draw_rectangle(50, 120, 100, 60, pyray.RED)
    pyray.draw_text("Rectangle", 60, 190, 12, pyray.BLACK)
    
    # Circle
    pyray.draw_circle(250, 150, 30, pyray.GREEN)
    pyray.draw_text("Circle", 230, 190, 12, pyray.BLACK)
    
    # Triangle
    v1 = pyray.Vector2(380, 120)
    v2 = pyray.Vector2(330, 180)
    v3 = pyray.Vector2(430, 180)
    pyray.draw_triangle(v1, v2, v3, pyray.BLUE)
    pyray.draw_text("Triangle", 360, 190, 12, pyray.BLACK)
    
    # Ellipse
    pyray.draw_ellipse(550, 150, 40, 25, pyray.ORANGE)
    pyray.draw_text("Ellipse", 530, 190, 12, pyray.BLACK)
    
    # Draw outlined shapes
    pyray.draw_text("Outlined Shapes", 100, 250, 20, pyray.BLACK)
    
    # Rectangle lines
    pyray.draw_rectangle_lines(50, 290, 100, 60, pyray.RED)
    pyray.draw_text("Rectangle", 60, 360, 12, pyray.BLACK)
    
    # Circle lines
    pyray.draw_circle_lines(250, 320, 30, pyray.GREEN)
    pyray.draw_text("Circle", 230, 360, 12, pyray.BLACK)
    
    # Triangle lines
    v1 = pyray.Vector2(380, 290)
    v2 = pyray.Vector2(330, 350)
    v3 = pyray.Vector2(430, 350)
    pyray.draw_triangle_lines(v1, v2, v3, pyray.BLUE)
    pyray.draw_text("Triangle", 360, 360, 12, pyray.BLACK)
    
    # Ellipse lines
    pyray.draw_ellipse_lines(550, 320, 40, 25, pyray.ORANGE)
    pyray.draw_text("Ellipse", 530, 360, 12, pyray.BLACK)
    
    # Draw lines
    pyray.draw_text("Lines", 100, 420, 20, pyray.BLACK)
    pyray.draw_line(50, 460, 150, 460, pyray.PURPLE)
    pyray.draw_line(200, 450, 300, 470, pyray.MAROON)
    pyray.draw_line(350, 470, 450, 450, pyray.VIOLET)
    
    # Draw polygon
    center = pyray.Vector2(650, 480)
    pyray.draw_polygon(center, 6, 30, 0, pyray.GOLD)
    pyray.draw_text("Polygon", 620, 520, 12, pyray.BLACK)
    
    # Show FPS
    fps = pyray.get_fps()
    pyray.draw_text(f"FPS: {fps}", 10, 10, 20, pyray.GREEN)
    
    pyray.end_drawing()

# Cleanup
pyray.close_window()
