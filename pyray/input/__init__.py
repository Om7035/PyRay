"""
PyRay Input Module
Handles keyboard, mouse, and gamepad input
"""

from pyray.input.keyboard import (
    is_key_pressed,
    is_key_released,
    is_key_down,
    is_key_up,
    get_key_pressed,
    get_char_pressed,
    set_exit_key,
)

from pyray.input.mouse import (
    is_mouse_button_pressed,
    is_mouse_button_released,
    is_mouse_button_down,
    is_mouse_button_up,
    get_mouse_x,
    get_mouse_y,
    get_mouse_position,
    get_mouse_delta,
    set_mouse_position,
    get_mouse_wheel_move,
    show_cursor,
    hide_cursor,
    is_cursor_hidden,
    is_cursor_on_screen,
)

__all__ = [
    # Keyboard
    "is_key_pressed",
    "is_key_released",
    "is_key_down",
    "is_key_up",
    "get_key_pressed",
    "get_char_pressed",
    "set_exit_key",
    
    # Mouse
    "is_mouse_button_pressed",
    "is_mouse_button_released",
    "is_mouse_button_down",
    "is_mouse_button_up",
    "get_mouse_x",
    "get_mouse_y",
    "get_mouse_position",
    "get_mouse_delta",
    "set_mouse_position",
    "get_mouse_wheel_move",
    "show_cursor",
    "hide_cursor",
    "is_cursor_hidden",
    "is_cursor_on_screen",
]
