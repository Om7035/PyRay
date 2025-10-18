"""
PyRay Backends Module
Alternative rendering backends for advanced features
"""

from pyray.backends.backend_base import Backend, BackendType

# Import available backends
try:
    from pyray.backends.pygame_backend import PygameBackend
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False
    PygameBackend = None

try:
    from pyray.backends.moderngl_backend import ModernGLBackend
    HAS_MODERNGL = True
except ImportError:
    HAS_MODERNGL = False
    ModernGLBackend = None

try:
    from pyray.backends.pyglet_backend import PygletBackend
    HAS_PYGLET = True
except ImportError:
    HAS_PYGLET = False
    PygletBackend = None

def get_backend(backend_type: BackendType = BackendType.PYGAME):
    """Get the appropriate backend based on type"""
    if backend_type == BackendType.PYGAME:
        if not HAS_PYGAME:
            raise ImportError("Pygame backend not available")
        return PygameBackend()
    elif backend_type == BackendType.MODERNGL:
        if not HAS_MODERNGL:
            raise ImportError("ModernGL backend not available. Install with: pip install pyray[moderngl]")
        return ModernGLBackend()
    elif backend_type == BackendType.PYGLET:
        if not HAS_PYGLET:
            raise ImportError("Pyglet backend not available. Install with: pip install pyray[pyglet]")
        return PygletBackend()
    else:
        raise ValueError(f"Unknown backend type: {backend_type}")

__all__ = ["Backend", "BackendType", "get_backend", "PygameBackend", "ModernGLBackend", "PygletBackend"]
