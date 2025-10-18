"""
OpenCV Bridge for PyRay
Provides interoperability between OpenCV and PyRay for computer vision applications
"""

import pygame
import numpy as np
from typing import Optional, Tuple, Any
from pyray.graphics.texture import Texture

try:
    import cv2
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False
    cv2 = None


class WebcamCapture:
    """Manages webcam capture and conversion to PyRay textures"""
    
    def __init__(self, device_id: int = 0):
        if not HAS_OPENCV:
            raise ImportError("OpenCV is required. Install with: pip install pyray[opencv]")
        
        self.cap = cv2.VideoCapture(device_id)
        self.texture: Optional[Texture] = None
        
    def update(self) -> Optional[Texture]:
        """Capture a frame and convert to texture"""
        ret, frame = self.cap.read()
        if ret:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert to texture
            self.texture = ndarray_to_texture(frame_rgb)
            return self.texture
        return None
    
    def release(self):
        """Release the webcam"""
        if self.cap:
            self.cap.release()
            
    def __del__(self):
        self.release()


def surface_to_ndarray(surface: pygame.Surface) -> np.ndarray:
    """Convert a pygame Surface to a numpy array
    
    Args:
        surface: pygame Surface to convert
        
    Returns:
        numpy array in RGB format (H, W, 3)
    """
    # Get the pixel array
    arr = pygame.surfarray.array3d(surface)
    # Transpose from (W, H, 3) to (H, W, 3)
    arr = np.transpose(arr, (1, 0, 2))
    return arr


def ndarray_to_surface(array: np.ndarray) -> pygame.Surface:
    """Convert a numpy array to a pygame Surface
    
    Args:
        array: numpy array in RGB format (H, W, 3)
        
    Returns:
        pygame Surface
    """
    # Ensure array is uint8
    if array.dtype != np.uint8:
        array = np.clip(array, 0, 255).astype(np.uint8)
    
    # Transpose from (H, W, 3) to (W, H, 3) for pygame
    arr_transposed = np.transpose(array, (1, 0, 2))
    
    # Create surface from array
    surface = pygame.surfarray.make_surface(arr_transposed)
    return surface


def ndarray_to_texture(array: np.ndarray) -> Texture:
    """Convert a numpy array to a PyRay texture
    
    Args:
        array: numpy array in RGB format (H, W, 3)
        
    Returns:
        PyRay Texture object
    """
    surface = ndarray_to_surface(array)
    return Texture(surface, f"opencv_array_{id(array)}")


def texture_to_ndarray(texture: Texture) -> np.ndarray:
    """Convert a PyRay texture to a numpy array
    
    Args:
        texture: PyRay Texture object
        
    Returns:
        numpy array in RGB format (H, W, 3)
    """
    return surface_to_ndarray(texture.surface)


def webcam_to_texture(device_id: int = 0) -> WebcamCapture:
    """Create a webcam capture that provides textures
    
    Args:
        device_id: Camera device ID (default 0)
        
    Returns:
        WebcamCapture object
        
    Example:
        webcam = webcam_to_texture(0)
        while not pyray.window_should_close():
            texture = webcam.update()
            if texture:
                pyray.draw_texture(texture, 0, 0)
    """
    return WebcamCapture(device_id)


# OpenCV filter helpers
def apply_canny_edge(array: np.ndarray, low_threshold: int = 50, 
                     high_threshold: int = 150) -> np.ndarray:
    """Apply Canny edge detection to an image
    
    Args:
        array: Input image array
        low_threshold: Lower threshold for edge detection
        high_threshold: Upper threshold for edge detection
        
    Returns:
        Edge-detected image array
    """
    if not HAS_OPENCV:
        raise ImportError("OpenCV is required for filters")
    
    # Convert to grayscale if needed
    if len(array.shape) == 3:
        gray = cv2.cvtColor(array, cv2.COLOR_RGB2GRAY)
    else:
        gray = array
    
    # Apply Canny edge detection
    edges = cv2.Canny(gray, low_threshold, high_threshold)
    
    # Convert back to RGB
    edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    return edges_rgb


def apply_blur(array: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """Apply Gaussian blur to an image
    
    Args:
        array: Input image array
        kernel_size: Size of the blur kernel (must be odd)
        
    Returns:
        Blurred image array
    """
    if not HAS_OPENCV:
        raise ImportError("OpenCV is required for filters")
    
    if kernel_size % 2 == 0:
        kernel_size += 1  # Ensure odd kernel size
    
    return cv2.GaussianBlur(array, (kernel_size, kernel_size), 0)


def apply_threshold(array: np.ndarray, threshold: int = 127, 
                   max_value: int = 255) -> np.ndarray:
    """Apply binary threshold to an image
    
    Args:
        array: Input image array
        threshold: Threshold value
        max_value: Maximum value to use with THRESH_BINARY
        
    Returns:
        Thresholded image array
    """
    if not HAS_OPENCV:
        raise ImportError("OpenCV is required for filters")
    
    # Convert to grayscale if needed
    if len(array.shape) == 3:
        gray = cv2.cvtColor(array, cv2.COLOR_RGB2GRAY)
    else:
        gray = array
    
    # Apply threshold
    _, thresh = cv2.threshold(gray, threshold, max_value, cv2.THRESH_BINARY)
    
    # Convert back to RGB
    thresh_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
    return thresh_rgb


def detect_faces(array: np.ndarray) -> list:
    """Detect faces in an image using Haar Cascades
    
    Args:
        array: Input image array
        
    Returns:
        List of face rectangles (x, y, w, h)
    """
    if not HAS_OPENCV:
        raise ImportError("OpenCV is required for face detection")
    
    # Load face cascade
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(array, cv2.COLOR_RGB2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    return faces.tolist() if len(faces) > 0 else []


def draw_contours(array: np.ndarray, color: Tuple[int, int, int] = (0, 255, 0), 
                  thickness: int = 2) -> np.ndarray:
    """Find and draw contours on an image
    
    Args:
        array: Input image array
        color: Color of contours (RGB)
        thickness: Thickness of contour lines
        
    Returns:
        Image with contours drawn
    """
    if not HAS_OPENCV:
        raise ImportError("OpenCV is required for contour detection")
    
    # Convert to grayscale
    gray = cv2.cvtColor(array, cv2.COLOR_RGB2GRAY)
    
    # Find contours
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw contours on a copy
    result = array.copy()
    cv2.drawContours(result, contours, -1, color[::-1], thickness)  # BGR for OpenCV
    
    return result
