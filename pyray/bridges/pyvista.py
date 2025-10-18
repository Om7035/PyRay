"""
PyVista Bridge for PyRay
Provides integration with PyVista for 3D visualization and mesh processing
"""

import numpy as np
from typing import Optional, Tuple, Any, List
from pyray.graphics.texture import Texture
import pygame
import io

try:
    import pyvista as pv
    HAS_PYVISTA = True
except ImportError:
    HAS_PYVISTA = False
    pv = None


class PyVistaRenderer:
    """Manages PyVista rendering to PyRay textures"""
    
    def __init__(self, width: int = 640, height: int = 480):
        if not HAS_PYVISTA:
            raise ImportError("PyVista is required. Install with: pip install pyray[pyvista]")
        
        self.width = width
        self.height = height
        
        # Create offscreen plotter
        self.plotter = pv.Plotter(
            off_screen=True,
            window_size=[width, height]
        )
        
        # Setup default scene
        self.setup_default_scene()
        
    def setup_default_scene(self):
        """Setup default lighting and camera"""
        self.plotter.set_background('black')
        self.plotter.add_light(pv.Light(position=(5, 5, 5), intensity=1.0))
        
    def add_mesh(self, mesh: Any, color: str = 'white', 
                 opacity: float = 1.0, style: str = 'surface',
                 name: Optional[str] = None) -> Any:
        """Add a mesh to the scene
        
        Args:
            mesh: PyVista mesh object
            color: Mesh color
            opacity: Mesh opacity (0-1)
            style: Rendering style ('surface', 'wireframe', 'points')
            name: Optional name for the mesh
            
        Returns:
            Actor object
        """
        return self.plotter.add_mesh(
            mesh,
            color=color,
            opacity=opacity,
            style=style,
            name=name
        )
        
    def add_points(self, points: np.ndarray, color: str = 'white',
                   point_size: float = 5.0, name: Optional[str] = None) -> Any:
        """Add points to the scene
        
        Args:
            points: Nx3 array of points
            color: Point color
            point_size: Size of points
            name: Optional name
            
        Returns:
            Actor object
        """
        point_cloud = pv.PolyData(points)
        return self.plotter.add_mesh(
            point_cloud,
            color=color,
            point_size=point_size,
            style='points',
            name=name
        )
        
    def add_arrows(self, start: np.ndarray, direction: np.ndarray,
                   mag: float = 1.0, color: str = 'white') -> Any:
        """Add arrows to the scene
        
        Args:
            start: Starting points
            direction: Arrow directions
            mag: Magnitude/length
            color: Arrow color
            
        Returns:
            Actor object
        """
        return self.plotter.add_arrows(start, direction, mag, color=color)
        
    def add_text(self, text: str, position: str = 'upper_left',
                font_size: int = 18, color: str = 'white') -> Any:
        """Add text to the scene
        
        Args:
            text: Text to display
            position: Position on screen
            font_size: Font size
            color: Text color
            
        Returns:
            Actor object
        """
        return self.plotter.add_text(text, position=position, 
                                    font_size=font_size, color=color)
        
    def set_camera(self, position: Tuple[float, float, float],
                   focal_point: Tuple[float, float, float] = (0, 0, 0),
                   viewup: Tuple[float, float, float] = (0, 1, 0)):
        """Set camera position and orientation"""
        self.plotter.camera_position = [position, focal_point, viewup]
        
    def clear(self):
        """Clear all actors from the scene"""
        self.plotter.clear()
        
    def render_to_texture(self) -> Texture:
        """Render the scene and return as PyRay texture"""
        # Render to image
        self.plotter.show(auto_close=False)
        img = self.plotter.screenshot(return_img=True)
        
        # Convert to pygame surface
        # PyVista returns RGB array
        surface = pygame.surfarray.make_surface(np.transpose(img, (1, 0, 2)))
        
        return Texture(surface, "pyvista_render")
        
    def render_to_array(self) -> np.ndarray:
        """Render the scene and return as numpy array"""
        self.plotter.show(auto_close=False)
        return self.plotter.screenshot(return_img=True)
        
    def close(self):
        """Close the plotter"""
        self.plotter.close()


def load_mesh(filename: str) -> Any:
    """Load a mesh from file
    
    Args:
        filename: Path to mesh file (.vtk, .stl, .obj, .ply, etc.)
        
    Returns:
        PyVista mesh object
    """
    if not HAS_PYVISTA:
        raise ImportError("PyVista is required")
    
    return pv.read(filename)


def save_mesh(mesh: Any, filename: str):
    """Save a mesh to file
    
    Args:
        mesh: PyVista mesh object
        filename: Output filename
    """
    if not HAS_PYVISTA:
        raise ImportError("PyVista is required")
    
    mesh.save(filename)


def create_sphere(radius: float = 0.5, center: Tuple[float, float, float] = (0, 0, 0),
                 theta_resolution: int = 30, phi_resolution: int = 30) -> Any:
    """Create a sphere mesh
    
    Args:
        radius: Sphere radius
        center: Center position
        theta_resolution: Horizontal resolution
        phi_resolution: Vertical resolution
        
    Returns:
        PyVista Sphere mesh
    """
    if not HAS_PYVISTA:
        raise ImportError("PyVista is required")
    
    return pv.Sphere(radius=radius, center=center,
                    theta_resolution=theta_resolution,
                    phi_resolution=phi_resolution)


def create_box(bounds: Tuple[float, float, float, float, float, float] = 
               (-1, 1, -1, 1, -1, 1)) -> Any:
    """Create a box mesh
    
    Args:
        bounds: (xmin, xmax, ymin, ymax, zmin, zmax)
        
    Returns:
        PyVista Box mesh
    """
    if not HAS_PYVISTA:
        raise ImportError("PyVista is required")
    
    return pv.Box(bounds)


def create_cylinder(center: Tuple[float, float, float] = (0, 0, 0),
                   direction: Tuple[float, float, float] = (1, 0, 0),
                   radius: float = 0.5, height: float = 1.0,
                   resolution: int = 30) -> Any:
    """Create a cylinder mesh
    
    Args:
        center: Center position
        direction: Cylinder axis direction
        radius: Cylinder radius
        height: Cylinder height
        resolution: Circular resolution
        
    Returns:
        PyVista Cylinder mesh
    """
    if not HAS_PYVISTA:
        raise ImportError("PyVista is required")
    
    return pv.Cylinder(center=center, direction=direction,
                       radius=radius, height=height,
                       resolution=resolution)


def create_arrow(start: Tuple[float, float, float] = (0, 0, 0),
                direction: Tuple[float, float, float] = (1, 0, 0),
                tip_length: float = 0.25, tip_radius: float = 0.1,
                shaft_radius: float = 0.05, scale: float = 1.0) -> Any:
    """Create an arrow mesh
    
    Args:
        start: Starting position
        direction: Arrow direction
        tip_length: Length of arrow tip
        tip_radius: Radius of arrow tip
        shaft_radius: Radius of arrow shaft
        scale: Overall scale
        
    Returns:
        PyVista Arrow mesh
    """
    if not HAS_PYVISTA:
        raise ImportError("PyVista is required")
    
    return pv.Arrow(start=start, direction=direction,
                   tip_length=tip_length, tip_radius=tip_radius,
                   shaft_radius=shaft_radius, scale=scale)


def create_plane(center: Tuple[float, float, float] = (0, 0, 0),
                direction: Tuple[float, float, float] = (0, 0, 1),
                i_size: float = 1, j_size: float = 1,
                i_resolution: int = 10, j_resolution: int = 10) -> Any:
    """Create a plane mesh
    
    Args:
        center: Center position
        direction: Normal direction
        i_size: Size in i direction
        j_size: Size in j direction
        i_resolution: Resolution in i direction
        j_resolution: Resolution in j direction
        
    Returns:
        PyVista Plane mesh
    """
    if not HAS_PYVISTA:
        raise ImportError("PyVista is required")
    
    return pv.Plane(center=center, direction=direction,
                   i_size=i_size, j_size=j_size,
                   i_resolution=i_resolution, j_resolution=j_resolution)


def create_text_3d(text: str, depth: float = 0.5) -> Any:
    """Create 3D text mesh
    
    Args:
        text: Text string
        depth: Extrusion depth
        
    Returns:
        PyVista Text3D mesh
    """
    if not HAS_PYVISTA:
        raise ImportError("PyVista is required")
    
    return pv.Text3D(text, depth=depth)


def apply_filter(mesh: Any, filter_type: str = 'smooth', **kwargs) -> Any:
    """Apply a filter to a mesh
    
    Args:
        mesh: PyVista mesh object
        filter_type: Type of filter
        **kwargs: Filter-specific parameters
        
    Returns:
        Filtered mesh
    """
    if not HAS_PYVISTA:
        raise ImportError("PyVista is required")
    
    if filter_type == 'smooth':
        return mesh.smooth(**kwargs)
    elif filter_type == 'decimate':
        return mesh.decimate(**kwargs)
    elif filter_type == 'subdivide':
        return mesh.subdivide(**kwargs)
    elif filter_type == 'clean':
        return mesh.clean(**kwargs)
    else:
        raise ValueError(f"Unknown filter type: {filter_type}")


def compute_normals(mesh: Any, cell_normals: bool = True,
                   point_normals: bool = True) -> Any:
    """Compute normals for a mesh
    
    Args:
        mesh: PyVista mesh object
        cell_normals: Compute cell normals
        point_normals: Compute point normals
        
    Returns:
        Mesh with computed normals
    """
    if not HAS_PYVISTA:
        raise ImportError("PyVista is required")
    
    return mesh.compute_normals(cell_normals=cell_normals,
                               point_normals=point_normals)


def slice_mesh(mesh: Any, normal: Tuple[float, float, float] = (1, 0, 0),
              origin: Tuple[float, float, float] = (0, 0, 0)) -> Any:
    """Slice a mesh with a plane
    
    Args:
        mesh: PyVista mesh object
        normal: Plane normal
        origin: Plane origin
        
    Returns:
        Sliced mesh
    """
    if not HAS_PYVISTA:
        raise ImportError("PyVista is required")
    
    return mesh.slice(normal=normal, origin=origin)


def create_volume_render(volume_data: np.ndarray, spacing: Tuple[float, float, float] = (1, 1, 1),
                        origin: Tuple[float, float, float] = (0, 0, 0)) -> Any:
    """Create a volume from 3D array data
    
    Args:
        volume_data: 3D numpy array
        spacing: Voxel spacing
        origin: Volume origin
        
    Returns:
        PyVista ImageData object
    """
    if not HAS_PYVISTA:
        raise ImportError("PyVista is required")
    
    grid = pv.ImageData()
    grid.dimensions = volume_data.shape
    grid.spacing = spacing
    grid.origin = origin
    grid.point_data["values"] = volume_data.flatten(order="F")
    
    return grid


def create_streamlines(mesh: Any, vectors: str, start_position: Tuple[float, float, float],
                      max_time: float = 1000.0, n_points: int = 1000) -> Any:
    """Create streamlines from vector field
    
    Args:
        mesh: PyVista mesh with vector data
        vectors: Name of vector array
        start_position: Starting position for streamline
        max_time: Maximum integration time
        n_points: Number of points in streamline
        
    Returns:
        Streamline mesh
    """
    if not HAS_PYVISTA:
        raise ImportError("PyVista is required")
    
    return mesh.streamlines(
        vectors=vectors,
        start_position=start_position,
        max_time=max_time,
        n_points=n_points
    )


# Example usage function
def create_3d_scene_example() -> PyVistaRenderer:
    """Create an example 3D scene with PyVista
    
    Returns:
        Configured PyVistaRenderer
    """
    if not HAS_PYVISTA:
        raise ImportError("PyVista is required")
    
    renderer = PyVistaRenderer(800, 600)
    
    # Create some geometry
    sphere = create_sphere(radius=0.5)
    renderer.add_mesh(sphere, color='red', opacity=0.8)
    
    box = create_box(bounds=(-1, 1, -1, 1, -1, 1))
    box.translate([3, 0, 0])
    renderer.add_mesh(box, color='green', style='wireframe')
    
    cylinder = create_cylinder(center=(-3, 0, 0), height=2.0)
    renderer.add_mesh(cylinder, color='blue')
    
    # Add some text
    text_3d = create_text_3d("PyVista", depth=0.2)
    text_3d.translate([0, 2, 0])
    renderer.add_mesh(text_3d, color='yellow')
    
    # Add axes
    axes = pv.Axes()
    renderer.add_mesh(axes.shaft, color='white')
    
    # Set camera
    renderer.set_camera(position=(5, 5, 5), focal_point=(0, 0, 0))
    
    return renderer


def create_scientific_visualization_example(data: np.ndarray) -> PyVistaRenderer:
    """Create a scientific visualization example
    
    Args:
        data: 3D numpy array of scalar data
        
    Returns:
        Configured PyVistaRenderer with volume rendering
    """
    if not HAS_PYVISTA:
        raise ImportError("PyVista is required")
    
    renderer = PyVistaRenderer(800, 600)
    
    # Create volume
    volume = create_volume_render(data)
    
    # Add volume with opacity mapping
    renderer.plotter.add_volume(
        volume,
        cmap='viridis',
        opacity='sigmoid',
        shade=True
    )
    
    # Add outline
    outline = volume.outline()
    renderer.add_mesh(outline, color='white')
    
    # Add scalar bar
    renderer.plotter.add_scalar_bar()
    
    return renderer
