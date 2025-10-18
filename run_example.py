"""
Quick test script to verify PyRay is working
Run this to test the library installation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyray

# Simple test window
pyray.init_window(400, 300, "PyRay Test")
pyray.set_target_fps(60)

frame_count = 0
max_frames = 180  # Run for 3 seconds at 60 FPS

print("PyRay initialized successfully!")
print("Running test for 3 seconds...")

while not pyray.window_should_close() and frame_count < max_frames:
    frame_count += 1
    
    pyray.begin_drawing()
    pyray.clear_background(pyray.DARKGRAY)
    
    # Draw test elements
    pyray.draw_text("PyRay is working!", 100, 100, 20, pyray.WHITE)
    pyray.draw_circle(200, 200, 30, pyray.RED)
    pyray.draw_rectangle(50, 50, 60, 40, pyray.GREEN)
    
    # Show frame counter
    pyray.draw_text(f"Frame: {frame_count}/{max_frames}", 10, 10, 16, pyray.LIGHTGRAY)
    
    pyray.end_drawing()

pyray.close_window()
print("Test completed successfully!")
