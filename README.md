# PyRay - Python Game Development Made Simple 🎮

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Discord](https://img.shields.io/discord/1234567890?color=7289da&label=Discord&logo=discord&logoColor=white)](https://discord.gg/pyray)

PyRay is a simple and easy-to-use Python library for game development and multimedia applications. Inspired by [raylib](https://www.raylib.com/), PyRay brings the simplicity of game development to Python with an intuitive API that lets you create games in just a few lines of code.

## 🚀 Features

- **Simple and Intuitive** - Create a window and start drawing in just 3 lines of code
- **Cross-Platform** - Works on Windows, macOS, Linux, and Web (via Pyodide)
- **2D Graphics** - Shapes, sprites, text rendering, particle systems
- **3D Graphics** - Basic 3D shapes, model loading, lighting (via Open3D/PyVista)
- **Input Handling** - Keyboard, mouse, gamepad support
- **Audio System** - Sound effects and music playback
- **Physics** - Built-in 2D physics and collision detection
- **Fast** - Hardware-accelerated rendering
- **Integrations** - OpenCV, Matplotlib, Jupyter, Open3D, PyVista support
- **Tools** - Project generator, migration guides, extensive examples

## 📦 Installation

```bash
# Basic installation
pip install pyray

# With optional integrations
pip install pyray[opencv]      # Computer vision support
pip install pyray[matplotlib]  # Data visualization
pip install pyray[jupyter]     # Jupyter notebook support
pip install pyray[all]         # Everything
```

## 🎯 Quick Start

```python
import pyray

# Create a window
pyray.init_window(800, 600, "My First PyRay Game")

# Game loop
while not pyray.window_should_close():
    # Update
    x = pyray.get_mouse_x()
    y = pyray.get_mouse_y()
    
    # Draw
    pyray.begin_drawing()
    pyray.clear_background(pyray.BLACK)
    pyray.draw_circle(x, y, 20, pyray.RED)
    pyray.draw_text("Hello PyRay!", 10, 10, 20, pyray.WHITE)
    pyray.end_drawing()

# Cleanup
pyray.close_window()
```

## 📚 Examples

Check out the [examples](examples/) directory for more demos:

**Basic Examples:**
- [Hello World](examples/01_hello_world.py) - Your first PyRay program
- [Drawing Shapes](examples/02_drawing_shapes.py) - Drawing various 2D shapes
- [Input Handling](examples/03_input_handling.py) - Keyboard and mouse input demo
- [Bouncing Ball](examples/04_bouncing_ball.py) - Simple physics and trails
- [Pong Game](examples/05_pong.py) - A complete 2-player Pong

**Complete Games:**
- [Snake](examples/games/snake.py) - Classic snake game with particles
- [Tetris](examples/games/tetris.py) - Full Tetris with rotation and line clearing
- [Space Shooter](examples/games/space_shooter.py) - Vertical shooter with power-ups

**Integrations:**
- [OpenCV Webcam](examples/integrations/opencv_webcam_filters.py) - Real-time video filters
- [Matplotlib Charts](examples/integrations/matplotlib_live_charts.py) - Live data visualization

## 🎓 Learning Resources

- [Getting Started Guide](docs/getting-started.md)
- [API Reference (Overview)](docs/api-reference.md)
- [Tutorials](docs/tutorials/)
- [Integrations: Jupyter & ML](docs/integrations/jupyter-ml.md)
- [Deployment Guides](docs/deployment/)
- [Roadmap](docs/roadmap/README.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 🗺️ Roadmap

### Phase 1: MVP (Current)
- ✅ Window management
- ✅ Basic 2D graphics (shapes, text)
- ✅ Input system (keyboard, mouse)
- ✅ Sprites & images (load/draw textures)
- ✅ Audio basics (sounds, music)

Read full roadmap and plans:

- [Phase 2: Advanced 2D & Foundation](docs/roadmap/phase-2.md)
- [Phase 3: 3D & Advanced](docs/roadmap/phase-3.md)
- [Phase 4: Ecosystem & Polish](docs/roadmap/phase-4.md)

## 📄 License

PyRay is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 🌟 Support

- **Discord**: [Join our community](https://discord.gg/pyray)
- **GitHub Issues**: [Report bugs or request features](https://github.com/Om7035/PyRay/issues)
- **Discussions**: [Ask questions and share ideas](https://github.com/Om7035/PyRay/discussions)

## 💖 Sponsors

PyRay is an open-source project. If you'd like to support its development:

- [GitHub Sponsors](https://github.com/sponsors/Om7035)
- [Patreon](https://patreon.com/pyray)

---

Made with ❤️ by the PyRay community
