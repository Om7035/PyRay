# Phase 3: 3D & Advanced

This document outlines PyRay's Phase 3 goals: adding practical, beginner-friendly 3D while preserving the simplicity of the 2D API.

## Goals

- Provide approachable 3D primitives and camera.
- Support basic model loading (glTF/OBJ) and materials.
- Introduce lighting and simple shaders with clear examples.
- Keep API progressive: simple defaults, power when needed.

## Feature Set

- **3D Primitives**
  - Cube, sphere, cylinder, cone, plane, torus
  - Wireframe and solid modes

- **3D Camera**
  - Perspective and orthographic
  - Orbit, FPS-style, and target-follow helpers
  - Frustum culling

- **Model System**
  - Load glTF 2.0 and OBJ
  - Materials: color, texture, basic PBR
  - Transform hierarchy (parent-child)

- **Lighting**
  - Directional, point, spotlights
  - Ambient lighting
  - Simple shadows (where backend allows)

- **Shaders**
  - Built-in effects (toon, grayscale)
  - Custom GLSL pipeline (ModernGL backend)

## API Sketch

- `pyray.models`
```python
# Load and draw a model
model = pyray.models.load_model("robot.glb")
model.position = pyray.Vector3(0, 0, 0)
model.rotation = pyray.Quaternion.identity()
model.scale = 1.0
model.draw()
```

- `pyray.camera3d`
```python
cam = pyray.camera3d.create_perspective(fov=60, near=0.1, far=100.0)
cam.orbit(target=(0,0,0), distance=6.0, yaw=45, pitch=-20)
with cam.apply():
    model.draw()
    pyray.draw_cube((0,0,0), 1, 1, 1, pyray.BLUE)
```

- `pyray.lighting`
```python
light = pyray.lighting.directional(direction=(1,-1,0), color=pyray.WHITE, intensity=1.0)
scene = pyray.Scene(camera=cam, lights=[light])
scene.draw([model])
```

## Example Projects To Ship

- **3D Primitives Playground:** orbit camera, draw primitives, change materials.
- **Model Viewer:** load glTF/OBJ, orbit camera, toggle lights.
- **3D Runner Demo:** simple track, obstacles, basic shadows.

## Performance Targets

- 60 FPS on laptops for scenes with a few thousand triangles.
- Efficient resource management and frustum culling.

## Backward Compatibility

- 2D remains unchanged; 3D is additive and optional.

## Contributing Checklist

- **Primitives:** geometry generation + draw helpers.
- **Camera:** transforms, helpers, context manager.
- **Models:** loaders and material system.
- **Lighting:** light representations and shader glue.
- **Shaders:** minimal shader library and examples.
- **Docs:** 3D tutorials and API reference pages.
