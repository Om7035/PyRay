"""
Color definitions and utilities for PyRay
"""

from typing import Tuple, Union


class Color:
    """Represents an RGBA color"""
    
    def __init__(self, r: int, g: int, b: int, a: int = 255):
        """Create a color from RGBA values (0-255)"""
        self.r = max(0, min(255, r))
        self.g = max(0, min(255, g))
        self.b = max(0, min(255, b))
        self.a = max(0, min(255, a))
        
    def to_tuple(self) -> Tuple[int, int, int, int]:
        """Convert to RGBA tuple"""
        return (self.r, self.g, self.b, self.a)
        
    def to_rgb(self) -> Tuple[int, int, int]:
        """Convert to RGB tuple (no alpha)"""
        return (self.r, self.g, self.b)
        
    def __repr__(self) -> str:
        return f"Color({self.r}, {self.g}, {self.b}, {self.a})"
        
    def __eq__(self, other) -> bool:
        if isinstance(other, Color):
            return (self.r == other.r and self.g == other.g and 
                    self.b == other.b and self.a == other.a)
        return False
        
    @classmethod
    def from_hex(cls, hex_color: str) -> 'Color':
        """Create color from hex string (#RRGGBB or #RRGGBBAA)"""
        hex_color = hex_color.lstrip('#')
        
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return cls(r, g, b)
        elif len(hex_color) == 8:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            a = int(hex_color[6:8], 16)
            return cls(r, g, b, a)
        else:
            raise ValueError(f"Invalid hex color: {hex_color}")
            
    @classmethod
    def from_hsv(cls, h: float, s: float, v: float) -> 'Color':
        """Create color from HSV values (h: 0-360, s: 0-1, v: 0-1)"""
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(h / 360.0, s, v)
        return cls(int(r * 255), int(g * 255), int(b * 255))


def fade(color: Color, alpha: float) -> Color:
    """Fade a color to a specified alpha value (0.0 to 1.0)"""
    new_alpha = int(alpha * 255)
    return Color(color.r, color.g, color.b, new_alpha)


def color_to_int(color: Color) -> int:
    """Convert color to integer representation"""
    return (color.r << 24) | (color.g << 16) | (color.b << 8) | color.a


def get_color(hex_value: Union[int, str]) -> Color:
    """Get color from hexadecimal value"""
    if isinstance(hex_value, str):
        return Color.from_hex(hex_value)
    else:
        r = (hex_value >> 24) & 0xFF
        g = (hex_value >> 16) & 0xFF
        b = (hex_value >> 8) & 0xFF
        a = hex_value & 0xFF
        return Color(r, g, b, a)


# Basic colors
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
YELLOW = Color(255, 255, 0)
MAGENTA = Color(255, 0, 255)
CYAN = Color(0, 255, 255)
ORANGE = Color(255, 161, 0)
PURPLE = Color(128, 0, 128)
BROWN = Color(127, 106, 79)
GRAY = Color(128, 128, 128)
DARKGRAY = Color(64, 64, 64)
LIGHTGRAY = Color(192, 192, 192)

# Extended colors
LIME = Color(0, 255, 0)
GOLD = Color(255, 203, 0)
PINK = Color(255, 192, 203)
MAROON = Color(128, 0, 0)
SKYBLUE = Color(135, 206, 235)
VIOLET = Color(238, 130, 238)
BEIGE = Color(245, 245, 220)

# Transparent
BLANK = Color(0, 0, 0, 0)
