# PyRay - Python Game Development Made Simple 🎮

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Discord](https://img.shields.io/discord/1234567890?color=7289da&label=Discord&logo=discord&logoColor=white)](https://discord.gg/pyray)

PyRay is a simple and easy-to-use Python library for game development and multimedia applications. Inspired by [raylib](https://www.raylib.com/), PyRay brings the simplicity of game development to Python with an intuitive API that lets you create games in just a few lines of code.

## 🚀 Features

- **Simple and Intuitive** - Create a window and start drawing in just 3 lines of code
- **Cross-Platform** - Works on Windows, macOS, Linux, and Web (via Pyodide)
- **2D Graphics** - Shapes, sprites, text rendering, particle systems
- **3D Graphics** - Basic 3D shapes, model loading, lighting (coming soon)
- **Input Handling** - Keyboard, mouse, gamepad support
- **Audio System** - Sound effects and music playback
- **Physics** - Built-in 2D physics and collision detection
- **Fast** - Hardware-accelerated rendering

## 📦 Installation

```bash
pip install pyray
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

- [Hello World](examples/01_hello_world.py) - Your first PyRay program
- [Drawing Shapes](examples/02_drawing_shapes.py) - Drawing various 2D shapes
- [Sprite Animation](examples/03_sprite_animation.py) - Animating sprites
- [Simple Game](examples/04_pong.py) - A complete Pong game in under 100 lines

## 🎓 Learning Resources

- [Getting Started Guide](docs/getting-started.md)
- [API Reference](docs/api-reference.md)
- [Tutorials](docs/tutorials/)
- [Video Tutorials](https://youtube.com/@pyray)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 🗺️ Roadmap

### Phase 1: MVP (Current)
- ✅ Window management
- ✅ Basic 2D graphics
- ✅ Input system
- 🚧 Sprite loading
- 🚧 Audio system

### Phase 2: Advanced 2D
- ⏳ Physics engine
- ⏳ Particle systems
- ⏳ Advanced animations

### Phase 3: 3D Support
- ⏳ 3D rendering
- ⏳ Model loading
- ⏳ Lighting system

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
