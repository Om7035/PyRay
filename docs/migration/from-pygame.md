# Migration Guide: From Pygame to PyRay

This guide helps Pygame developers transition to PyRay, highlighting key differences and providing equivalent code examples.

## Why Migrate to PyRay?

- **Simpler API**: PyRay provides a more intuitive, beginner-friendly API
- **Better defaults**: Sensible defaults mean less boilerplate code
- **Modern features**: Built-in support for shaders, 3D, and advanced effects
- **Integrated tools**: Project generator, asset management, and more
- **Active community**: Growing ecosystem with regular updates

## Quick Comparison

| Pygame | PyRay |
|--------|-------|
| `pygame.init()` | `pyray.init_window()` |
| `pygame.display.set_mode()` | Included in `init_window()` |
| `pygame.time.Clock()` | `pyray.set_target_fps()` |
| `pygame.event.get()` | Automatic event handling |
| `pygame.draw.rect()` | `pyray.draw_rectangle()` |
| `pygame.draw.circle()` | `pyray.draw_circle()` |
| `pygame.font.Font()` | `pyray.load_font()` |
| `pygame.image.load()` | `pyray.load_texture()` |
| `pygame.mixer.Sound()` | `pyray.load_sound()` |

## Basic Window Setup

### Pygame
```python
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0, 0, 0))
    # Draw here
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

### PyRay
```python
import pyray

pyray.init_window(800, 600, "My Game")
pyray.set_target_fps(60)

while not pyray.window_should_close():
    pyray.begin_drawing()
    pyray.clear_background(pyray.BLACK)
    # Draw here
    pyray.end_drawing()

pyray.close_window()
```

## Drawing Shapes

### Pygame
```python
# Rectangle
pygame.draw.rect(screen, (255, 0, 0), (100, 100, 50, 50))

# Circle
pygame.draw.circle(screen, (0, 255, 0), (200, 200), 30)

# Line
pygame.draw.line(screen, (0, 0, 255), (0, 0), (100, 100), 2)

# Polygon
points = [(100, 100), (150, 50), (200, 100)]
pygame.draw.polygon(screen, (255, 255, 0), points)
```

### PyRay
```python
# Rectangle
pyray.draw_rectangle(100, 100, 50, 50, pyray.RED)

# Circle
pyray.draw_circle(200, 200, 30, pyray.GREEN)

# Line
pyray.draw_line(0, 0, 100, 100, pyray.BLUE)

# Polygon (using triangle as example)
v1 = pyray.Vector2(100, 100)
v2 = pyray.Vector2(150, 50)
v3 = pyray.Vector2(200, 100)
pyray.draw_triangle(v1, v2, v3, pyray.YELLOW)
```

## Handling Input

### Pygame
```python
# Keyboard
keys = pygame.key.get_pressed()
if keys[pygame.K_SPACE]:
    # Space is held
    pass

for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            # Space was just pressed
            pass

# Mouse
mouse_x, mouse_y = pygame.mouse.get_pos()
mouse_buttons = pygame.mouse.get_pressed()
if mouse_buttons[0]:  # Left button
    pass
```

### PyRay
```python
# Keyboard
if pyray.is_key_down(pyray.KEY_SPACE):
    # Space is held
    pass

if pyray.is_key_pressed(pyray.KEY_SPACE):
    # Space was just pressed
    pass

# Mouse
mouse_x = pyray.get_mouse_x()
mouse_y = pyray.get_mouse_y()
if pyray.is_mouse_button_down(pyray.MOUSE_BUTTON_LEFT):
    pass
```

## Loading and Drawing Images

### Pygame
```python
# Load image
image = pygame.image.load("sprite.png")
image_rect = image.get_rect()

# Draw image
screen.blit(image, (100, 100))

# Draw scaled image
scaled = pygame.transform.scale(image, (200, 200))
screen.blit(scaled, (300, 100))
```

### PyRay
```python
# Load texture
texture = pyray.load_texture("sprite.png")

# Draw texture
pyray.draw_texture(texture, 100, 100, pyray.WHITE)

# Draw scaled texture
pyray.draw_texture_ex(texture, 300, 100, 0, 2.0, pyray.WHITE)
```

## Text Rendering

### Pygame
```python
# Create font
font = pygame.font.Font(None, 36)

# Render text
text_surface = font.render("Hello World", True, (255, 255, 255))

# Draw text
screen.blit(text_surface, (100, 100))
```

### PyRay
```python
# Draw text (default font)
pyray.draw_text("Hello World", 100, 100, 36, pyray.WHITE)

# Load custom font
font = pyray.load_font("myfont.ttf")
pyray.draw_text_ex(font, "Hello World", (100, 100), 36, 2, pyray.WHITE)
```

## Sound and Music

### Pygame
```python
# Initialize mixer
pygame.mixer.init()

# Load and play sound
sound = pygame.mixer.Sound("sound.wav")
sound.play()

# Load and play music
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)  # Loop forever
```

### PyRay
```python
# Initialize audio
pyray.init_audio_device()

# Load and play sound
sound = pyray.load_sound("sound.wav")
pyray.play_sound(sound)

# Load and play music
music = pyray.load_music_stream("music.mp3")
pyray.play_music_stream(music)
```

## Sprite Classes

### Pygame
```python
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)
```

### PyRay
```python
class Player:
    def __init__(self):
        self.texture = pyray.load_texture("player.png")
        self.x = 100
        self.y = 100
        self.width = self.texture.width
        self.height = self.texture.height
        
    def update(self, dt):
        if pyray.is_key_down(pyray.KEY_LEFT):
            self.x -= 300 * dt  # Speed * delta time
        if pyray.is_key_down(pyray.KEY_RIGHT):
            self.x += 300 * dt
            
    def draw(self):
        pyray.draw_texture(self.texture, self.x, self.y, pyray.WHITE)
```

## Collision Detection

### Pygame
```python
# Rectangle collision
rect1 = pygame.Rect(100, 100, 50, 50)
rect2 = pygame.Rect(120, 120, 50, 50)
if rect1.colliderect(rect2):
    # Collision detected
    pass

# Circle collision (manual)
import math
dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
if dist < radius1 + radius2:
    # Collision detected
    pass
```

### PyRay
```python
# Rectangle collision
if pyray.check_collision_recs((100, 100, 50, 50), (120, 120, 50, 50)):
    # Collision detected
    pass

# Circle collision
pos1 = pyray.Vector2(x1, y1)
pos2 = pyray.Vector2(x2, y2)
if pyray.check_collision_circles(pos1, radius1, pos2, radius2):
    # Collision detected
    pass
```

## Color Management

### Pygame
```python
# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Use colors
screen.fill(BLACK)
pygame.draw.rect(screen, RED, (100, 100, 50, 50))
```

### PyRay
```python
# Use built-in colors
pyray.clear_background(pyray.BLACK)
pyray.draw_rectangle(100, 100, 50, 50, pyray.RED)

# Create custom colors
my_color = pyray.Color(128, 64, 255, 255)  # RGBA
```

## Common Patterns

### Game State Management

#### Pygame Pattern
```python
class GameState:
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2

state = GameState.MENU

while running:
    if state == GameState.MENU:
        # Handle menu
        pass
    elif state == GameState.PLAYING:
        # Handle gameplay
        pass
```

#### PyRay Pattern (Same!)
```python
from enum import Enum

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2

state = GameState.MENU

while not pyray.window_should_close():
    if state == GameState.MENU:
        # Handle menu
        pass
    elif state == GameState.PLAYING:
        # Handle gameplay
        pass
```

## Performance Tips

1. **Use delta time**: PyRay provides `get_frame_time()` for smooth movement
2. **Batch drawing**: PyRay automatically batches similar draw calls
3. **Texture atlases**: Use sprite sheets for better performance
4. **Avoid per-frame allocations**: Reuse objects when possible

## Advanced Features in PyRay

PyRay offers several features not readily available in Pygame:

- **Shaders**: Custom GPU shaders for effects
- **3D Graphics**: Full 3D rendering support
- **Camera Systems**: 2D and 3D camera management
- **Particle Systems**: Built-in particle effects
- **Physics**: Integrated physics simulation

## Migration Checklist

- [ ] Replace `pygame.init()` with `pyray.init_window()`
- [ ] Remove explicit event loops
- [ ] Update drawing functions to PyRay equivalents
- [ ] Convert RGB tuples to PyRay colors
- [ ] Replace `clock.tick()` with `set_target_fps()`
- [ ] Update input handling to PyRay methods
- [ ] Convert sprite classes to simpler PyRay entities
- [ ] Replace `blit()` with `draw_texture()`
- [ ] Update collision detection functions
- [ ] Add delta time to movement calculations

## Getting Help

- [PyRay Documentation](../README.md)
- [API Reference](../api-reference.md)
- [Examples](../../examples/)
- [Community Discord](https://discord.gg/pyray)

## Example: Complete Game Migration

See the [migrated Pygame examples](../../examples/migrations/) for complete game conversions from Pygame to PyRay.
