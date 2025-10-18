"""
PyRay Graphics Module
Handles 2D/3D rendering, drawing, and graphics operations
"""

from pyray.graphics.drawing import (
    begin_drawing,
    end_drawing,
    clear_background,
)

from pyray.graphics.shapes import (
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
)

from pyray.graphics.text import (
    draw_text,
    draw_text_ex,
    measure_text,
    load_font,
    unload_font,
)

from pyray.graphics.texture import (
    load_image,
    load_texture,
    unload_texture,
    draw_texture,
    draw_texture_ex,
    draw_texture_rect,
)

__all__ = [
    # Drawing control
    "begin_drawing",
    "end_drawing",
    "clear_background",
    
    # Shapes
    "draw_pixel",
    "draw_line",
    "draw_circle",
    "draw_circle_lines",
    "draw_ellipse",
    "draw_ellipse_lines",
    "draw_rectangle",
    "draw_rectangle_lines",
    "draw_rectangle_rounded",
    "draw_triangle",
    "draw_triangle_lines",
    "draw_polygon",
    "draw_polygon_lines",
    
    # Text
    "draw_text",
    "draw_text_ex",
    "measure_text",
    "load_font",
    "unload_font",
    
    # Textures
    "load_image",
    "load_texture",
    "unload_texture",
    "draw_texture",
    "draw_texture_ex",
    "draw_texture_rect",
]
