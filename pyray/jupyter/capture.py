"""
Jupyter notebook capture utilities for PyRay
Enables rendering PyRay content in Jupyter notebooks
"""

import pygame
import numpy as np
from typing import Optional, List, Callable
from PIL import Image
import io
import base64

try:
    from IPython.display import display, clear_output, HTML, Image as IPImage
    import ipywidgets as widgets
    HAS_IPYTHON = True
except ImportError:
    HAS_IPYTHON = False

try:
    import imageio
    HAS_IMAGEIO = True
except ImportError:
    HAS_IMAGEIO = False


class NotebookRenderer:
    """Manages PyRay rendering in Jupyter notebooks"""
    
    def __init__(self, width: int = 640, height: int = 480, fps: int = 30):
        """
        Initialize notebook renderer
        
        Args:
            width: Window width
            height: Window height
            fps: Target frames per second
        """
        self.width = width
        self.height = height
        self.fps = fps
        self.frames: List[Image.Image] = []
        self.recording = False
        
    def start_recording(self):
        """Start recording frames"""
        self.frames = []
        self.recording = True
        
    def stop_recording(self):
        """Stop recording frames"""
        self.recording = False
        
    def capture_and_display(self):
        """Capture current frame and display in notebook"""
        frame = capture_frame()
        if frame and HAS_IPYTHON:
            display_frame(frame)
            
        if self.recording and frame:
            self.frames.append(frame)
            
    def save_gif(self, filename: str = "output.gif"):
        """Save recorded frames as GIF"""
        if self.frames:
            record_gif(self.frames, filename, self.fps)
            
    def save_video(self, filename: str = "output.mp4"):
        """Save recorded frames as video"""
        if self.frames:
            record_video(self.frames, filename, self.fps)


def capture_frame() -> Optional[Image.Image]:
    """Capture the current PyRay frame as a PIL Image
    
    Returns:
        PIL Image of the current frame, or None if no window
    """
    try:
        # Get the current pygame surface
        surface = pygame.display.get_surface()
        if surface is None:
            return None
            
        # Convert to numpy array
        arr = pygame.surfarray.array3d(surface)
        # Transpose from (W, H, 3) to (H, W, 3)
        arr = np.transpose(arr, (1, 0, 2))
        
        # Create PIL Image
        img = Image.fromarray(arr.astype(np.uint8))
        return img
        
    except Exception as e:
        print(f"Error capturing frame: {e}")
        return None


def display_frame(image: Image.Image, clear: bool = True):
    """Display a PIL Image in the notebook
    
    Args:
        image: PIL Image to display
        clear: Whether to clear previous output
    """
    if not HAS_IPYTHON:
        print("IPython not available. Cannot display in notebook.")
        return
        
    if clear:
        clear_output(wait=True)
        
    # Convert to bytes
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    buf.seek(0)
    
    # Display
    display(IPImage(data=buf.read()))


def record_gif(frames: List[Image.Image], filename: str = "output.gif", 
               fps: int = 30, loop: int = 0):
    """Record a list of frames as an animated GIF
    
    Args:
        frames: List of PIL Images
        filename: Output filename
        fps: Frames per second
        loop: Number of loops (0 = infinite)
    """
    if not frames:
        print("No frames to save")
        return
        
    if not HAS_IMAGEIO:
        # Fallback to PIL
        frames[0].save(
            filename,
            save_all=True,
            append_images=frames[1:],
            duration=1000//fps,
            loop=loop
        )
    else:
        # Use imageio for better quality
        imageio.mimsave(filename, frames, duration=1/fps, loop=loop)
        
    print(f"Saved {len(frames)} frames to {filename}")


def record_video(frames: List[Image.Image], filename: str = "output.mp4", 
                fps: int = 30):
    """Record a list of frames as a video file
    
    Args:
        frames: List of PIL Images
        filename: Output filename
        fps: Frames per second
    """
    if not HAS_IMAGEIO:
        print("imageio is required for video export. Install with: pip install pyray[jupyter]")
        return
        
    if not frames:
        print("No frames to save")
        return
        
    # Convert PIL images to numpy arrays
    arrays = [np.array(img) for img in frames]
    
    # Save as video
    imageio.mimsave(filename, arrays, fps=fps)
    print(f"Saved {len(frames)} frames to {filename}")


def create_notebook_window(width: int = 640, height: int = 480, 
                          title: str = "PyRay Notebook") -> NotebookRenderer:
    """Create a PyRay window suitable for notebook rendering
    
    Args:
        width: Window width
        height: Window height
        title: Window title
        
    Returns:
        NotebookRenderer instance
        
    Example:
        renderer = create_notebook_window(640, 480)
        renderer.start_recording()
        
        for i in range(60):
            pyray.begin_drawing()
            pyray.clear_background(pyray.BLACK)
            pyray.draw_circle(320 + i*2, 240, 20, pyray.RED)
            pyray.end_drawing()
            renderer.capture_and_display()
            
        renderer.save_gif("animation.gif")
    """
    import pyray
    
    # Initialize PyRay window
    pyray.init_window(width, height, title)
    
    # Create renderer
    renderer = NotebookRenderer(width, height)
    
    return renderer


# Interactive widgets for notebooks
def create_slider_control(label: str, min_val: float = 0, max_val: float = 100, 
                         initial: float = 50, callback: Optional[Callable] = None):
    """Create an interactive slider for notebooks
    
    Args:
        label: Slider label
        min_val: Minimum value
        max_val: Maximum value
        initial: Initial value
        callback: Function to call on value change
        
    Returns:
        ipywidgets slider if available, None otherwise
    """
    if not HAS_IPYTHON:
        return None
        
    slider = widgets.FloatSlider(
        value=initial,
        min=min_val,
        max=max_val,
        description=label,
        continuous_update=True
    )
    
    if callback:
        slider.observe(lambda change: callback(change['new']), names='value')
        
    return slider


def create_color_picker(label: str = "Color", 
                        initial: str = "#FF0000",
                        callback: Optional[Callable] = None):
    """Create a color picker widget for notebooks
    
    Args:
        label: Widget label
        initial: Initial color (hex string)
        callback: Function to call on color change
        
    Returns:
        ipywidgets color picker if available, None otherwise
    """
    if not HAS_IPYTHON:
        return None
        
    picker = widgets.ColorPicker(
        value=initial,
        description=label,
        disabled=False
    )
    
    if callback:
        picker.observe(lambda change: callback(change['new']), names='value')
        
    return picker


def create_button(label: str, callback: Callable):
    """Create a button widget for notebooks
    
    Args:
        label: Button label
        callback: Function to call on click
        
    Returns:
        ipywidgets button if available, None otherwise
    """
    if not HAS_IPYTHON:
        return None
        
    button = widgets.Button(description=label)
    button.on_click(lambda b: callback())
    
    return button


def inline_game_loop(update_fn: Callable, draw_fn: Callable, 
                     frames: int = 60, fps: int = 30,
                     width: int = 640, height: int = 480):
    """Run a game loop inline in a notebook with automatic capture
    
    Args:
        update_fn: Update function (called each frame)
        draw_fn: Draw function (called each frame)
        frames: Number of frames to run
        fps: Target frames per second
        width: Window width
        height: Window height
        
    Example:
        def update():
            global x
            x += 2
            
        def draw():
            pyray.begin_drawing()
            pyray.clear_background(pyray.BLACK)
            pyray.draw_circle(x, 240, 20, pyray.RED)
            pyray.end_drawing()
            
        inline_game_loop(update, draw, frames=120)
    """
    import pyray
    import time
    
    # Create window and renderer
    renderer = create_notebook_window(width, height)
    renderer.start_recording()
    
    frame_time = 1.0 / fps
    
    for i in range(frames):
        start_time = time.time()
        
        # Update and draw
        update_fn()
        draw_fn()
        
        # Capture and display
        renderer.capture_and_display()
        
        # Frame timing
        elapsed = time.time() - start_time
        if elapsed < frame_time:
            time.sleep(frame_time - elapsed)
    
    # Clean up
    pyray.close_window()
    
    return renderer
