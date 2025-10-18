# PyRay API Reference (Overview)

This is a high-level overview of the modules and key functions available in Phase 1. Full auto-generated docs will be added with Sphinx.

## Modules

- `pyray.core`
  - Window: `init_window`, `close_window`, `window_should_close`, `toggle_fullscreen`
  - Timing: `set_target_fps`, `get_fps`, `get_frame_time`, `get_time`

- `pyray.graphics`
  - Drawing control: `begin_drawing`, `end_drawing`, `clear_background`
  - Shapes: `draw_pixel`, `draw_line`, `draw_circle`, `draw_circle_lines`, `draw_ellipse`, `draw_rectangle`, `draw_rectangle_lines`, `draw_rectangle_rounded`, `draw_triangle`, `draw_triangle_lines`, `draw_polygon`, `draw_polygon_lines`
  - Text: `draw_text`, `draw_text_ex`, `measure_text`, `load_font`, `unload_font`
  - Textures: `load_image`, `load_texture`, `unload_texture`, `draw_texture`, `draw_texture_ex`, `draw_texture_rect`

- `pyray.input`
  - Keyboard: `is_key_pressed`, `is_key_released`, `is_key_down`, `is_key_up`, `get_key_pressed`, `get_char_pressed`, `set_exit_key`
  - Mouse: `is_mouse_button_pressed`, `is_mouse_button_released`, `is_mouse_button_down`, `is_mouse_button_up`, `get_mouse_x`, `get_mouse_y`, `get_mouse_position`, `get_mouse_delta`, `set_mouse_position`, `get_mouse_wheel_move`, `show_cursor`, `hide_cursor`, `is_cursor_hidden`, `is_cursor_on_screen`

- `pyray.audio`
  - Device: `init_audio_device`, `close_audio_device`, `is_audio_device_ready`, `set_master_volume`
  - Sound: `load_sound`, `unload_sound`, `play_sound`, `stop_sound`, `pause_sound`, `resume_sound`, `is_sound_playing`, `set_sound_volume`, `set_sound_pitch`
  - Music: `load_music_stream`, `unload_music_stream`, `play_music_stream`, `stop_music_stream`, `pause_music_stream`, `resume_music_stream`, `is_music_stream_playing`, `set_music_volume`, `set_music_pitch`, `seek_music_stream`, `get_music_time_length`, `get_music_time_played`

- `pyray.math`
  - Types: `Vector2`
  - Helpers: `lerp`, `clamp`, `normalize`, `distance`, `angle`, `rotate_point`, `random_int`, `random_float`

- `pyray.colors`
  - `Color` plus color constants like `WHITE`, `BLACK`, `RED`, `DARKGRAY`, etc.

- `pyray.constants`
  - Keyboard and mouse button constants (e.g., `KEY_A`, `KEY_SPACE`, `MOUSE_BUTTON_LEFT`).

## Notes

- All drawing should happen between `begin_drawing()` and `end_drawing()` each frame.
- Always call `close_window()` when you're done to free resources.
- Input states update each frame; check them within your main loop.

## Coming Soon

- Phase 2/3/4 APIs will be added over time. See `docs/roadmap/` for details and contribute!
