"""
PyRay - Python Game Development Made Simple

A simple and easy-to-use Python library for game development and multimedia applications.
"""

from pyray.__version__ import __version__

# Core module imports
from pyray.core import (
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
    set_target_fps,
    get_fps,
    get_frame_time,
    get_time,
)

# Graphics module imports
from pyray.graphics import (
    # Drawing functions
    begin_drawing,
    end_drawing,
    clear_background,
    
    # Basic shapes
    draw_pixel,
    draw_line,
    draw_circle,
    draw_circle_lines,
    draw_ellipse,
    draw_ellipse_lines,
    draw_rectangle,
    draw_rectangle_lines,
    draw_rectangle_rounded,
    draw_triangle,
    draw_triangle_lines,
    draw_polygon,
    draw_polygon_lines,
    
    # Text
    draw_text,
    draw_text_ex,
    measure_text,
    
    # Sprites/Images
    load_image,
    load_texture,
    unload_texture,
    draw_texture,
    draw_texture_ex,
    draw_texture_rect,
)

# Input module imports
from pyray.input import (
    # Keyboard
    is_key_pressed,
    is_key_released,
    is_key_down,
    is_key_up,
    get_key_pressed,
    get_char_pressed,
    
    # Mouse
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
    
    # Gamepad (Phase 2)
    # is_gamepad_available,
    # get_gamepad_name,
    # is_gamepad_button_pressed,
    # is_gamepad_button_down,
    # is_gamepad_button_released,
    # is_gamepad_button_up,
    # get_gamepad_axis_movement,
)

# Audio module imports (basic)
from pyray.audio import (
    init_audio_device,
    close_audio_device,
    is_audio_device_ready,
    set_master_volume,
    
    # Sound
    load_sound,
    unload_sound,
    play_sound,
    stop_sound,
    pause_sound,
    resume_sound,
    is_sound_playing,
    set_sound_volume,
    set_sound_pitch,
    
    # Music
    load_music_stream,
    unload_music_stream,
    play_music_stream,
    stop_music_stream,
    pause_music_stream,
    resume_music_stream,
    is_music_stream_playing,
    set_music_volume,
    set_music_pitch,
    get_music_time_length,
    get_music_time_played,
)

# Math utilities
from pyray.math import (
    Vector2,
    lerp,
    clamp,
    normalize,
    distance,
    angle,
    rotate_point,
    random_int,
    random_float,
)

# Color constants
from pyray.colors import (
    # Basic colors
    WHITE,
    BLACK,
    RED,
    GREEN,
    BLUE,
    YELLOW,
    MAGENTA,
    CYAN,
    ORANGE,
    PURPLE,
    BROWN,
    GRAY,
    DARKGRAY,
    LIGHTGRAY,
    
    # Extended colors
    LIME,
    GOLD,
    PINK,
    MAROON,
    SKYBLUE,
    VIOLET,
    BEIGE,
    
    # Utility
    Color,
    fade,
    color_to_int,
    get_color,
)

# Constants
from pyray.constants import (
    # Mouse buttons
    MOUSE_BUTTON_LEFT,
    MOUSE_BUTTON_RIGHT,
    MOUSE_BUTTON_MIDDLE,
    
    # Keyboard keys
    KEY_NULL,
    KEY_APOSTROPHE,
    KEY_COMMA,
    KEY_MINUS,
    KEY_PERIOD,
    KEY_SLASH,
    KEY_ZERO,
    KEY_ONE,
    KEY_TWO,
    KEY_THREE,
    KEY_FOUR,
    KEY_FIVE,
    KEY_SIX,
    KEY_SEVEN,
    KEY_EIGHT,
    KEY_NINE,
    KEY_SEMICOLON,
    KEY_EQUAL,
    KEY_A,
    KEY_B,
    KEY_C,
    KEY_D,
    KEY_E,
    KEY_F,
    KEY_G,
    KEY_H,
    KEY_I,
    KEY_J,
    KEY_K,
    KEY_L,
    KEY_M,
    KEY_N,
    KEY_O,
    KEY_P,
    KEY_Q,
    KEY_R,
    KEY_S,
    KEY_T,
    KEY_U,
    KEY_V,
    KEY_W,
    KEY_X,
    KEY_Y,
    KEY_Z,
    KEY_LEFT_BRACKET,
    KEY_BACKSLASH,
    KEY_RIGHT_BRACKET,
    KEY_GRAVE,
    KEY_SPACE,
    KEY_ESCAPE,
    KEY_ENTER,
    KEY_TAB,
    KEY_BACKSPACE,
    KEY_INSERT,
    KEY_DELETE,
    KEY_RIGHT,
    KEY_LEFT,
    KEY_DOWN,
    KEY_UP,
    KEY_PAGE_UP,
    KEY_PAGE_DOWN,
    KEY_HOME,
    KEY_END,
    KEY_CAPS_LOCK,
    KEY_SCROLL_LOCK,
    KEY_NUM_LOCK,
    KEY_PRINT_SCREEN,
    KEY_PAUSE,
    KEY_F1,
    KEY_F2,
    KEY_F3,
    KEY_F4,
    KEY_F5,
    KEY_F6,
    KEY_F7,
    KEY_F8,
    KEY_F9,
    KEY_F10,
    KEY_F11,
    KEY_F12,
    KEY_LEFT_SHIFT,
    KEY_LEFT_CONTROL,
    KEY_LEFT_ALT,
    KEY_LEFT_SUPER,
    KEY_RIGHT_SHIFT,
    KEY_RIGHT_CONTROL,
    KEY_RIGHT_ALT,
    KEY_RIGHT_SUPER,
)

__all__ = [
    "__version__",
    
    # Core functions
    "init_window",
    "close_window",
    "window_should_close",
    "is_window_ready",
    "set_window_title",
    "set_target_fps",
    "get_fps",
    "get_frame_time",
    
    # Graphics functions
    "begin_drawing",
    "end_drawing",
    "clear_background",
    "draw_circle",
    "draw_rectangle",
    "draw_line",
    "draw_text",
    "load_texture",
    "draw_texture",
    
    # Input functions
    "is_key_pressed",
    "is_key_down",
    "get_mouse_x",
    "get_mouse_y",
    "is_mouse_button_pressed",
    
    # Audio functions
    "init_audio_device",
    "load_sound",
    "play_sound",
    
    # Math utilities
    "Vector2",
    "lerp",
    
    # Colors
    "Color",
    "WHITE",
    "BLACK",
    "RED",
    "GREEN",
    "BLUE",
    
    # Add more as needed...
]
