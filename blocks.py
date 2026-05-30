"""
Block definitions and properties
Defines all block types and their characteristics
"""

class Block:
    """Represents a block type in the world"""
    
    def __init__(self, block_id, name, color, hardness=1.0, drops=None):
        self.id = block_id
        self.name = name
        self.color = color
        self.hardness = hardness  # Time to break in seconds
        self.drops = drops or name  # What item drops when broken
    
    def __repr__(self):
        return f"Block({self.name})"

# Define all block types
BLOCK_TYPES = {
    "air": 0,
    "stone": 1,
    "dirt": 2,
    "grass": 3,
    "oak_wood": 4,
    "oak_leaves": 5,
    "sand": 6,
    "water": 7,
    "glass": 8,
    "cobblestone": 9,
    "oak_planks": 10,
    "crafting_table": 11,
    "furnace": 12,
    "chest": 13,
}

# Block properties database
BLOCK_PROPERTIES = {
    0: Block(0, "air", (135, 206, 235), hardness=0),
    1: Block(1, "stone", (128, 128, 128), hardness=1.5, drops="cobblestone"),
    2: Block(2, "dirt", (139, 90, 43), hardness=0.5, drops="dirt"),
    3: Block(3, "grass", (34, 139, 34), hardness=0.6, drops="dirt"),
    4: Block(4, "oak_wood", (139, 69, 19), hardness=2.0, drops="oak_wood"),
    5: Block(5, "oak_leaves", (34, 139, 34), hardness=0.2, drops="oak_leaves"),
    6: Block(6, "sand", (238, 214, 175), hardness=0.5, drops="sand"),
    7: Block(7, "water", (30, 144, 255), hardness=0, drops=None),
    8: Block(8, "glass", (173, 216, 230), hardness=0.3, drops=None),
    9: Block(9, "cobblestone", (112, 112, 112), hardness=2.0, drops="cobblestone"),
    10: Block(10, "oak_planks", (160, 82, 45), hardness=2.0, drops="oak_planks"),
    11: Block(11, "crafting_table", (139, 69, 19), hardness=2.5, drops="crafting_table"),
    12: Block(12, "furnace", (64, 64, 64), hardness=3.5, drops="furnace"),
    13: Block(13, "chest", (139, 69, 19), hardness=2.5, drops="chest"),
}

def get_block_by_id(block_id):
    """Get block properties by ID"""
    return BLOCK_PROPERTIES.get(block_id, BLOCK_PROPERTIES[0])

def get_block_by_name(name):
    """Get block ID by name"""
    return BLOCK_TYPES.get(name, 0)

def is_solid(block_id):
    """Check if a block is solid"""
    return block_id not in [0, 7]  # air and water are not solid

def is_transparent(block_id):
    """Check if a block is transparent"""
    return block_id in [0, 5, 7, 8]  # air, leaves, water, glass
