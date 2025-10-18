"""
Math utilities for PyRay
Provides vector math, interpolation, and other mathematical functions
"""

import math
import random
from typing import Tuple, Optional


class Vector2:
    """2D vector class with common operations"""
    
    def __init__(self, x: float = 0.0, y: float = 0.0):
        """Create a 2D vector"""
        self.x = float(x)
        self.y = float(y)
        
    def __add__(self, other: 'Vector2') -> 'Vector2':
        """Add two vectors"""
        return Vector2(self.x + other.x, self.y + other.y)
        
    def __sub__(self, other: 'Vector2') -> 'Vector2':
        """Subtract two vectors"""
        return Vector2(self.x - other.x, self.y - other.y)
        
    def __mul__(self, scalar: float) -> 'Vector2':
        """Multiply vector by scalar"""
        return Vector2(self.x * scalar, self.y * scalar)
        
    def __truediv__(self, scalar: float) -> 'Vector2':
        """Divide vector by scalar"""
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Vector2(self.x / scalar, self.y / scalar)
        
    def __neg__(self) -> 'Vector2':
        """Negate vector"""
        return Vector2(-self.x, -self.y)
        
    def __eq__(self, other) -> bool:
        """Check if two vectors are equal"""
        if isinstance(other, Vector2):
            return abs(self.x - other.x) < 1e-6 and abs(self.y - other.y) < 1e-6
        return False
        
    def __repr__(self) -> str:
        return f"Vector2({self.x}, {self.y})"
        
    def length(self) -> float:
        """Get vector length/magnitude"""
        return math.sqrt(self.x * self.x + self.y * self.y)
        
    def length_squared(self) -> float:
        """Get squared length (faster than length)"""
        return self.x * self.x + self.y * self.y
        
    def normalize(self) -> 'Vector2':
        """Get normalized vector (unit vector)"""
        length = self.length()
        if length == 0:
            return Vector2(0, 0)
        return Vector2(self.x / length, self.y / length)
        
    def dot(self, other: 'Vector2') -> float:
        """Calculate dot product with another vector"""
        return self.x * other.x + self.y * other.y
        
    def angle(self) -> float:
        """Get angle of vector in radians"""
        return math.atan2(self.y, self.x)
        
    def rotate(self, angle: float) -> 'Vector2':
        """Rotate vector by angle (in radians)"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vector2(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )
        
    def distance_to(self, other: 'Vector2') -> float:
        """Calculate distance to another vector"""
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)
        
    def to_tuple(self) -> Tuple[float, float]:
        """Convert to tuple"""
        return (self.x, self.y)
        
    @classmethod
    def zero(cls) -> 'Vector2':
        """Create zero vector"""
        return cls(0, 0)
        
    @classmethod
    def one(cls) -> 'Vector2':
        """Create unit vector (1, 1)"""
        return cls(1, 1)
        
    @classmethod
    def up(cls) -> 'Vector2':
        """Create up vector (0, -1)"""
        return cls(0, -1)
        
    @classmethod
    def down(cls) -> 'Vector2':
        """Create down vector (0, 1)"""
        return cls(0, 1)
        
    @classmethod
    def left(cls) -> 'Vector2':
        """Create left vector (-1, 0)"""
        return cls(-1, 0)
        
    @classmethod
    def right(cls) -> 'Vector2':
        """Create right vector (1, 0)"""
        return cls(1, 0)


def lerp(start: float, end: float, amount: float) -> float:
    """Linear interpolation between two values"""
    return start + (end - start) * amount


def lerp_vector2(start: Vector2, end: Vector2, amount: float) -> Vector2:
    """Linear interpolation between two vectors"""
    return Vector2(
        lerp(start.x, end.x, amount),
        lerp(start.y, end.y, amount)
    )


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Clamp value between min and max"""
    return max(min_value, min(max_value, value))


def normalize(value: float, start: float, end: float) -> float:
    """Normalize value between start and end (returns 0-1)"""
    if end - start == 0:
        return 0
    return (value - start) / (end - start)


def remap(value: float, input_start: float, input_end: float, 
          output_start: float, output_end: float) -> float:
    """Remap value from one range to another"""
    normalized = normalize(value, input_start, input_end)
    return lerp(output_start, output_end, normalized)


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate distance between two points"""
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx * dx + dy * dy)


def distance_vector2(v1: Vector2, v2: Vector2) -> float:
    """Calculate distance between two vectors"""
    return v1.distance_to(v2)


def angle(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate angle between two points in radians"""
    return math.atan2(y2 - y1, x2 - x1)


def angle_vector2(v1: Vector2, v2: Vector2) -> float:
    """Calculate angle between two vectors in radians"""
    return math.atan2(v2.y - v1.y, v2.x - v1.x)


def rotate_point(x: float, y: float, cx: float, cy: float, angle: float) -> Tuple[float, float]:
    """Rotate a point around a center point by angle (in radians)"""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    
    # Translate to origin
    tx = x - cx
    ty = y - cy
    
    # Rotate
    rx = tx * cos_a - ty * sin_a
    ry = tx * sin_a + ty * cos_a
    
    # Translate back
    return (rx + cx, ry + cy)


def degrees_to_radians(degrees: float) -> float:
    """Convert degrees to radians"""
    return degrees * math.pi / 180.0


def radians_to_degrees(radians: float) -> float:
    """Convert radians to degrees"""
    return radians * 180.0 / math.pi


def random_int(min_value: int, max_value: int) -> int:
    """Get random integer between min and max (inclusive)"""
    return random.randint(min_value, max_value)


def random_float(min_value: float = 0.0, max_value: float = 1.0) -> float:
    """Get random float between min and max"""
    return random.uniform(min_value, max_value)


def random_vector2(min_x: float, max_x: float, min_y: float, max_y: float) -> Vector2:
    """Get random vector within specified ranges"""
    return Vector2(
        random_float(min_x, max_x),
        random_float(min_y, max_y)
    )


def wrap(value: float, min_value: float, max_value: float) -> float:
    """Wrap value between min and max"""
    range_size = max_value - min_value
    if range_size <= 0:
        return min_value
        
    result = value - min_value
    result = result % range_size
    return result + min_value


def sign(value: float) -> int:
    """Get sign of value (-1, 0, or 1)"""
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0
