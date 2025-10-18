# OpenCV Integration Guide

PyRay provides seamless integration with OpenCV for computer vision and image processing capabilities.

## Installation

```bash
pip install pyray[opencv]
```

## Features

- **Surface/Array Conversion**: Convert between PyRay surfaces and NumPy arrays
- **Webcam Support**: Real-time webcam capture as PyRay textures
- **Image Filters**: Apply OpenCV filters (Canny edge, blur, threshold)
- **Face Detection**: Built-in face detection using Haar Cascades
- **Contour Detection**: Find and draw contours

## Basic Usage

### Webcam to Texture

```python
import pyray
from pyray.bridges.opencv import webcam_to_texture

# Initialize webcam
webcam = webcam_to_texture(0)  # Device ID 0

while not pyray.window_should_close():
    # Get webcam frame as texture
    texture = webcam.update()
    
    pyray.begin_drawing()
    pyray.clear_background(pyray.BLACK)
    
    if texture:
        pyray.draw_texture(texture, 0, 0, pyray.WHITE)
    
    pyray.end_drawing()

webcam.release()
```

### Applying Filters

```python
from pyray.bridges.opencv import (
    texture_to_ndarray,
    ndarray_to_texture,
    apply_canny_edge,
    apply_blur
)

# Convert texture to numpy array
arr = texture_to_ndarray(texture)

# Apply filter
filtered = apply_canny_edge(arr, low_threshold=50, high_threshold=150)
# or
blurred = apply_blur(arr, kernel_size=5)

# Convert back to texture
new_texture = ndarray_to_texture(filtered)
```

### Face Detection

```python
from pyray.bridges.opencv import detect_faces

# Detect faces in image
faces = detect_faces(image_array)

# Draw bounding boxes
for (x, y, w, h) in faces:
    pyray.draw_rectangle_lines(x, y, w, h, pyray.GREEN)
```

## Surface/Array Conversion

```python
from pyray.bridges.opencv import surface_to_ndarray, ndarray_to_surface

# PyRay surface to NumPy array
surface = pygame.display.get_surface()
arr = surface_to_ndarray(surface)  # Returns (H, W, 3) RGB array

# NumPy array to PyRay surface
surface = ndarray_to_surface(arr)
```

## Advanced Examples

### Real-time Edge Detection

```python
import pyray
from pyray.bridges.opencv import (
    webcam_to_texture,
    texture_to_ndarray,
    ndarray_to_texture,
    apply_canny_edge
)

webcam = webcam_to_texture(0)
edge_threshold_low = 50
edge_threshold_high = 150

while not pyray.window_should_close():
    # Adjust thresholds with keys
    if pyray.is_key_down(pyray.KEY_Q):
        edge_threshold_low = max(0, edge_threshold_low - 5)
    if pyray.is_key_down(pyray.KEY_W):
        edge_threshold_low = min(255, edge_threshold_low + 5)
    
    # Get frame and apply edge detection
    raw_texture = webcam.update()
    if raw_texture:
        arr = texture_to_ndarray(raw_texture)
        edges = apply_canny_edge(arr, edge_threshold_low, edge_threshold_high)
        texture = ndarray_to_texture(edges)
        
        pyray.begin_drawing()
        pyray.clear_background(pyray.BLACK)
        pyray.draw_texture(texture, 0, 0, pyray.WHITE)
        pyray.draw_text(f"Threshold: {edge_threshold_low}-{edge_threshold_high}", 10, 10, 20, pyray.WHITE)
        pyray.end_drawing()
```

### Motion Detection

```python
import cv2
import numpy as np
from pyray.bridges.opencv import webcam_to_texture, texture_to_ndarray

webcam = webcam_to_texture(0)
prev_frame = None
motion_threshold = 30

while not pyray.window_should_close():
    texture = webcam.update()
    if texture:
        frame = texture_to_ndarray(texture)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        if prev_frame is not None:
            # Calculate frame difference
            diff = cv2.absdiff(prev_frame, gray)
            _, thresh = cv2.threshold(diff, motion_threshold, 255, cv2.THRESH_BINARY)
            
            # Find contours (motion areas)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Draw motion areas
            for contour in contours:
                if cv2.contourArea(contour) > 500:  # Minimum area
                    x, y, w, h = cv2.boundingRect(contour)
                    pyray.draw_rectangle_lines(x, y, w, h, pyray.RED)
        
        prev_frame = gray
```

## Performance Tips

1. **Reuse Arrays**: Avoid creating new arrays every frame when possible
2. **Downscale**: Process smaller images for real-time performance
3. **Threading**: Consider processing in a separate thread for heavy operations
4. **Cache Textures**: Reuse texture objects instead of creating new ones

## Common Use Cases

- **Augmented Reality**: Overlay game elements on webcam feed
- **Computer Vision Games**: Games controlled by gestures or face tracking
- **Image Effects**: Real-time filters and effects
- **QR Code Reading**: Scan QR codes in-game
- **Motion Controls**: Use motion detection for input

## Troubleshooting

- **Webcam not found**: Check device ID, try 0, 1, or -1
- **Performance issues**: Reduce resolution or processing frequency
- **Import errors**: Ensure OpenCV is installed: `pip install opencv-python`

## See Also

- [OpenCV Documentation](https://docs.opencv.org/)
- [Example: Webcam Filters](../../examples/integrations/opencv_webcam_filters.py)
