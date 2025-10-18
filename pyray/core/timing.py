"""
Timing module for PyRay
Handles frame rate control and time management
"""

import pygame
import time
from pyray.core.config import Config


class TimingManager:
    """Manages timing and frame rate"""
    
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.target_fps = 60
        self.current_fps = 0
        self.frame_time = 0.0
        self.total_time = 0.0
        self.start_time = time.time()
        
    def set_target_fps(self, fps: int) -> None:
        """Set target frames per second"""
        self.target_fps = fps
        Config.instance().target_fps = fps
        
    def tick(self) -> None:
        """Update timing (call once per frame)"""
        # Limit frame rate and get frame time in milliseconds
        self.frame_time = self.clock.tick(self.target_fps) / 1000.0
        self.current_fps = self.clock.get_fps()
        self.total_time = time.time() - self.start_time
        
    def get_fps(self) -> int:
        """Get current frames per second"""
        return int(self.current_fps)
        
    def get_frame_time(self) -> float:
        """Get time in seconds for last frame"""
        return self.frame_time
        
    def get_time(self) -> float:
        """Get elapsed time in seconds since init"""
        return self.total_time


# Global timing manager instance
_timing_manager = TimingManager()


# Public API functions
def set_target_fps(fps: int) -> None:
    """Set target FPS (frames per second)"""
    _timing_manager.set_target_fps(fps)


def get_fps() -> int:
    """Get current FPS (frames per second)"""
    return _timing_manager.get_fps()


def get_frame_time() -> float:
    """Get time in seconds for last frame"""
    return _timing_manager.get_frame_time()


def get_time() -> float:
    """Get elapsed time in seconds since window creation"""
    return _timing_manager.get_time()


def tick() -> None:
    """Update timing (internal use)"""
    _timing_manager.tick()
