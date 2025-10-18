"""
Keyboard input module for PyRay
Handles keyboard state and input events
"""

import pygame
from typing import Optional, Set


class KeyboardManager:
    """Manages keyboard input state"""
    
    def __init__(self):
        self.keys_down: Set[int] = set()
        self.keys_pressed: Set[int] = set()  # Just pressed this frame
        self.keys_released: Set[int] = set()  # Just released this frame
        self.last_keys_down: Set[int] = set()
        self.char_pressed: Optional[str] = None
        self.exit_key: int = pygame.K_ESCAPE
        
    def update(self) -> None:
        """Update keyboard state (called each frame)"""
        # Get current keyboard state
        keys = pygame.key.get_pressed()
        current_keys = {i for i, pressed in enumerate(keys) if pressed}
        
        # Calculate pressed and released keys
        self.keys_pressed = current_keys - self.last_keys_down
        self.keys_released = self.last_keys_down - current_keys
        
        # Update state
        self.keys_down = current_keys
        self.last_keys_down = current_keys.copy()
        
        # Handle text input
        self.char_pressed = None
        for event in pygame.event.get(pygame.KEYDOWN):
            if event.unicode and event.unicode.isprintable():
                self.char_pressed = event.unicode
                
    def is_key_down(self, key: int) -> bool:
        """Check if key is currently being held down"""
        return key in self.keys_down
        
    def is_key_pressed(self, key: int) -> bool:
        """Check if key was just pressed this frame"""
        return key in self.keys_pressed
        
    def is_key_released(self, key: int) -> bool:
        """Check if key was just released this frame"""
        return key in self.keys_released
        
    def is_key_up(self, key: int) -> bool:
        """Check if key is not being held down"""
        return key not in self.keys_down
        
    def get_key_pressed(self) -> int:
        """Get the last key pressed (0 if none)"""
        if self.keys_pressed:
            return next(iter(self.keys_pressed))
        return 0
        
    def get_char_pressed(self) -> Optional[str]:
        """Get the last character pressed"""
        return self.char_pressed


# Global keyboard manager
_keyboard_manager = KeyboardManager()


# Public API functions
def is_key_pressed(key: int) -> bool:
    """Check if a key has been pressed once"""
    return _keyboard_manager.is_key_pressed(key)


def is_key_released(key: int) -> bool:
    """Check if a key has been released once"""
    return _keyboard_manager.is_key_released(key)


def is_key_down(key: int) -> bool:
    """Check if a key is being pressed"""
    return _keyboard_manager.is_key_down(key)


def is_key_up(key: int) -> bool:
    """Check if a key is not being pressed"""
    return _keyboard_manager.is_key_up(key)


def get_key_pressed() -> int:
    """Get key pressed (keycode), call it multiple times for multiple keys"""
    return _keyboard_manager.get_key_pressed()


def get_char_pressed() -> Optional[str]:
    """Get char pressed (unicode), call it multiple times for multiple chars"""
    return _keyboard_manager.get_char_pressed()


def set_exit_key(key: int) -> None:
    """Set exit key (default is ESC)"""
    _keyboard_manager.exit_key = key


def update_keyboard() -> None:
    """Update keyboard state (internal use)"""
    _keyboard_manager.update()
