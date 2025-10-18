"""
PyRay Bridges Module
Integration adapters for external libraries
"""

# Optional imports based on installed extras
try:
    from pyray.bridges import opencv
except ImportError:
    opencv = None

try:
    from pyray.bridges import matplotlib
except ImportError:
    matplotlib = None

try:
    from pyray.bridges import open3d
except ImportError:
    open3d = None

try:
    from pyray.bridges import pyvista
except ImportError:
    pyvista = None

try:
    from pyray.bridges import arcade
except ImportError:
    arcade = None

__all__ = ["opencv", "matplotlib", "open3d", "pyvista", "arcade"]
