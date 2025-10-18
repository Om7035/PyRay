# Getting Started with PyRay

Welcome to PyRay! This guide helps you install the library, run examples, and create your first project.

## Prerequisites

- Python 3.8 or newer
- Windows/macOS/Linux

## Installation

Install from source in development mode (recommended while the project evolves):

```bash
# From the project root
pip install -e .
```

If you only want to run the examples inside this repo, install dependencies:

```bash
pip install -r requirements.txt
```

## Running Examples

The `examples/` folder contains runnable demos:

```bash
python examples/01_hello_world.py
python examples/02_drawing_shapes.py
python examples/03_input_handling.py
python examples/04_bouncing_ball.py
python examples/05_pong.py
```

If a window does not appear or closes immediately, check your Python/pygame installation and GPU drivers.

## Your First Program (5 minutes)

```python
import pyray

pyray.init_window(800, 600, "My First PyRay Program")
pyray.set_target_fps(60)

while not pyray.window_should_close():
    pyray.begin_drawing()
    pyray.clear_background(pyray.BLACK)
    x, y = pyray.get_mouse_x(), pyray.get_mouse_y()
    pyray.draw_text("Hello, PyRay!", 10, 10, 24, pyray.WHITE)
    pyray.draw_circle(x, y, 20, pyray.RED)
    pyray.end_drawing()

pyray.close_window()
```

## Common Issues

- "No module named pyray": ensure you ran `pip install -e .` from the repo root.
- Black screen: make sure you call `begin_drawing()` then `end_drawing()` each frame.
- High CPU usage: use `pyray.set_target_fps(60)` to limit FPS.

## Next Steps

- Browse the API overview: `docs/api-reference.md`
- Read the roadmap for upcoming features: `docs/roadmap/`
- Try the Jupyter + ML integrations: `docs/integrations/jupyter-ml.md`
