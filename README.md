# Eli - Minecraft Clone in Python

A basic Minecraft-like game built with Python and Pygame featuring voxel world generation, block placement/breaking, inventory, and crafting systems.

## Features

- **Voxel World Generation**: Procedurally generated terrain using Perlin noise
- **Block System**: Multiple block types (stone, dirt, grass, wood, water, glass, etc.)
- **Player Movement**: WASD movement, jumping, and gravity physics
- **Block Interaction**: Break and place blocks with left/right clicks
- **Inventory System**: Collect and manage items
- **Crafting System**: Craft new items from collected materials
- **3D Rendering**: Perspective-based 3D block rendering

## Installation

1. Clone the repository:
```bash
git clone https://github.com/drdeanputhoff-cloud/Eli.git
cd Eli
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

## Controls

- **E/Q/A/D**: Move forward/backward/left/right
- **SPACE**: Jump
- **Left Click**: Break block
- **Right Click**: Place block
- **I**: Open Inventory
- **C**: Open Crafting Table
- **ESC**: Exit game

## Game Files

- `main.py`: Main game loop and core systems
- `world.py`: World generation and chunk management
- `blocks.py`: Block definitions and properties
- `player.py`: Player character and movement
- `renderer.py`: 3D rendering system
- `inventory.py`: Inventory management
- `crafting.py`: Crafting system and recipes

## Building & Crafting

Open the crafting table (C key) to craft new items from your inventory:

- **Planks**: 1 Oak Wood → 4 Oak Planks
- **Sticks**: 2 Oak Planks → 4 Sticks
- **Crafting Table**: 4 Oak Planks → 1 Crafting Table
- **Chest**: 8 Oak Planks → 1 Chest
- **Wooden Pickaxe**: 3 Oak Planks + 2 Sticks → 1 Wooden Pickaxe
- **Stone Pickaxe**: 3 Cobblestone + 2 Sticks → 1 Stone Pickaxe
- **Furnace**: 8 Cobblestone → 1 Furnace

## Development

This is a basic implementation meant as a learning project. Feel free to expand with:
- Better graphics and textures
- More block types
- Mining level requirements
- Tools system
- Smelting in furnaces
- Multiplayer support
- Improved physics
- Animations

## License

MIT License - Feel free to use and modify!
