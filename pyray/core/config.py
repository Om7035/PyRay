"""
Configuration module for PyRay
Manages global configuration and settings
"""

from typing import Optional


class Config:
    """Singleton configuration manager"""
    
    _instance: Optional['Config'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize configuration settings"""
        self.window_initialized = False
        self.audio_initialized = False
        self.target_fps = 60
        self.vsync_enabled = True
        self.debug_mode = False
        self.backend = "pygame"  # Default backend
        
    @classmethod
    def instance(cls) -> 'Config':
        """Get the singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def reset(self):
        """Reset configuration to defaults"""
        self._initialize()
