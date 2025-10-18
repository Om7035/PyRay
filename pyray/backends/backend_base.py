"""
Base backend interface for PyRay
Defines the common API that all backends must implement
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple, Optional, Any

class BackendType(Enum):
    PYGAME = "pygame"
    MODERNGL = "moderngl"
    PYGLET = "pyglet"

class Backend(ABC):
    """Abstract base class for PyRay rendering backends"""
    
    @abstractmethod
    def init_window(self, width: int, height: int, title: str) -> None:
        """Initialize the window"""
        pass
    
    @abstractmethod
    def close_window(self) -> None:
        """Close the window"""
        pass
    
    @abstractmethod
    def window_should_close(self) -> bool:
        """Check if window should close"""
        pass
    
    @abstractmethod
    def begin_drawing(self) -> None:
        """Begin drawing mode"""
        pass
    
    @abstractmethod
    def end_drawing(self) -> None:
        """End drawing mode and present frame"""
        pass
    
    @abstractmethod
    def clear_background(self, color: Tuple[int, int, int, int]) -> None:
        """Clear the background with a color"""
        pass
    
    @abstractmethod
    def draw_pixel(self, x: int, y: int, color: Tuple[int, int, int, int]) -> None:
        """Draw a pixel"""
        pass
    
    @abstractmethod
    def draw_line(self, x1: int, y1: int, x2: int, y2: int, 
                  color: Tuple[int, int, int, int]) -> None:
        """Draw a line"""
        pass
    
    @abstractmethod
    def draw_rectangle(self, x: int, y: int, width: int, height: int,
                      color: Tuple[int, int, int, int]) -> None:
        """Draw a filled rectangle"""
        pass
    
    @abstractmethod
    def draw_rectangle_lines(self, x: int, y: int, width: int, height: int,
                            color: Tuple[int, int, int, int]) -> None:
        """Draw rectangle outline"""
        pass
    
    @abstractmethod
    def draw_circle(self, center_x: int, center_y: int, radius: float,
                   color: Tuple[int, int, int, int]) -> None:
        """Draw a filled circle"""
        pass
    
    @abstractmethod
    def draw_circle_lines(self, center_x: int, center_y: int, radius: float,
                         color: Tuple[int, int, int, int]) -> None:
        """Draw circle outline"""
        pass
    
    @abstractmethod
    def draw_text(self, text: str, x: int, y: int, font_size: int,
                 color: Tuple[int, int, int, int]) -> None:
        """Draw text"""
        pass
    
    @abstractmethod
    def load_texture(self, filename: str) -> Any:
        """Load a texture from file"""
        pass
    
    @abstractmethod
    def draw_texture(self, texture: Any, x: int, y: int,
                    tint: Tuple[int, int, int, int] = (255, 255, 255, 255)) -> None:
        """Draw a texture"""
        pass
    
    @abstractmethod
    def get_fps(self) -> int:
        """Get current FPS"""
        pass
    
    @abstractmethod
    def set_target_fps(self, fps: int) -> None:
        """Set target FPS"""
        pass
    
    @abstractmethod
    def get_frame_time(self) -> float:
        """Get frame time in seconds"""
        pass
    
    # Input methods
    @abstractmethod
    def is_key_pressed(self, key: int) -> bool:
        """Check if key was pressed this frame"""
        pass
    
    @abstractmethod
    def is_key_down(self, key: int) -> bool:
        """Check if key is currently down"""
        pass
    
    @abstractmethod
    def is_mouse_button_pressed(self, button: int) -> bool:
        """Check if mouse button was pressed this frame"""
        pass
    
    @abstractmethod
    def is_mouse_button_down(self, button: int) -> bool:
        """Check if mouse button is currently down"""
        pass
    
    @abstractmethod
    def get_mouse_position(self) -> Tuple[int, int]:
        """Get mouse position"""
        pass
    
    # Optional advanced features
    def supports_shaders(self) -> bool:
        """Check if backend supports custom shaders"""
        return False
    
    def load_shader(self, vertex_source: str, fragment_source: str) -> Optional[Any]:
        """Load a custom shader (if supported)"""
        return None
    
    def use_shader(self, shader: Any) -> None:
        """Use a custom shader for rendering"""
        pass
    
    def supports_3d(self) -> bool:
        """Check if backend supports 3D rendering"""
        return False
    
    def begin_3d_mode(self, camera: Any) -> None:
        """Begin 3D rendering mode"""
        pass
    
    def end_3d_mode(self) -> None:
        """End 3D rendering mode"""
        pass
