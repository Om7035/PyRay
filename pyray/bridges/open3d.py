"""
Open3D Bridge for PyRay
Provides integration with Open3D for 3D data processing and visualization
"""

import numpy as np
from typing import Optional, Tuple, Any
from pyray.graphics.texture import Texture
import pygame

try:
    import open3d as o3d
    HAS_OPEN3D = True
except ImportError:
    HAS_OPEN3D = False
    o3d = None


class Open3DRenderer:
    """Manages Open3D rendering to PyRay textures"""
    
    def __init__(self, width: int = 640, height: int = 480):
        if not HAS_OPEN3D:
            raise ImportError("Open3D is required. Install with: pip install pyray[open3d]")
        
        self.width = width
        self.height = height
        
        # Create offscreen renderer
        self.renderer = o3d.visualization.rendering.OffscreenRenderer(width, height)
        
        # Setup default scene
        self.setup_default_scene()
        
    def setup_default_scene(self):
        """Setup default lighting and camera"""
        # Set background color
        self.renderer.scene.set_background([0.1, 0.1, 0.1, 1.0])
        
        # Add default lighting
        self.renderer.scene.scene.set_sun_light(
            [0.577, -0.577, -0.577],  # Direction
            [1.0, 1.0, 1.0],  # Color
            100000  # Intensity
        )
        self.renderer.scene.scene.enable_sun_light(True)
        
        # Setup camera
        center = [0, 0, 0]
        eye = [0, 0, 5]
        up = [0, 1, 0]
        self.renderer.setup_camera(60, center, eye, up)
        
    def add_geometry(self, name: str, geometry: Any, material: Optional[Any] = None):
        """Add geometry to the scene
        
        Args:
            name: Unique name for the geometry
            geometry: Open3D geometry object
            material: Optional material
        """
        if material is None:
            material = o3d.visualization.rendering.MaterialRecord()
            material.shader = "defaultLit"
            
        self.renderer.scene.add_geometry(name, geometry, material)
        
    def remove_geometry(self, name: str):
        """Remove geometry from the scene"""
        self.renderer.scene.remove_geometry(name)
        
    def clear_geometries(self):
        """Clear all geometries from the scene"""
        self.renderer.scene.clear_geometry()
        
    def set_camera(self, eye: Tuple[float, float, float],
                   center: Tuple[float, float, float] = (0, 0, 0),
                   up: Tuple[float, float, float] = (0, 1, 0),
                   fov: float = 60):
        """Set camera position and orientation"""
        self.renderer.setup_camera(fov, center, eye, up)
        
    def render_to_texture(self) -> Texture:
        """Render the scene and return as PyRay texture"""
        # Render to image
        img = self.renderer.render_to_image()
        
        # Convert to numpy array
        img_array = np.asarray(img)
        
        # Convert to pygame surface
        surface = pygame.surfarray.make_surface(np.transpose(img_array, (1, 0, 2)))
        
        return Texture(surface, "open3d_render")
        
    def render_to_array(self) -> np.ndarray:
        """Render the scene and return as numpy array"""
        img = self.renderer.render_to_image()
        return np.asarray(img)


def load_point_cloud(filename: str) -> Any:
    """Load a point cloud from file
    
    Args:
        filename: Path to point cloud file (.ply, .pcd, .xyz, etc.)
        
    Returns:
        Open3D PointCloud object
    """
    if not HAS_OPEN3D:
        raise ImportError("Open3D is required")
    
    return o3d.io.read_point_cloud(filename)


def load_mesh(filename: str) -> Any:
    """Load a mesh from file
    
    Args:
        filename: Path to mesh file (.obj, .stl, .ply, etc.)
        
    Returns:
        Open3D TriangleMesh object
    """
    if not HAS_OPEN3D:
        raise ImportError("Open3D is required")
    
    return o3d.io.read_triangle_mesh(filename)


def save_point_cloud(point_cloud: Any, filename: str) -> bool:
    """Save a point cloud to file
    
    Args:
        point_cloud: Open3D PointCloud object
        filename: Output filename
        
    Returns:
        True if successful
    """
    if not HAS_OPEN3D:
        raise ImportError("Open3D is required")
    
    return o3d.io.write_point_cloud(filename, point_cloud)


def save_mesh(mesh: Any, filename: str) -> bool:
    """Save a mesh to file
    
    Args:
        mesh: Open3D TriangleMesh object
        filename: Output filename
        
    Returns:
        True if successful
    """
    if not HAS_OPEN3D:
        raise ImportError("Open3D is required")
    
    return o3d.io.write_triangle_mesh(filename, mesh)


def create_point_cloud_from_depth(depth_image: np.ndarray,
                                 intrinsic: Optional[Any] = None,
                                 extrinsic: Optional[np.ndarray] = None) -> Any:
    """Create a point cloud from a depth image
    
    Args:
        depth_image: Depth image as numpy array
        intrinsic: Camera intrinsic parameters
        extrinsic: Camera extrinsic parameters
        
    Returns:
        Open3D PointCloud object
    """
    if not HAS_OPEN3D:
        raise ImportError("Open3D is required")
    
    # Convert to Open3D image
    depth = o3d.geometry.Image(depth_image.astype(np.float32))
    
    # Use default intrinsic if not provided
    if intrinsic is None:
        height, width = depth_image.shape
        fx = fy = width
        cx = width / 2
        cy = height / 2
        intrinsic = o3d.camera.PinholeCameraIntrinsic(width, height, fx, fy, cx, cy)
    
    # Create point cloud
    pcd = o3d.geometry.PointCloud.create_from_depth_image(
        depth, intrinsic, extrinsic if extrinsic is not None else np.eye(4)
    )
    
    return pcd


def create_mesh_sphere(radius: float = 1.0, resolution: int = 20) -> Any:
    """Create a sphere mesh
    
    Args:
        radius: Sphere radius
        resolution: Mesh resolution
        
    Returns:
        Open3D TriangleMesh object
    """
    if not HAS_OPEN3D:
        raise ImportError("Open3D is required")
    
    return o3d.geometry.TriangleMesh.create_sphere(radius, resolution)


def create_mesh_box(width: float = 1.0, height: float = 1.0, depth: float = 1.0) -> Any:
    """Create a box mesh
    
    Args:
        width: Box width
        height: Box height  
        depth: Box depth
        
    Returns:
        Open3D TriangleMesh object
    """
    if not HAS_OPEN3D:
        raise ImportError("Open3D is required")
    
    return o3d.geometry.TriangleMesh.create_box(width, height, depth)


def create_mesh_cylinder(radius: float = 1.0, height: float = 2.0, 
                        resolution: int = 20, split: int = 4) -> Any:
    """Create a cylinder mesh
    
    Args:
        radius: Cylinder radius
        height: Cylinder height
        resolution: Circular resolution
        split: Height split
        
    Returns:
        Open3D TriangleMesh object
    """
    if not HAS_OPEN3D:
        raise ImportError("Open3D is required")
    
    return o3d.geometry.TriangleMesh.create_cylinder(radius, height, resolution, split)


def apply_mesh_filter(mesh: Any, filter_type: str = "smooth", iterations: int = 1) -> Any:
    """Apply a filter to a mesh
    
    Args:
        mesh: Open3D TriangleMesh object
        filter_type: Type of filter ("smooth", "sharpen", "subdivide")
        iterations: Number of iterations
        
    Returns:
        Filtered mesh
    """
    if not HAS_OPEN3D:
        raise ImportError("Open3D is required")
    
    mesh_copy = o3d.geometry.TriangleMesh(mesh)
    
    if filter_type == "smooth":
        mesh_copy.filter_smooth_simple(number_of_iterations=iterations)
    elif filter_type == "sharpen":
        mesh_copy.filter_sharpen(number_of_iterations=iterations)
    elif filter_type == "subdivide":
        mesh_copy.subdivide_midpoint(number_of_iterations=iterations)
    
    return mesh_copy


def compute_mesh_normals(mesh: Any) -> Any:
    """Compute vertex normals for a mesh
    
    Args:
        mesh: Open3D TriangleMesh object
        
    Returns:
        Mesh with computed normals
    """
    if not HAS_OPEN3D:
        raise ImportError("Open3D is required")
    
    mesh_copy = o3d.geometry.TriangleMesh(mesh)
    mesh_copy.compute_vertex_normals()
    return mesh_copy


def visualize_mesh_wireframe(mesh: Any, width: int = 640, height: int = 480) -> Texture:
    """Render a mesh as wireframe
    
    Args:
        mesh: Open3D TriangleMesh object
        width: Render width
        height: Render height
        
    Returns:
        PyRay texture with wireframe rendering
    """
    if not HAS_OPEN3D:
        raise ImportError("Open3D is required")
    
    # Create renderer
    renderer = Open3DRenderer(width, height)
    
    # Create wireframe material
    material = o3d.visualization.rendering.MaterialRecord()
    material.shader = "unlitLine"
    material.line_width = 2.0
    
    # Convert mesh to line set for wireframe
    line_set = o3d.geometry.LineSet.create_from_triangle_mesh(mesh)
    
    # Add to scene
    renderer.add_geometry("wireframe", line_set, material)
    
    # Render
    return renderer.render_to_texture()


# Example usage function
def create_3d_scene_example() -> Open3DRenderer:
    """Create an example 3D scene with Open3D
    
    Returns:
        Configured Open3DRenderer
    """
    if not HAS_OPEN3D:
        raise ImportError("Open3D is required")
    
    renderer = Open3DRenderer(800, 600)
    
    # Create some geometry
    sphere = create_mesh_sphere(0.5, 30)
    sphere.paint_uniform_color([1.0, 0.0, 0.0])  # Red
    sphere.compute_vertex_normals()
    
    box = create_mesh_box(0.8, 0.8, 0.8)
    box.paint_uniform_color([0.0, 1.0, 0.0])  # Green
    box.compute_vertex_normals()
    box.translate([2, 0, 0])
    
    cylinder = create_mesh_cylinder(0.3, 1.5, 30)
    cylinder.paint_uniform_color([0.0, 0.0, 1.0])  # Blue
    cylinder.compute_vertex_normals()
    cylinder.translate([-2, 0, 0])
    
    # Add to scene
    renderer.add_geometry("sphere", sphere)
    renderer.add_geometry("box", box)
    renderer.add_geometry("cylinder", cylinder)
    
    # Set camera
    renderer.set_camera(eye=[3, 3, 3], center=[0, 0, 0])
    
    return renderer
