# Desktop Packaging (Windows/macOS/Linux)

Use PyInstaller to build distributable executables for desktop platforms.

## Quick Start

```bash
pip install pyinstaller
pyinstaller -F your_game.py
```

## Tips

- Include assets in the bundle via `--add-data`.
- Test on a clean machine or VM.
- Prefer relative paths for assets.

## Example

```bash
pyinstaller -F --add-data "assets;assets" examples/05_pong.py
```
