"""
PyRay + OpenCV Integration Example
Real-time webcam filters and effects
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pyray
from pyray.bridges.opencv import (
    webcam_to_texture, 
    texture_to_ndarray,
    ndarray_to_texture,
    apply_canny_edge,
    apply_blur,
    apply_threshold,
    detect_faces
)

# Window settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize PyRay
pyray.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "PyRay + OpenCV: Webcam Filters")
pyray.set_target_fps(30)

# Initialize webcam
try:
    webcam = webcam_to_texture(0)
    webcam_available = True
except Exception as e:
    print(f"Webcam not available: {e}")
    webcam_available = False

# Filter modes
FILTER_NONE = 0
FILTER_CANNY = 1
FILTER_BLUR = 2
FILTER_THRESHOLD = 3
FILTER_FACE_DETECT = 4
current_filter = FILTER_NONE

filter_names = ["None", "Canny Edge", "Blur", "Threshold", "Face Detection"]

# Parameters
blur_strength = 5
threshold_value = 127
canny_low = 50
canny_high = 150

# Main loop
while not pyray.window_should_close():
    # Update
    
    # Switch filters with number keys
    if pyray.is_key_pressed(pyray.KEY_ONE):
        current_filter = FILTER_NONE
    elif pyray.is_key_pressed(pyray.KEY_TWO):
        current_filter = FILTER_CANNY
    elif pyray.is_key_pressed(pyray.KEY_THREE):
        current_filter = FILTER_BLUR
    elif pyray.is_key_pressed(pyray.KEY_FOUR):
        current_filter = FILTER_THRESHOLD
    elif pyray.is_key_pressed(pyray.KEY_FIVE):
        current_filter = FILTER_FACE_DETECT
    
    # Adjust parameters
    if pyray.is_key_down(pyray.KEY_Q):
        blur_strength = max(1, blur_strength - 2)
    if pyray.is_key_down(pyray.KEY_W):
        blur_strength = min(31, blur_strength + 2)
        
    if pyray.is_key_down(pyray.KEY_A):
        threshold_value = max(0, threshold_value - 5)
    if pyray.is_key_down(pyray.KEY_S):
        threshold_value = min(255, threshold_value + 5)
    
    # Get webcam frame
    texture = None
    faces = []
    
    if webcam_available:
        raw_texture = webcam.update()
        
        if raw_texture and current_filter != FILTER_NONE:
            # Convert to numpy array
            arr = texture_to_ndarray(raw_texture)
            
            # Apply filter
            if current_filter == FILTER_CANNY:
                arr = apply_canny_edge(arr, canny_low, canny_high)
            elif current_filter == FILTER_BLUR:
                arr = apply_blur(arr, blur_strength)
            elif current_filter == FILTER_THRESHOLD:
                arr = apply_threshold(arr, threshold_value)
            elif current_filter == FILTER_FACE_DETECT:
                faces = detect_faces(arr)
            
            # Convert back to texture
            texture = ndarray_to_texture(arr)
        else:
            texture = raw_texture
    
    # Draw
    pyray.begin_drawing()
    pyray.clear_background(pyray.DARKGRAY)
    
    if webcam_available and texture:
        # Calculate position to center the webcam feed
        tex_width = texture.width
        tex_height = texture.height
        
        # Scale to fit window
        scale = min(SCREEN_WIDTH / tex_width, SCREEN_HEIGHT / tex_height) * 0.8
        draw_width = int(tex_width * scale)
        draw_height = int(tex_height * scale)
        draw_x = (SCREEN_WIDTH - draw_width) // 2
        draw_y = (SCREEN_HEIGHT - draw_height) // 2 + 20
        
        # Draw webcam texture
        pyray.draw_texture_ex(texture, draw_x, draw_y, 0, scale, pyray.WHITE)
        
        # Draw face detection boxes
        if current_filter == FILTER_FACE_DETECT:
            for (x, y, w, h) in faces:
                # Scale coordinates to match display
                rx = draw_x + int(x * scale)
                ry = draw_y + int(y * scale)
                rw = int(w * scale)
                rh = int(h * scale)
                pyray.draw_rectangle_lines(rx, ry, rw, rh, pyray.GREEN)
                pyray.draw_text("Face", rx, ry - 20, 16, pyray.GREEN)
    else:
        pyray.draw_text("Webcam not available", SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 20, pyray.WHITE)
        pyray.draw_text("Make sure OpenCV is installed:", SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 + 30, 16, pyray.LIGHTGRAY)
        pyray.draw_text("pip install pyray[opencv]", SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50, 16, pyray.LIGHTGRAY)
    
    # Draw UI
    pyray.draw_text("OpenCV Webcam Filters", 10, 10, 24, pyray.WHITE)
    pyray.draw_text(f"Current Filter: {filter_names[current_filter]}", 10, 40, 18, pyray.LIGHTGRAY)
    
    # Draw controls
    y_pos = SCREEN_HEIGHT - 120
    pyray.draw_text("Controls:", 10, y_pos, 16, pyray.WHITE)
    pyray.draw_text("1-5: Switch filters", 10, y_pos + 20, 14, pyray.LIGHTGRAY)
    
    if current_filter == FILTER_BLUR:
        pyray.draw_text(f"Q/W: Blur strength ({blur_strength})", 10, y_pos + 40, 14, pyray.LIGHTGRAY)
    elif current_filter == FILTER_THRESHOLD:
        pyray.draw_text(f"A/S: Threshold ({threshold_value})", 10, y_pos + 40, 14, pyray.LIGHTGRAY)
    
    pyray.draw_text("ESC: Exit", 10, y_pos + 60, 14, pyray.LIGHTGRAY)
    
    # Show FPS
    fps = pyray.get_fps()
    pyray.draw_text(f"FPS: {fps}", SCREEN_WIDTH - 80, 10, 16, pyray.GREEN)
    
    pyray.end_drawing()

# Cleanup
if webcam_available:
    webcam.release()
pyray.close_window()
