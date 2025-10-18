# Jupyter & ML Integrations with PyRay

This guide shows how to use PyRay effectively in Jupyter notebooks and how ML practitioners can benefit from PyRay for visualization, prototyping, and interactive demos.

## Why PyRay for ML?

- Rapid prototyping of interactive visualizations and simulations
- Visualize model predictions, annotations, and data augmentations
- Build teaching demos that run in-class (Jupyter-ready workflows)

## Running in Jupyter: Approaches

Pygame windows can work in Jupyter, but notebook cells are not ideal for real-time loops. Here are practical approaches:

### 1) Snapshot Rendering (inline images)

Render a frame, capture it to a NumPy array, and display inline using IPython.

```python
import pyray, pygame, numpy as np
from IPython.display import display, clear_output
from PIL import Image
import time

# Create a window (a native window may appear). For headless snapshots see notes below.
pyray.init_window(640, 360, "PyRay Jupyter Snapshot")
pyray.set_target_fps(60)

for t in range(60):  # 60 frames
    pyray.begin_drawing()
    pyray.clear_background(pyray.DARKGRAY)
    pyray.draw_text(f"Frame {t}", 10, 10, 20, pyray.WHITE)
    pyray.draw_circle(100 + t*3, 180, 20, pyray.RED)
    pyray.end_drawing()

    # Capture the current frame from pygame
    surf = pygame.display.get_surface()  # current screen surface
    arr = pygame.surfarray.array3d(surf)  # (W, H, 3)
    # Convert to image (transpose to H,W,3), then display inline
    img = Image.fromarray(np.transpose(arr, (1,0,2)))
    clear_output(wait=True)
    display(img)
    time.sleep(0.02)

pyray.close_window()
```

### 2) Offline Video/GIF Generation

Generate frames offscreen and save as a GIF or MP4 for reports or docs.

```python
import pyray, pygame, numpy as np, imageio
from PIL import Image

pyray.init_window(320, 240, "Recorder")
frames = []

for t in range(120):  # 2 seconds @ 60 FPS
    pyray.begin_drawing()
    pyray.clear_background(pyray.BLACK)
    pyray.draw_circle(160, 120, 30, pyray.RED)
    pyray.draw_text(f"t={t}", 10, 10, 20, pyray.WHITE)
    pyray.end_drawing()

    surf = pygame.display.get_surface()
    arr = pygame.surfarray.array3d(surf)
    img = Image.fromarray(np.transpose(arr, (1,0,2)))
    frames.append(img)

imageio.mimsave("demo.gif", frames, duration=1/60)
pyray.close_window()
```

### 3) Headless Mode (advanced)

On some platforms you can set SDL to use a dummy video driver for offscreen rendering:

```python
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"  # try before importing pygame
```

This may not support full rendering on all systems. If it fails, use the snapshot or offline methods above.

## ML Use Cases

- **Dataset Visualization**: draw bounding boxes, keypoints, segmentation previews during preprocessing.
- **Model Inference Demos**: render predictions in real-time and record GIFs for reports.
- **Reinforcement Learning**: use PyRay to visualize agents, states, and rewards for debugging.
- **Interactive Annotation Tools**: build simple in-notebook UIs (mouse/keyboard) to correct labels.
- **Procedural Data Generation**: synthesize labeled 2D scenes for training toy models.

## Interop Tips

- Use `numpy` to compute geometry (e.g., polygon points) and pass values into PyRay draw calls.
- Convert pygame surfaces to NumPy arrays via `pygame.surfarray.array3d` for further ML processing.
- Keep the main loop short in notebooks; consider generating frames in batches.

## Example: Drawing Bounding Boxes

```python
import pyray

W, H = 640, 360
pyray.init_window(W, H, "BBox Demo")

boxes = [(50, 40, 120, 80), (200, 100, 180, 120)]  # x, y, w, h

for _ in range(120):
    pyray.begin_drawing()
    pyray.clear_background(pyray.BLACK)
    for (x, y, w, h) in boxes:
        pyray.draw_rectangle_lines(x, y, w, h, pyray.GREEN)
    pyray.draw_text("Bounding Boxes", 10, 10, 20, pyray.WHITE)
    pyray.end_drawing()

pyray.close_window()
```

## Next Steps

- See the roadmap for Phase 2/3 features that further benefit ML and education: `docs/roadmap/`
- Share your notebook examples via PRs to `docs/integrations/`!
