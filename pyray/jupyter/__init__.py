"""
PyRay Jupyter Integration
Utilities for using PyRay in Jupyter notebooks
"""

from pyray.jupyter.capture import (
    capture_frame,
    record_gif,
    record_video,
    display_frame,
    create_notebook_window,
    NotebookRenderer,
)

__all__ = [
    "capture_frame",
    "record_gif", 
    "record_video",
    "display_frame",
    "create_notebook_window",
    "NotebookRenderer",
]
