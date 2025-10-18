# Phase 4: Ecosystem & Polish

Phase 4 focuses on developer experience, deployment targets (web/mobile/desktop), performance tooling, and community programs. The goal is to make PyRay production-ready and delightful to adopt.

## Goals

- Provide project scaffolding and a smooth onboarding flow.
- Ship web/mobile/desktop packaging guides and helpers.
- Add performance profiling and debug visualization.
- Launch community ecosystem (templates, jams, showcase).

## Feature Set

- **Dev Tools**
  - Project template generator (`pyray-new`)
  - Debug draw helpers (bounds, physics, collisions)
  - Performance overlay (FPS, frame time, draw calls)
  - Hot-reload (where backend allows)

- **Deployment**
  - Web export guidance (Pyodide/WebAssembly)
  - Mobile packaging (Kivy/buildozer) with touch mapping
  - Desktop packaging (PyInstaller) with best practices

- **Performance**
  - Batching and culling recommendations
  - Memory and asset management tips
  - Profiling workflows with example scripts

- **Community**
  - Game jam templates and onboarding docs
  - Contribution guidelines and example issues/PRs
  - Showcase directory and submission process

## Tooling Sketch

- `pyray.tools.project_generator`
```bash
pyray-new my-game
cd my-game
python run.py
```

- `pyray.debug`
```python
pyray.debug.draw_aabb(x, y, w, h, color=pyray.LIME)
pyray.debug.draw_grid(spacing=32, color=pyray.fade(pyray.GRAY, 0.3))
pyray.debug.overlay(enable=True)  # FPS, frame time, batches
```

- Packaging Guides
  - `docs/deployment/web.md`
  - `docs/deployment/mobile.md`
  - `docs/deployment/desktop.md`

## Example Projects To Ship

- **Jam Starter Kit:** menu state + gameplay state + build scripts.
- **Web Export Demo:** playable in browser via Pyodide.
- **Mobile Touch Demo:** on-screen controls and touch gestures.

## Acceptance Criteria

- New project can be scaffolded and run in under 1 minute.
- Clear deployment instructions with verified example repos.
- Debug overlay and helpers documented and demoed.

## Contributing Checklist

- **Tools:** implement `pyray-new` and template contents.
- **Debug:** overlay + helpers and toggles.
- **Docs:** deployment guides, jam templates, contribution flow.
