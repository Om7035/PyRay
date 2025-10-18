# Phase 2: Advanced 2D & Foundation

This document describes the goals, APIs, examples, and contribution plan for Phase 2. The focus is to complete a full-featured 2D stack: animation, camera, particles, collisions, physics, advanced input, and enhanced audio.

## Goals

- Complete, ergonomic 2D workflow suitable for platformers, shooters, and arcade games.
- Keep API simple with progressive disclosure for power users.
- Ship battle-tested examples and mini tools to accelerate learning.

## Feature Set

- **Sprite Sheets & Animation**
  - Frame definitions from sprite sheets
  - Named animations (loop, once, ping-pong)
  - Events: `on_start`, `on_frame`, `on_complete`
  - Time-based playback (FPS/seconds)

- **2D Camera**
  - Pan, zoom, rotate
  - Follow target with smoothing
  - World bounds and dead zones
  - Viewport helpers and screen-to-world mapping

- **Particle System**
  - Emitters (burst, continuous)
  - Parameters: lifetime, speed, gravity, color over time
  - Built-in effects (sparks, smoke, fire)

- **Visual Effects & Blending**
  - Blend modes: additive, multiply, screen
  - Tinting and alpha fades
  - Simple post-process effects (blur, glow) where backend allows

- **Advanced Text**
  - Custom font loading (TTF)
  - Alignment, wrapping, outline/shadow

- **Collision Detection**
  - AABB, circle, AABB-circle
  - Point queries and raycasts
  - Spatial partitioning (grid/quadtree)

- **2D Physics**
  - Rigid bodies (dynamic/static/kinematic)
  - Gravity, forces/impulses, damping
  - Simple constraints (pin)
  - Collision response (slide/bounce)

- **Advanced Input**
  - Gamepad (multi-controller)
  - Input history/buffer for combos
  - Touch support (for mobile later)

- **Enhanced Audio**
  - Groups: Master, SFX, Music
  - Ducking (auto lower music when SFX plays)

## Planned Modules & API Sketch

- `pyray.animation`
```python
anim = pyray.animation.create(sprite_sheet, frame_w=32, frame_h=32)
anim.add("run", frames=[0,1,2,3,4,5], fps=12, loop=True)
anim.play("run")
anim.update(dt)
anim.draw(x, y)
```

- `pyray.camera`
```python
cam = pyray.camera.create()
cam.follow(target, smooth=0.15)
cam.set_bounds(0, 0, world_w, world_h)
with cam.apply():
    # all draw calls are transformed
    pyray.draw_rectangle(...)
```

- `pyray.particles`
```python
em = pyray.particles.emitter(x, y, kind="burst", rate=200, lifetime=(0.4, 0.8))
em.color_over_time([(0.0, pyray.YELLOW), (1.0, pyray.BLANK)])
em.update(dt)
em.draw()
```

- `pyray.collision`
```python
hit = pyray.collision.rect_rect(r1, r2)
info = pyray.collision.raycast(origin, direction, max_dist, colliders)
```

- `pyray.physics`
```python
world = pyray.physics.World(gravity=(0, 900))
body = world.body(dynamic=True, x=100, y=100, w=32, h=32)
body.apply_force(0, -250)
world.step(dt)
```

- `pyray.input` (extensions)
```python
if pyray.is_gamepad_available(0):
    x = pyray.get_gamepad_axis_movement(0, "LX")
    if pyray.is_gamepad_button_pressed(0, "A"): jump()
```

## Example Projects To Ship

- **Pong+ (remastered):** camera shake, particles, SFX ducking.
- **Platformer Kit:** player controller, camera follow, tiles, collisions.
- **Particles Playground:** tweakable emitter parameters in real-time.
- **Top-Down Shooter:** enemy AI lite, collisions, particle impacts.

## Acceptance Criteria

- Render 1000 particles at 60 FPS on mid-range laptops.
- Physics stable for common 2D gameplay (no tunneling for typical speeds).
- Clear tutorial coverage for each new subsystem.

## Performance Targets

- Batching where possible, avoid per-frame allocations.
- Grid partitioning by default; quadtree optional.

## Backward Compatibility

- Phase 1 APIs remain intact.
- New features are opt-in; defaults maintain simplicity.

## Contributing Checklist

- **Animation:** frame parser, named clips, events, tests.
- **Camera:** transform stack, follow/smooth, bounds, tests.
- **Particles:** emitter core, presets, pooling, examples.
- **Collision/Physics:** algorithms, world step, debug draw.
- **Docs:** tutorials and API reference pages for each subsystem.
