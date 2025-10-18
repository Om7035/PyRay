"""
Drawing control module for PyRay
Manages the drawing context and rendering pipeline
"""

import pygame
from typing import Tuple
from pyray.core.window import get_window_handle
from pyray.core.timing import tick
from pyray.colors import Color
from pyray.input.keyboard import update_keyboard
from pyray.input.mouse import update_mouse


class DrawingContext:
    """Manages the drawing state"""
    
    def __init__(self):
        self.is_drawing = False
        self.background_color = (0, 0, 0)  # Black by default
        
    def begin(self) -> None:
        """Begin drawing mode"""
        if self.is_drawing:
            raise RuntimeError("begin_drawing() called while already drawing")
        self.is_drawing = True
        
    def end(self) -> None:
        """End drawing mode and present frame"""
        if not self.is_drawing:
            raise RuntimeError("end_drawing() called without begin_drawing()")
            
        # Update the display
        pygame.display.flip()
        
        # Update input systems
        update_keyboard()
        update_mouse()
        
        # Update timing
        tick()
        
        self.is_drawing = False
        
    def clear(self, color: Tuple[int, int, int]) -> None:
        """Clear the screen with specified color"""
        screen = get_window_handle()
        if screen:
            screen.fill(color)


# Global drawing context
_drawing_context = DrawingContext()


# Public API functions
def begin_drawing() -> None:
    """Begin drawing mode"""
    _drawing_context.begin()


def end_drawing() -> None:
    """End drawing mode and swap buffers"""
    _drawing_context.end()


def clear_background(color: Color) -> None:
    """Clear background with specified color"""
    _drawing_context.clear(color.to_tuple()[:3])  # RGB only


def is_drawing() -> bool:
    """Check if currently in drawing mode"""
    return _drawing_context.is_drawing
