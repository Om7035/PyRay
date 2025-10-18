"""
PyRay Project Generator
Create new PyRay projects with templates and boilerplate
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional

# Project templates
TEMPLATES = {
    "basic": {
        "description": "Basic PyRay window with game loop",
        "files": {
            "main.py": '''"""
{project_name} - A PyRay Game
Created with pyray-new
"""

import pyray

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "{project_name}"

def main():
    # Initialize
    pyray.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    pyray.set_target_fps(60)
    
    # Game loop
    while not pyray.window_should_close():
        # Update
        dt = pyray.get_frame_time()
        
        # TODO: Add your update logic here
        
        # Draw
        pyray.begin_drawing()
        pyray.clear_background(pyray.DARKGRAY)
        
        # TODO: Add your drawing code here
        pyray.draw_text("Hello PyRay!", 10, 10, 20, pyray.WHITE)
        
        pyray.end_drawing()
    
    # Cleanup
    pyray.close_window()

if __name__ == "__main__":
    main()
''',
            "requirements.txt": "pyray>=0.1.0\n",
            "README.md": """# {project_name}

A game created with PyRay.

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python main.py
```

## Controls

- ESC: Exit

## License

MIT
"""
        }
    },
    
    "game": {
        "description": "Complete game template with states and entities",
        "files": {
            "main.py": '''"""
{project_name} - A PyRay Game
Created with pyray-new
"""

import pyray
from game import Game

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "{project_name}"

def main():
    # Initialize
    pyray.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    pyray.set_target_fps(60)
    
    # Create game
    game = Game()
    
    # Game loop
    while not pyray.window_should_close():
        dt = pyray.get_frame_time()
        
        # Update
        game.update(dt)
        
        # Draw
        pyray.begin_drawing()
        pyray.clear_background(pyray.DARKGRAY)
        
        game.draw()
        
        # Show FPS
        fps = pyray.get_fps()
        pyray.draw_text(f"FPS: {{fps}}", 10, 10, 14, pyray.GREEN)
        
        pyray.end_drawing()
    
    # Cleanup
    pyray.close_window()

if __name__ == "__main__":
    main()
''',
            "game.py": '''"""
Game logic and state management
"""

import pyray
from enum import Enum

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3

class Game:
    def __init__(self):
        self.state = GameState.MENU
        self.score = 0
        self.high_score = 0
        
    def reset(self):
        """Reset game to initial state"""
        self.score = 0
        # TODO: Reset game entities
        
    def update(self, dt: float):
        """Update game logic"""
        if self.state == GameState.MENU:
            if pyray.is_key_pressed(pyray.KEY_ENTER):
                self.reset()
                self.state = GameState.PLAYING
                
        elif self.state == GameState.PLAYING:
            # TODO: Update game entities
            
            if pyray.is_key_pressed(pyray.KEY_P):
                self.state = GameState.PAUSED
                
        elif self.state == GameState.PAUSED:
            if pyray.is_key_pressed(pyray.KEY_P):
                self.state = GameState.PLAYING
                
        elif self.state == GameState.GAME_OVER:
            if pyray.is_key_pressed(pyray.KEY_ENTER):
                self.reset()
                self.state = GameState.PLAYING
            elif pyray.is_key_pressed(pyray.KEY_ESCAPE):
                self.state = GameState.MENU
                
    def draw(self):
        """Draw game"""
        if self.state == GameState.MENU:
            pyray.draw_text("{project_name}", 300, 200, 36, pyray.WHITE)
            pyray.draw_text("Press ENTER to start", 280, 300, 18, pyray.LIGHTGRAY)
            
        elif self.state == GameState.PLAYING:
            # TODO: Draw game entities
            pyray.draw_text(f"Score: {{self.score}}", 10, 40, 20, pyray.WHITE)
            
        elif self.state == GameState.PAUSED:
            pyray.draw_text("PAUSED", 350, 280, 30, pyray.YELLOW)
            pyray.draw_text("Press P to continue", 310, 320, 16, pyray.WHITE)
            
        elif self.state == GameState.GAME_OVER:
            pyray.draw_text("GAME OVER", 320, 250, 36, pyray.RED)
            pyray.draw_text(f"Score: {{self.score}}", 350, 300, 24, pyray.WHITE)
            pyray.draw_text("Press ENTER to retry", 300, 340, 18, pyray.LIGHTGRAY)
''',
            "entities.py": '''"""
Game entities and objects
"""

import pyray
from typing import List

class Entity:
    """Base class for game entities"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.active = True
        
    def update(self, dt: float):
        """Update entity"""
        pass
        
    def draw(self):
        """Draw entity"""
        pass
        
    def collides_with(self, other: 'Entity') -> bool:
        """Check collision with another entity"""
        # TODO: Implement collision detection
        return False

class Player(Entity):
    """Player character"""
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.speed = 200
        self.size = 20
        
    def update(self, dt: float):
        """Update player"""
        if pyray.is_key_down(pyray.KEY_LEFT):
            self.x -= self.speed * dt
        if pyray.is_key_down(pyray.KEY_RIGHT):
            self.x += self.speed * dt
        if pyray.is_key_down(pyray.KEY_UP):
            self.y -= self.speed * dt
        if pyray.is_key_down(pyray.KEY_DOWN):
            self.y += self.speed * dt
            
    def draw(self):
        """Draw player"""
        pyray.draw_circle(int(self.x), int(self.y), self.size, pyray.BLUE)
''',
            "assets/.gitkeep": "",
            "requirements.txt": "pyray>=0.1.0\n",
            "README.md": """# {project_name}

A game created with PyRay.

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python main.py
```

## Project Structure

- `main.py` - Entry point and main loop
- `game.py` - Game state management
- `entities.py` - Game objects and entities
- `assets/` - Game assets (images, sounds, etc.)

## Controls

- Arrow Keys: Move
- P: Pause
- ESC: Exit

## License

MIT
"""
        }
    },
    
    "platformer": {
        "description": "2D platformer game template",
        "files": {
            "main.py": '''"""
{project_name} - A PyRay Platformer
Created with pyray-new
"""

import pyray
from game import PlatformerGame

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
TITLE = "{project_name}"

def main():
    # Initialize
    pyray.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    pyray.set_target_fps(60)
    
    # Create game
    game = PlatformerGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Game loop
    while not pyray.window_should_close():
        dt = pyray.get_frame_time()
        
        # Update
        game.update(dt)
        
        # Draw
        pyray.begin_drawing()
        pyray.clear_background(pyray.SKYBLUE)
        
        game.draw()
        
        pyray.end_drawing()
    
    # Cleanup
    pyray.close_window()

if __name__ == "__main__":
    main()
''',
            "game.py": '''"""
Platformer game logic
"""

import pyray
from player import Player
from level import Level

class PlatformerGame:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.player = Player(100, height - 200)
        self.level = Level()
        self.camera_x = 0
        self.camera_y = 0
        
    def update(self, dt: float):
        """Update game"""
        self.player.update(dt, self.level)
        
        # Update camera to follow player
        target_x = self.player.x - self.width // 2
        target_y = self.player.y - self.height // 2
        
        self.camera_x += (target_x - self.camera_x) * 0.1
        self.camera_y += (target_y - self.camera_y) * 0.1
        
    def draw(self):
        """Draw game"""
        # Apply camera transform
        pyray.push_matrix()
        pyray.translate(-self.camera_x, -self.camera_y, 0)
        
        # Draw level
        self.level.draw()
        
        # Draw player
        self.player.draw()
        
        pyray.pop_matrix()
        
        # Draw UI
        pyray.draw_text(f"Score: {{self.player.score}}", 10, 10, 20, pyray.WHITE)
''',
            "player.py": '''"""
Player character for platformer
"""

import pyray

class Player:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.width = 32
        self.height = 48
        self.speed = 300
        self.jump_power = 500
        self.gravity = 1000
        self.on_ground = False
        self.score = 0
        
    def update(self, dt: float, level):
        """Update player physics"""
        # Horizontal movement
        if pyray.is_key_down(pyray.KEY_LEFT):
            self.vx = -self.speed
        elif pyray.is_key_down(pyray.KEY_RIGHT):
            self.vx = self.speed
        else:
            self.vx *= 0.8  # Friction
            
        # Jump
        if pyray.is_key_pressed(pyray.KEY_SPACE) and self.on_ground:
            self.vy = -self.jump_power
            
        # Apply gravity
        self.vy += self.gravity * dt
        
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Check ground collision (simple)
        if self.y > 500:  # Ground level
            self.y = 500
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
    def draw(self):
        """Draw player"""
        pyray.draw_rectangle(int(self.x - self.width//2), 
                            int(self.y - self.height),
                            self.width, self.height, pyray.RED)
''',
            "level.py": '''"""
Level and tilemap management
"""

import pyray

class Level:
    def __init__(self):
        self.tiles = []
        self.tile_size = 32
        self.create_test_level()
        
    def create_test_level(self):
        """Create a simple test level"""
        # Ground
        for x in range(0, 2000, self.tile_size):
            self.tiles.append((x, 532, self.tile_size, self.tile_size))
            
        # Platforms
        self.tiles.append((300, 400, self.tile_size * 3, self.tile_size))
        self.tiles.append((500, 300, self.tile_size * 3, self.tile_size))
        self.tiles.append((700, 450, self.tile_size * 2, self.tile_size))
        
    def draw(self):
        """Draw level"""
        for tile in self.tiles:
            x, y, w, h = tile
            pyray.draw_rectangle(x, y, w, h, pyray.DARKGREEN)
''',
            "requirements.txt": "pyray>=0.1.0\n",
            "README.md": """# {project_name}

A platformer game created with PyRay.

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python main.py
```

## Controls

- Arrow Keys: Move left/right
- Space: Jump
- ESC: Exit

## License

MIT
"""
        }
    }
}

def create_project(name: str, template: str = "basic", path: Optional[str] = None) -> bool:
    """
    Create a new PyRay project
    
    Args:
        name: Project name
        template: Template to use
        path: Path to create project in (default: current directory)
        
    Returns:
        True if successful
    """
    if template not in TEMPLATES:
        print(f"Error: Unknown template '{template}'")
        print(f"Available templates: {', '.join(TEMPLATES.keys())}")
        return False
        
    # Create project directory
    project_path = Path(path or ".") / name
    if project_path.exists():
        print(f"Error: Directory '{project_path}' already exists")
        return False
        
    try:
        project_path.mkdir(parents=True)
        
        # Create files from template
        template_data = TEMPLATES[template]
        for filename, content in template_data["files"].items():
            file_path = project_path / filename
            
            # Create subdirectories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file with project name substitution
            file_content = content.format(project_name=name)
            file_path.write_text(file_content)
            
        print(f"✓ Created project '{name}' using template '{template}'")
        print(f"  Location: {project_path.absolute()}")
        print(f"\nNext steps:")
        print(f"  cd {name}")
        print(f"  pip install -r requirements.txt")
        print(f"  python main.py")
        
        return True
        
    except Exception as e:
        print(f"Error creating project: {e}")
        return False

def main():
    """Command-line interface for project generator"""
    parser = argparse.ArgumentParser(
        description="PyRay Project Generator - Create new PyRay projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Templates:
  basic      - Basic window with game loop
  game       - Complete game with states and entities  
  platformer - 2D platformer game template

Examples:
  pyray-new my-game
  pyray-new my-game --template platformer
  pyray-new my-game --path ~/projects
"""
    )
    
    parser.add_argument("name", help="Project name")
    parser.add_argument(
        "--template", "-t",
        default="basic",
        choices=TEMPLATES.keys(),
        help="Project template to use (default: basic)"
    )
    parser.add_argument(
        "--path", "-p",
        help="Path to create project in (default: current directory)"
    )
    parser.add_argument(
        "--list-templates", "-l",
        action="store_true",
        help="List available templates"
    )
    
    args = parser.parse_args()
    
    if args.list_templates:
        print("Available templates:")
        for name, data in TEMPLATES.items():
            print(f"  {name:12} - {data['description']}")
        return 0
        
    # Create project
    success = create_project(args.name, args.template, args.path)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
