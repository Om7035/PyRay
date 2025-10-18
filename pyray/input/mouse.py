"""
Mouse input module for PyRay
Handles mouse position, buttons, and wheel
"""

import pygame
from typing import Tuple, Set
from pyray.math import Vector2


class MouseManager:
    """Manages mouse input state"""
    
    def __init__(self):
        self.x: int = 0
        self.y: int = 0
        self.last_x: int = 0
        self.last_y: int = 0
        self.delta_x: int = 0
        self.delta_y: int = 0
        self.wheel_move: float = 0.0
        
        self.buttons_down: Set[int] = set()
        self.buttons_pressed: Set[int] = set()
        self.buttons_released: Set[int] = set()
        self.last_buttons_down: Set[int] = set()
        
        self.cursor_hidden: bool = False
        self.cursor_on_screen: bool = True
        
    def update(self) -> None:
        """Update mouse state (called each frame)"""
        # Update position
        self.last_x = self.x
        self.last_y = self.y
        self.x, self.y = pygame.mouse.get_pos()
        self.delta_x = self.x - self.last_x
        self.delta_y = self.y - self.last_y
        
        # Update button state
        buttons = pygame.mouse.get_pressed(num_buttons=5)
        current_buttons = {i for i, pressed in enumerate(buttons) if pressed}
        
        self.buttons_pressed = current_buttons - self.last_buttons_down
        self.buttons_released = self.last_buttons_down - current_buttons
        
        self.buttons_down = current_buttons
        self.last_buttons_down = current_buttons.copy()
        
        # Update wheel
        self.wheel_move = 0.0
        for event in pygame.event.get(pygame.MOUSEWHEEL):
            self.wheel_move += event.y
            
        # Check if cursor is on screen
        self.cursor_on_screen = pygame.mouse.get_focused()
        
    def is_button_down(self, button: int) -> bool:
        """Check if mouse button is being held down"""
        return button in self.buttons_down
        
    def is_button_pressed(self, button: int) -> bool:
        """Check if mouse button was just pressed"""
        return button in self.buttons_pressed
        
    def is_button_released(self, button: int) -> bool:
        """Check if mouse button was just released"""
        return button in self.buttons_released
        
    def is_button_up(self, button: int) -> bool:
        """Check if mouse button is not being held"""
        return button not in self.buttons_down
        
    def set_position(self, x: int, y: int) -> None:
        """Set mouse position"""
        pygame.mouse.set_pos(x, y)
        self.x = x
        self.y = y
        
    def show_cursor(self) -> None:
        """Show mouse cursor"""
        pygame.mouse.set_visible(True)
        self.cursor_hidden = False
        
    def hide_cursor(self) -> None:
        """Hide mouse cursor"""
        pygame.mouse.set_visible(False)
        self.cursor_hidden = True


# Global mouse manager
_mouse_manager = MouseManager()


# Public API functions
def is_mouse_button_pressed(button: int) -> bool:
    """Check if a mouse button has been pressed once"""
    return _mouse_manager.is_button_pressed(button)


def is_mouse_button_released(button: int) -> bool:
    """Check if a mouse button has been released once"""
    return _mouse_manager.is_button_released(button)


def is_mouse_button_down(button: int) -> bool:
    """Check if a mouse button is being pressed"""
    return _mouse_manager.is_button_down(button)


def is_mouse_button_up(button: int) -> bool:
    """Check if a mouse button is not being pressed"""
    return _mouse_manager.is_button_up(button)


def get_mouse_x() -> int:
    """Get mouse position X"""
    return _mouse_manager.x


def get_mouse_y() -> int:
    """Get mouse position Y"""
    return _mouse_manager.y


def get_mouse_position() -> Vector2:
    """Get mouse position as Vector2"""
    return Vector2(_mouse_manager.x, _mouse_manager.y)


def get_mouse_delta() -> Vector2:
    """Get mouse delta between frames"""
    return Vector2(_mouse_manager.delta_x, _mouse_manager.delta_y)


def set_mouse_position(x: int, y: int) -> None:
    """Set mouse position"""
    _mouse_manager.set_position(x, y)


def get_mouse_wheel_move() -> float:
    """Get mouse wheel movement for this frame"""
    return _mouse_manager.wheel_move


def show_cursor() -> None:
    """Show mouse cursor"""
    _mouse_manager.show_cursor()


def hide_cursor() -> None:
    """Hide mouse cursor"""
    _mouse_manager.hide_cursor()


def is_cursor_hidden() -> bool:
    """Check if cursor is hidden"""
    return _mouse_manager.cursor_hidden


def is_cursor_on_screen() -> bool:
    """Check if cursor is on screen/window"""
    return _mouse_manager.cursor_on_screen


def update_mouse() -> None:
    """Update mouse state (internal use)"""
    _mouse_manager.update()
