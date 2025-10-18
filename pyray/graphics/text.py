"""
Text rendering module for PyRay
Handles font loading and text drawing
"""

import pygame
from typing import Optional, Dict, Tuple
from pyray.core.window import get_window_handle
from pyray.colors import Color


class Font:
    """Represents a loaded font"""
    
    def __init__(self, pygame_font: pygame.font.Font):
        self.font = pygame_font
        self.size = pygame_font.get_height()
        
    def render(self, text: str, color: Color) -> pygame.Surface:
        """Render text to a surface"""
        return self.font.render(text, True, color.to_rgb())
        
    def measure(self, text: str) -> Tuple[int, int]:
        """Get the size of rendered text"""
        return self.font.size(text)


class TextManager:
    """Manages fonts and text rendering"""
    
    def __init__(self):
        self.fonts: Dict[str, Font] = {}
        self.default_font: Optional[Font] = None
        self.default_font_size = 20
        
        # Initialize pygame font system
        pygame.font.init()
        
        # Load default font
        self._load_default_font()
        
    def _load_default_font(self) -> None:
        """Load the default system font"""
        try:
            pygame_font = pygame.font.Font(None, self.default_font_size)
            self.default_font = Font(pygame_font)
        except Exception as e:
            print(f"Warning: Could not load default font: {e}")
            
    def load_font(self, filename: str, size: int) -> Font:
        """Load a font from file"""
        key = f"{filename}_{size}"
        
        if key in self.fonts:
            return self.fonts[key]
            
        try:
            pygame_font = pygame.font.Font(filename, size)
            font = Font(pygame_font)
            self.fonts[key] = font
            return font
        except Exception as e:
            print(f"Error loading font {filename}: {e}")
            return self.default_font
            
    def load_font_from_memory(self, font_data: bytes, size: int) -> Font:
        """Load a font from memory"""
        try:
            import io
            font_io = io.BytesIO(font_data)
            pygame_font = pygame.font.Font(font_io, size)
            return Font(pygame_font)
        except Exception as e:
            print(f"Error loading font from memory: {e}")
            return self.default_font
            
    def unload_font(self, font: Font) -> None:
        """Unload a font (cleanup)"""
        # Remove from cache if present
        for key, cached_font in list(self.fonts.items()):
            if cached_font == font:
                del self.fonts[key]
                
    def draw_text(self, text: str, x: int, y: int, size: int, color: Color, 
                  font: Optional[Font] = None) -> None:
        """Draw text at specified position"""
        screen = get_window_handle()
        if not screen:
            return
            
        # Use provided font or create temporary one with specified size
        if font is None:
            if size != self.default_font_size:
                temp_font = pygame.font.Font(None, size)
                rendered = temp_font.render(text, True, color.to_rgb())
            else:
                if self.default_font:
                    rendered = self.default_font.render(text, color)
                else:
                    return
        else:
            rendered = font.render(text, color)
            
        screen.blit(rendered, (x, y))
        
    def draw_text_ex(self, font: Font, text: str, position: Tuple[int, int], 
                     font_size: float, spacing: float, color: Color) -> None:
        """Draw text with extended parameters"""
        screen = get_window_handle()
        if not screen:
            return
            
        # Render text
        rendered = font.render(text, color)
        
        # Apply scaling if font_size differs from font's natural size
        if font_size != font.size:
            scale = font_size / font.size
            width = int(rendered.get_width() * scale)
            height = int(rendered.get_height() * scale)
            rendered = pygame.transform.scale(rendered, (width, height))
            
        screen.blit(rendered, position)
        
    def measure_text(self, text: str, font_size: int, 
                     font: Optional[Font] = None) -> int:
        """Measure text width"""
        if font is None:
            if self.default_font:
                width, _ = self.default_font.measure(text)
                if font_size != self.default_font_size:
                    scale = font_size / self.default_font_size
                    width = int(width * scale)
                return width
            else:
                # Rough estimate if no font available
                return len(text) * (font_size // 2)
        else:
            width, _ = font.measure(text)
            if font_size != font.size:
                scale = font_size / font.size
                width = int(width * scale)
            return width


# Global text manager
_text_manager = TextManager()


# Public API functions
def draw_text(text: str, x: int, y: int, font_size: int, color: Color) -> None:
    """Draw text using default font"""
    _text_manager.draw_text(text, x, y, font_size, color)


def draw_text_ex(font: Font, text: str, position: Tuple[int, int], 
                 font_size: float, spacing: float, color: Color) -> None:
    """Draw text with extended parameters"""
    _text_manager.draw_text_ex(font, text, position, font_size, spacing, color)


def measure_text(text: str, font_size: int) -> int:
    """Measure string width for default font"""
    return _text_manager.measure_text(text, font_size)


def measure_text_ex(font: Font, text: str, font_size: float, spacing: float) -> Tuple[int, int]:
    """Measure string size with extended parameters"""
    width, height = font.measure(text)
    if font_size != font.size:
        scale = font_size / font.size
        width = int(width * scale)
        height = int(height * scale)
    return (width, height)


def load_font(filename: str, size: int = 32) -> Font:
    """Load font from file"""
    return _text_manager.load_font(filename, size)


def load_font_from_memory(font_data: bytes, size: int = 32) -> Font:
    """Load font from memory"""
    return _text_manager.load_font_from_memory(font_data, size)


def unload_font(font: Font) -> None:
    """Unload font from memory"""
    _text_manager.unload_font(font)


def get_default_font() -> Optional[Font]:
    """Get default font"""
    return _text_manager.default_font
