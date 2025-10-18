"""
PyRay Core Module
Handles window management, game loop, and core functionality
"""

from pyray.core.window import (
    init_window,
    close_window,
    window_should_close,
    is_window_ready,
    is_window_fullscreen,
    is_window_hidden,
    is_window_minimized,
    is_window_maximized,
    is_window_focused,
    is_window_resized,
    set_window_title,
    set_window_position,
    set_window_size,
    set_window_min_size,
    set_window_max_size,
    get_window_width,
    get_window_height,
    get_screen_width,
    get_screen_height,
    toggle_fullscreen,
)

from pyray.core.timing import (
    set_target_fps,
    get_fps,
    get_frame_time,
    get_time,
)

__all__ = [
    # Window management
    "init_window",
    "close_window",
    "window_should_close",
    "is_window_ready",
    "is_window_fullscreen",
    "is_window_hidden",
    "is_window_minimized",
    "is_window_maximized",
    "is_window_focused",
    "is_window_resized",
    "set_window_title",
    "set_window_position",
    "set_window_size",
    "set_window_min_size",
    "set_window_max_size",
    "get_window_width",
    "get_window_height",
    "get_screen_width",
    "get_screen_height",
    "toggle_fullscreen",
    
    # Timing
    "set_target_fps",
    "get_fps",
    "get_frame_time",
    "get_time",
]
