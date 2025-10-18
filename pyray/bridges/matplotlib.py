"""
Matplotlib Bridge for PyRay
Provides integration between Matplotlib and PyRay for data visualization in games
"""

import pygame
import numpy as np
from typing import Optional, Callable, Any, Tuple
from pyray.graphics.texture import Texture
import io

try:
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    matplotlib.use('Agg')  # Use non-interactive backend
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    plt = None


class LiveChart:
    """Manages a live-updating chart that can be rendered as a texture"""
    
    def __init__(self, update_fn: Callable, width: int = 400, height: int = 300, 
                 transparent: bool = False):
        """
        Create a live chart
        
        Args:
            update_fn: Function that updates the chart (receives fig, ax)
            width: Chart width in pixels
            height: Chart height in pixels
            transparent: Whether to use transparent background
        """
        if not HAS_MATPLOTLIB:
            raise ImportError("Matplotlib is required. Install with: pip install pyray[matplotlib]")
        
        self.update_fn = update_fn
        self.width = width
        self.height = height
        self.transparent = transparent
        
        # Create figure with specified size
        dpi = 100
        self.fig = plt.figure(figsize=(width/dpi, height/dpi), dpi=dpi)
        if transparent:
            self.fig.patch.set_alpha(0.0)
        
        self.ax = self.fig.add_subplot(111)
        if transparent:
            self.ax.patch.set_alpha(0.0)
        
        self.canvas = FigureCanvasAgg(self.fig)
        self.texture: Optional[Texture] = None
        
    def update(self) -> Texture:
        """Update the chart and return as texture"""
        # Clear the axes
        self.ax.clear()
        
        # Call update function
        self.update_fn(self.fig, self.ax)
        
        # Render to texture
        self.texture = figure_to_texture(self.fig, transparent=self.transparent)
        return self.texture
    
    def close(self):
        """Close the figure"""
        plt.close(self.fig)


def figure_to_texture(fig: Any, transparent: bool = False) -> Texture:
    """Convert a matplotlib figure to a PyRay texture
    
    Args:
        fig: Matplotlib figure
        transparent: Whether to preserve transparency
        
    Returns:
        PyRay Texture object
    """
    if not HAS_MATPLOTLIB:
        raise ImportError("Matplotlib is required. Install with: pip install pyray[matplotlib]")
    
    # Draw the figure
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    
    # Get the RGBA buffer from the figure
    buf = canvas.buffer_rgba()
    arr = np.frombuffer(buf, dtype=np.uint8)
    
    # Get dimensions
    w, h = canvas.get_width_height()
    
    # Reshape to (H, W, 4) for RGBA
    arr = arr.reshape((h, w, 4))
    
    if not transparent:
        # Convert RGBA to RGB by dropping alpha channel
        arr = arr[:, :, :3]
    
    # Create pygame surface
    if transparent:
        # Create RGBA surface
        surface = pygame.Surface((w, h), pygame.SRCALPHA)
        # pygame expects (W, H, 4) so we need to transpose
        arr_transposed = np.transpose(arr, (1, 0, 2))
        pygame.surfarray.pixels3d(surface)[:, :, :3] = arr_transposed[:, :, :3]
        pygame.surfarray.pixels_alpha(surface)[:] = arr_transposed[:, :, 3]
    else:
        # Create RGB surface
        arr_transposed = np.transpose(arr, (1, 0, 2))
        surface = pygame.surfarray.make_surface(arr_transposed)
    
    return Texture(surface, f"matplotlib_fig_{id(fig)}")


def figure_to_surface(fig: Any, transparent: bool = False) -> pygame.Surface:
    """Convert a matplotlib figure to a pygame Surface
    
    Args:
        fig: Matplotlib figure
        transparent: Whether to preserve transparency
        
    Returns:
        pygame Surface
    """
    texture = figure_to_texture(fig, transparent)
    return texture.surface


def live_chart_overlay(update_fn: Callable, width: int = 400, 
                      height: int = 300, transparent: bool = True) -> LiveChart:
    """Create a live-updating chart overlay
    
    Args:
        update_fn: Function that updates the chart (receives fig, ax)
        width: Chart width in pixels
        height: Chart height in pixels
        transparent: Whether to use transparent background
        
    Returns:
        LiveChart object
        
    Example:
        def update_fps(fig, ax):
            ax.plot(fps_history[-60:])
            ax.set_ylim(0, 70)
            ax.set_title("FPS")
            
        chart = live_chart_overlay(update_fps, 200, 150)
        
        # In game loop:
        texture = chart.update()
        pyray.draw_texture(texture, 10, 10)
    """
    return LiveChart(update_fn, width, height, transparent)


# Pre-built chart helpers
def create_fps_chart(history_size: int = 60) -> LiveChart:
    """Create a pre-configured FPS chart
    
    Args:
        history_size: Number of frames to show in history
        
    Returns:
        LiveChart configured for FPS display
    """
    fps_history = []
    
    def update_fps(fig, ax):
        import pyray
        current_fps = pyray.get_fps()
        fps_history.append(current_fps)
        if len(fps_history) > history_size:
            fps_history.pop(0)
        
        ax.plot(fps_history, 'g-', linewidth=2)
        ax.set_ylim(0, 70)
        ax.set_xlim(0, history_size)
        ax.set_title("FPS", fontsize=10)
        ax.set_ylabel("FPS", fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.set_facecolor('#00000000')  # Transparent background
    
    return LiveChart(update_fps, 200, 150, transparent=True)


def create_performance_chart() -> LiveChart:
    """Create a multi-metric performance chart
    
    Returns:
        LiveChart configured for performance metrics
    """
    frame_times = []
    draw_calls = []
    
    def update_perf(fig, ax):
        import pyray
        import time
        
        # Simulate metrics (replace with actual in production)
        frame_time = pyray.get_frame_time() * 1000  # Convert to ms
        frame_times.append(frame_time)
        if len(frame_times) > 60:
            frame_times.pop(0)
        
        # Plot frame time
        ax.plot(frame_times, 'b-', label='Frame Time (ms)', linewidth=1)
        ax.set_ylim(0, 50)
        ax.set_xlim(0, 60)
        ax.set_title("Performance", fontsize=10)
        ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.set_facecolor('#00000000')
    
    return LiveChart(update_perf, 250, 150, transparent=True)


def create_histogram(data_fn: Callable, bins: int = 20, 
                     title: str = "Histogram") -> LiveChart:
    """Create a live-updating histogram
    
    Args:
        data_fn: Function that returns the data to plot
        bins: Number of histogram bins
        title: Chart title
        
    Returns:
        LiveChart configured as histogram
    """
    def update_hist(fig, ax):
        data = data_fn()
        if data is not None and len(data) > 0:
            ax.hist(data, bins=bins, alpha=0.7, color='blue', edgecolor='black')
            ax.set_title(title, fontsize=10)
            ax.grid(True, alpha=0.3)
            ax.set_facecolor('#00000000')
    
    return LiveChart(update_hist, 300, 200, transparent=True)


def create_scatter_plot(x_fn: Callable, y_fn: Callable, 
                       title: str = "Scatter Plot") -> LiveChart:
    """Create a live-updating scatter plot
    
    Args:
        x_fn: Function that returns x data
        y_fn: Function that returns y data
        title: Chart title
        
    Returns:
        LiveChart configured as scatter plot
    """
    def update_scatter(fig, ax):
        x_data = x_fn()
        y_data = y_fn()
        if x_data is not None and y_data is not None:
            ax.scatter(x_data, y_data, alpha=0.6, s=20)
            ax.set_title(title, fontsize=10)
            ax.grid(True, alpha=0.3)
            ax.set_facecolor('#00000000')
    
    return LiveChart(update_scatter, 300, 200, transparent=True)


def save_figure_to_file(fig: Any, filename: str, dpi: int = 100):
    """Save a matplotlib figure to a file
    
    Args:
        fig: Matplotlib figure
        filename: Output filename
        dpi: Dots per inch for output
    """
    if not HAS_MATPLOTLIB:
        raise ImportError("Matplotlib is required")
    
    fig.savefig(filename, dpi=dpi, bbox_inches='tight')
