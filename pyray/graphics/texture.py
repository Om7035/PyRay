"""
Texture and image handling module for PyRay
Manages loading, unloading, and drawing of textures/sprites
"""

import pygame
from typing import Optional, Dict, Tuple
from PIL import Image as PILImage
import io
from pyray.core.window import get_window_handle
from pyray.colors import Color
from pyray.math import Vector2


class Texture:
    """Represents a loaded texture/image"""
    
    def __init__(self, surface: pygame.Surface, filename: Optional[str] = None):
        self.surface = surface
        self.filename = filename
        self.width = surface.get_width()
        self.height = surface.get_height()
        self.format = surface.get_format()
        
    def get_data(self) -> bytes:
        """Get raw pixel data"""
        return pygame.image.tostring(self.surface, 'RGBA')
        
    def set_filter(self, filter_mode: int) -> None:
        """Set texture filter mode (for scaling)"""
        # In pygame, this is handled during scaling operations
        pass


class Image:
    """Represents an image in memory (not GPU texture)"""
    
    def __init__(self, data: PILImage.Image):
        self.data = data
        self.width = data.width
        self.height = data.height
        
    def to_texture(self) -> Texture:
        """Convert image to texture"""
        # Convert PIL image to pygame surface
        mode = self.data.mode
        size = self.data.size
        data_bytes = self.data.tobytes()
        
        if mode == 'RGBA':
            surface = pygame.image.fromstring(data_bytes, size, mode)
        elif mode == 'RGB':
            surface = pygame.image.fromstring(data_bytes, size, mode)
        else:
            # Convert to RGBA
            rgba_image = self.data.convert('RGBA')
            data_bytes = rgba_image.tobytes()
            surface = pygame.image.fromstring(data_bytes, size, 'RGBA')
            
        return Texture(surface)


class TextureManager:
    """Manages texture loading and caching"""
    
    def __init__(self):
        self.textures: Dict[str, Texture] = {}
        
    def load_image(self, filename: str) -> Image:
        """Load image from file (CPU memory)"""
        try:
            pil_image = PILImage.open(filename)
            return Image(pil_image)
        except Exception as e:
            print(f"Error loading image {filename}: {e}")
            # Return a default 1x1 white image
            default_image = PILImage.new('RGBA', (1, 1), (255, 255, 255, 255))
            return Image(default_image)
            
    def load_texture(self, filename: str) -> Texture:
        """Load texture from file (GPU memory)"""
        # Check cache first
        if filename in self.textures:
            return self.textures[filename]
            
        try:
            # Load with pygame directly for better performance
            surface = pygame.image.load(filename).convert_alpha()
            texture = Texture(surface, filename)
            self.textures[filename] = texture
            return texture
        except Exception as e:
            print(f"Error loading texture {filename}: {e}")
            # Return a default 1x1 white texture
            surface = pygame.Surface((1, 1), pygame.SRCALPHA)
            surface.fill((255, 255, 255, 255))
            return Texture(surface)
            
    def load_texture_from_image(self, image: Image) -> Texture:
        """Create texture from image"""
        return image.to_texture()
        
    def unload_texture(self, texture: Texture) -> None:
        """Unload texture from memory"""
        # Remove from cache if present
        if texture.filename and texture.filename in self.textures:
            del self.textures[texture.filename]
            
        # pygame surfaces are garbage collected automatically
        texture.surface = None
        
    def draw_texture(self, texture: Texture, x: int, y: int, tint: Color) -> None:
        """Draw texture at position with tint color"""
        screen = get_window_handle()
        if not screen or not texture.surface:
            return
            
        # Apply tint if not white
        if tint != Color(255, 255, 255, 255):
            tinted_surface = texture.surface.copy()
            tinted_surface.fill((tint.r, tint.g, tint.b, tint.a), 
                              special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(tinted_surface, (x, y))
        else:
            screen.blit(texture.surface, (x, y))
            
    def draw_texture_ex(self, texture: Texture, position: Vector2, 
                       rotation: float, scale: float, tint: Color) -> None:
        """Draw texture with extended parameters"""
        screen = get_window_handle()
        if not screen or not texture.surface:
            return
            
        # Apply transformations
        transformed = texture.surface
        
        # Scale
        if scale != 1.0:
            new_width = int(texture.width * scale)
            new_height = int(texture.height * scale)
            transformed = pygame.transform.scale(transformed, (new_width, new_height))
            
        # Rotate
        if rotation != 0:
            transformed = pygame.transform.rotate(transformed, -rotation)  # Negative for correct direction
            
        # Apply tint
        if tint != Color(255, 255, 255, 255):
            transformed = transformed.copy()
            transformed.fill((tint.r, tint.g, tint.b, tint.a), 
                           special_flags=pygame.BLEND_RGBA_MULT)
            
        # Draw at position (accounting for rotation center)
        rect = transformed.get_rect(center=(position.x, position.y))
        screen.blit(transformed, rect)
        
    def draw_texture_rect(self, texture: Texture, source: Tuple[int, int, int, int],
                         dest: Tuple[int, int, int, int], origin: Vector2,
                         rotation: float, tint: Color) -> None:
        """Draw part of a texture (texture atlas)"""
        screen = get_window_handle()
        if not screen or not texture.surface:
            return
            
        # Extract the source rectangle from texture
        source_rect = pygame.Rect(source)
        subsurface = texture.surface.subsurface(source_rect)
        
        # Scale to destination size if different
        dest_rect = pygame.Rect(dest)
        if dest_rect.width != source_rect.width or dest_rect.height != source_rect.height:
            subsurface = pygame.transform.scale(subsurface, (dest_rect.width, dest_rect.height))
            
        # Rotate if needed
        if rotation != 0:
            subsurface = pygame.transform.rotate(subsurface, -rotation)
            
        # Apply tint
        if tint != Color(255, 255, 255, 255):
            subsurface = subsurface.copy()
            subsurface.fill((tint.r, tint.g, tint.b, tint.a), 
                          special_flags=pygame.BLEND_RGBA_MULT)
            
        # Draw at destination
        if rotation != 0:
            # Account for rotation center
            rect = subsurface.get_rect(center=(dest_rect.x + origin.x, dest_rect.y + origin.y))
            screen.blit(subsurface, rect)
        else:
            screen.blit(subsurface, (dest_rect.x, dest_rect.y))


# Global texture manager
_texture_manager = TextureManager()


# Public API functions
def load_image(filename: str) -> Image:
    """Load image from file"""
    return _texture_manager.load_image(filename)


def load_texture(filename: str) -> Texture:
    """Load texture from file"""
    return _texture_manager.load_texture(filename)


def load_texture_from_image(image: Image) -> Texture:
    """Load texture from image"""
    return _texture_manager.load_texture_from_image(image)


def unload_texture(texture: Texture) -> None:
    """Unload texture from GPU memory"""
    _texture_manager.unload_texture(texture)


def draw_texture(texture: Texture, x: int, y: int, tint: Color = None) -> None:
    """Draw a texture"""
    if tint is None:
        tint = Color(255, 255, 255, 255)
    _texture_manager.draw_texture(texture, x, y, tint)


def draw_texture_ex(texture: Texture, position: Vector2, rotation: float, 
                   scale: float, tint: Color = None) -> None:
    """Draw a texture with extended parameters"""
    if tint is None:
        tint = Color(255, 255, 255, 255)
    _texture_manager.draw_texture_ex(texture, position, rotation, scale, tint)


def draw_texture_rect(texture: Texture, source: Tuple[int, int, int, int],
                     dest: Tuple[int, int, int, int], origin: Vector2,
                     rotation: float, tint: Color = None) -> None:
    """Draw part of a texture"""
    if tint is None:
        tint = Color(255, 255, 255, 255)
    _texture_manager.draw_texture_rect(texture, source, dest, origin, rotation, tint)
