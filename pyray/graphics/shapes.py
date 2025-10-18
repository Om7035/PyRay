"""
Shape drawing module for PyRay
Provides functions to draw various 2D shapes
"""

import pygame
import math
from typing import List, Tuple
from pyray.core.window import get_window_handle
from pyray.colors import Color
from pyray.math import Vector2


def draw_pixel(x: int, y: int, color: Color) -> None:
    """Draw a pixel at specified position"""
    screen = get_window_handle()
    if screen:
        screen.set_at((x, y), color.to_tuple())


def draw_line(start_x: int, start_y: int, end_x: int, end_y: int, color: Color) -> None:
    """Draw a line between two points"""
    screen = get_window_handle()
    if screen:
        pygame.draw.line(screen, color.to_rgb(), (start_x, start_y), (end_x, end_y), 1)


def draw_line_ex(start: Vector2, end: Vector2, thickness: float, color: Color) -> None:
    """Draw a line with specified thickness"""
    screen = get_window_handle()
    if screen:
        pygame.draw.line(screen, color.to_rgb(), 
                        (start.x, start.y), (end.x, end.y), int(thickness))


def draw_circle(center_x: int, center_y: int, radius: float, color: Color) -> None:
    """Draw a filled circle"""
    screen = get_window_handle()
    if screen:
        pygame.draw.circle(screen, color.to_rgb(), (center_x, center_y), int(radius))


def draw_circle_lines(center_x: int, center_y: int, radius: float, color: Color) -> None:
    """Draw circle outline"""
    screen = get_window_handle()
    if screen:
        pygame.draw.circle(screen, color.to_rgb(), (center_x, center_y), int(radius), 1)


def draw_ellipse(center_x: int, center_y: int, radius_h: float, radius_v: float, color: Color) -> None:
    """Draw a filled ellipse"""
    screen = get_window_handle()
    if screen:
        rect = pygame.Rect(center_x - radius_h, center_y - radius_v, 
                          radius_h * 2, radius_v * 2)
        pygame.draw.ellipse(screen, color.to_rgb(), rect)


def draw_ellipse_lines(center_x: int, center_y: int, radius_h: float, radius_v: float, color: Color) -> None:
    """Draw ellipse outline"""
    screen = get_window_handle()
    if screen:
        rect = pygame.Rect(center_x - radius_h, center_y - radius_v, 
                          radius_h * 2, radius_v * 2)
        pygame.draw.ellipse(screen, color.to_rgb(), rect, 1)


def draw_rectangle(x: int, y: int, width: int, height: int, color: Color) -> None:
    """Draw a filled rectangle"""
    screen = get_window_handle()
    if screen:
        pygame.draw.rect(screen, color.to_rgb(), (x, y, width, height))


def draw_rectangle_lines(x: int, y: int, width: int, height: int, color: Color) -> None:
    """Draw rectangle outline"""
    screen = get_window_handle()
    if screen:
        pygame.draw.rect(screen, color.to_rgb(), (x, y, width, height), 1)


def draw_rectangle_rounded(x: int, y: int, width: int, height: int, 
                          roundness: float, segments: int, color: Color) -> None:
    """Draw a rounded rectangle"""
    screen = get_window_handle()
    if screen:
        rect = pygame.Rect(x, y, width, height)
        border_radius = int(min(width, height) * roundness / 2)
        
        # Draw rounded rectangle using pygame's built-in function (pygame 2.0+)
        try:
            pygame.draw.rect(screen, color.to_rgb(), rect, border_radius=border_radius)
        except TypeError:
            # Fallback for older pygame versions
            pygame.draw.rect(screen, color.to_rgb(), rect)


def draw_triangle(v1: Vector2, v2: Vector2, v3: Vector2, color: Color) -> None:
    """Draw a filled triangle"""
    screen = get_window_handle()
    if screen:
        points = [(v1.x, v1.y), (v2.x, v2.y), (v3.x, v3.y)]
        pygame.draw.polygon(screen, color.to_rgb(), points)


def draw_triangle_lines(v1: Vector2, v2: Vector2, v3: Vector2, color: Color) -> None:
    """Draw triangle outline"""
    screen = get_window_handle()
    if screen:
        points = [(v1.x, v1.y), (v2.x, v2.y), (v3.x, v3.y)]
        pygame.draw.polygon(screen, color.to_rgb(), points, 1)


def draw_polygon(center: Vector2, sides: int, radius: float, rotation: float, color: Color) -> None:
    """Draw a regular polygon"""
    screen = get_window_handle()
    if screen:
        points = []
        angle_step = (2 * math.pi) / sides
        
        for i in range(sides):
            angle = rotation + (i * angle_step)
            x = center.x + radius * math.cos(angle)
            y = center.y + radius * math.sin(angle)
            points.append((x, y))
            
        pygame.draw.polygon(screen, color.to_rgb(), points)


def draw_polygon_lines(center: Vector2, sides: int, radius: float, rotation: float, color: Color) -> None:
    """Draw a regular polygon outline"""
    screen = get_window_handle()
    if screen:
        points = []
        angle_step = (2 * math.pi) / sides
        
        for i in range(sides):
            angle = rotation + (i * angle_step)
            x = center.x + radius * math.cos(angle)
            y = center.y + radius * math.sin(angle)
            points.append((x, y))
            
        pygame.draw.polygon(screen, color.to_rgb(), points, 1)
