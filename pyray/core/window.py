"""
Window management module for PyRay
Handles window creation, properties, and state
"""

import pygame
import sys
from typing import Optional, Tuple
from pyray.core.config import Config


class WindowManager:
    """Manages the game window and its properties"""
    
    def __init__(self):
        self.screen: Optional[pygame.Surface] = None
        self.width: int = 800
        self.height: int = 600
        self.title: str = "PyRay Window"
        self.is_ready: bool = False
        self.should_close: bool = False
        self.is_fullscreen: bool = False
        self.is_hidden: bool = False
        self.is_minimized: bool = False
        self.is_maximized: bool = False
        self.is_focused: bool = True
        self.is_resized: bool = False
        self.min_width: int = 120
        self.min_height: int = 120
        self.max_width: int = 0  # 0 means no limit
        self.max_height: int = 0
        self.screen_width: int = 0
        self.screen_height: int = 0
        
    def init(self, width: int, height: int, title: str) -> None:
        """Initialize the window"""
        pygame.init()
        
        # Get screen dimensions
        info = pygame.display.Info()
        self.screen_width = info.current_w
        self.screen_height = info.current_h
        
        # Set window properties
        self.width = width
        self.height = height
        self.title = title
        
        # Create the window
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.screen = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption(title)
        
        self.is_ready = True
        self.should_close = False
        
    def close(self) -> None:
        """Close the window and cleanup"""
        if self.is_ready:
            pygame.quit()
            self.is_ready = False
            self.screen = None
            
    def check_should_close(self) -> bool:
        """Check if window should close"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.should_close = True
            elif event.type == pygame.VIDEORESIZE:
                self.is_resized = True
                self.width = event.w
                self.height = event.h
            elif event.type == pygame.ACTIVEEVENT:
                if event.state == 1:  # Mouse focus
                    self.is_focused = event.gain == 1
                elif event.state == 2:  # Input focus
                    self.is_focused = event.gain == 1
                elif event.state == 6:  # Minimized
                    self.is_minimized = event.gain == 0
                    
        return self.should_close
        
    def set_title(self, title: str) -> None:
        """Set window title"""
        self.title = title
        if self.is_ready:
            pygame.display.set_caption(title)
            
    def set_position(self, x: int, y: int) -> None:
        """Set window position on screen"""
        if self.is_ready:
            # Note: pygame doesn't have direct window positioning
            # This would require platform-specific code
            pass
            
    def set_size(self, width: int, height: int) -> None:
        """Set window size"""
        if self.max_width > 0:
            width = min(width, self.max_width)
        width = max(width, self.min_width)
        
        if self.max_height > 0:
            height = min(height, self.max_height)
        height = max(height, self.min_height)
        
        self.width = width
        self.height = height
        
        if self.is_ready:
            flags = pygame.DOUBLEBUF | pygame.HWSURFACE
            if self.is_fullscreen:
                flags |= pygame.FULLSCREEN
            self.screen = pygame.display.set_mode((width, height), flags)
            
    def toggle_fullscreen(self) -> None:
        """Toggle fullscreen mode"""
        if not self.is_ready:
            return
            
        self.is_fullscreen = not self.is_fullscreen
        
        if self.is_fullscreen:
            flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
            self.screen = pygame.display.set_mode((0, 0), flags)
            # Update dimensions to fullscreen size
            info = pygame.display.Info()
            self.width = info.current_w
            self.height = info.current_h
        else:
            flags = pygame.DOUBLEBUF | pygame.HWSURFACE
            self.screen = pygame.display.set_mode((self.width, self.height), flags)


# Global window manager instance
_window_manager = WindowManager()


# Public API functions
def init_window(width: int, height: int, title: str) -> None:
    """Initialize window with specified width, height and title"""
    _window_manager.init(width, height, title)
    Config.instance().window_initialized = True


def close_window() -> None:
    """Close window and free resources"""
    _window_manager.close()
    Config.instance().window_initialized = False


def window_should_close() -> bool:
    """Check if window should close (user pressed close button)"""
    return _window_manager.check_should_close()


def is_window_ready() -> bool:
    """Check if window has been initialized successfully"""
    return _window_manager.is_ready


def is_window_fullscreen() -> bool:
    """Check if window is in fullscreen mode"""
    return _window_manager.is_fullscreen


def is_window_hidden() -> bool:
    """Check if window is hidden"""
    return _window_manager.is_hidden


def is_window_minimized() -> bool:
    """Check if window is minimized"""
    return _window_manager.is_minimized


def is_window_maximized() -> bool:
    """Check if window is maximized"""
    return _window_manager.is_maximized


def is_window_focused() -> bool:
    """Check if window is focused"""
    return _window_manager.is_focused


def is_window_resized() -> bool:
    """Check if window has been resized"""
    result = _window_manager.is_resized
    _window_manager.is_resized = False  # Reset flag after checking
    return result


def set_window_title(title: str) -> None:
    """Set window title"""
    _window_manager.set_title(title)


def set_window_position(x: int, y: int) -> None:
    """Set window position on screen"""
    _window_manager.set_position(x, y)


def set_window_size(width: int, height: int) -> None:
    """Set window size"""
    _window_manager.set_size(width, height)


def set_window_min_size(width: int, height: int) -> None:
    """Set window minimum size"""
    _window_manager.min_width = width
    _window_manager.min_height = height


def set_window_max_size(width: int, height: int) -> None:
    """Set window maximum size"""
    _window_manager.max_width = width
    _window_manager.max_height = height


def get_window_width() -> int:
    """Get current window width"""
    return _window_manager.width


def get_window_height() -> int:
    """Get current window height"""
    return _window_manager.height


def get_screen_width() -> int:
    """Get current screen width"""
    return _window_manager.screen_width


def get_screen_height() -> int:
    """Get current screen height"""
    return _window_manager.screen_height


def toggle_fullscreen() -> None:
    """Toggle fullscreen mode"""
    _window_manager.toggle_fullscreen()


def get_window_handle() -> Optional[pygame.Surface]:
    """Get the pygame screen surface (internal use)"""
    return _window_manager.screen
