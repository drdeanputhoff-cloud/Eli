"""
Player character system
Handles player position, movement, jumping, and block interaction
"""

import math
from blocks import BLOCK_TYPES, get_block_by_id

class Player:
    """Represents the player character"""
    
    def __init__(self, world):
        self.world = world
        self.x = 0
        self.y = 100
        self.z = 0
        
        # Player dimensions
        self.width = 0.6
        self.height = 1.8
        self.eye_height = 1.62
        self.crouch_height = 1.2  # Height when crouching
        
        # Movement
        self.velocity_y = 0
        self.is_jumping = False
        self.is_crouching = False
        self.on_ground = False
        self.move_speed = 0.15
        self.crouch_speed = 0.08  # Slower when crouching
        self.jump_power = 0.5
        self.gravity = 0.02
        
        # Rotation
        self.yaw = 0  # Horizontal rotation
        self.pitch = 0  # Vertical rotation
        
        # Selected block type (for placing)
        self.selected_block = BLOCK_TYPES["oak_planks"]
    
    def update(self, world):
        """Update player physics and state"""
        # Apply gravity
        self.velocity_y -= self.gravity
        self.y += self.velocity_y
        
        # Current eye height based on crouching
        current_eye_height = self.crouch_height if self.is_crouching else self.eye_height
        
        # Check collision with ground
        ground_block = world.get_block(int(self.x), int(self.y - current_eye_height/2), int(self.z))
        if world.is_solid(int(self.x), int(self.y - current_eye_height/2 - 1), int(self.z)):
            self.on_ground = True
            self.velocity_y = 0
            self.y = int(self.y - current_eye_height/2) + 2
        else:
            self.on_ground = False
        
        # Clamp player below world height limit
        if self.y > 256:
            self.y = 256
    
    def move_forward(self, world):
        """Move forward relative to player rotation (W key)"""
        speed = self.crouch_speed if self.is_crouching else self.move_speed
        new_x = self.x + math.sin(self.yaw) * speed
        new_z = self.z + math.cos(self.yaw) * speed
        
        if not self.is_colliding(new_x, self.y, new_z, world):
            self.x = new_x
            self.z = new_z
    
    def move_backward(self, world):
        """Move backward relative to player rotation (S key)"""
        speed = self.crouch_speed if self.is_crouching else self.move_speed
        new_x = self.x - math.sin(self.yaw) * speed
        new_z = self.z - math.cos(self.yaw) * speed
        
        if not self.is_colliding(new_x, self.y, new_z, world):
            self.x = new_x
            self.z = new_z
    
    def move_left(self, world):
        """Move left relative to player rotation (A key)"""
        speed = self.crouch_speed if self.is_crouching else self.move_speed
        new_x = self.x + math.sin(self.yaw - math.pi/2) * speed
        new_z = self.z + math.cos(self.yaw - math.pi/2) * speed
        
        if not self.is_colliding(new_x, self.y, new_z, world):
            self.x = new_x
            self.z = new_z
    
    def move_right(self, world):
        """Move right relative to player rotation (D key)"""
        speed = self.crouch_speed if self.is_crouching else self.move_speed
        new_x = self.x + math.sin(self.yaw + math.pi/2) * speed
        new_z = self.z + math.cos(self.yaw + math.pi/2) * speed
        
        if not self.is_colliding(new_x, self.y, new_z, world):
            self.x = new_x
            self.z = new_z
    
    def jump(self):
        """Make the player jump (SPACE key)"""
        if self.on_ground and not self.is_crouching:
            self.velocity_y = self.jump_power
            self.is_jumping = True
            self.on_ground = False
    
    def toggle_crouch(self):
        """Toggle crouching (SHIFT key)"""
        self.is_crouching = not self.is_crouching
    
    def set_crouch(self, crouching):
        """Set crouch state"""
        self.is_crouching = crouching
    
    def is_colliding(self, x, y, z, world):
        """Check if player collides with blocks at given position"""
        # Simple AABB collision detection
        current_height = self.crouch_height if self.is_crouching else self.height
        for dx in [-self.width/2, self.width/2]:
            for dy in [0, current_height]:
                for dz in [-self.width/2, self.width/2]:
                    block_x = int(x + dx)
                    block_y = int(y + dy)
                    block_z = int(z + dz)
                    if world.is_solid(block_x, block_y, block_z):
                        return True
        return False
    
    def break_block(self, world, inventory):
        """Break a block in front of the player (Left click)"""
        # Get the block in front of the player
        reach = 5
        for i in range(1, reach):
            block_x = int(self.x + math.sin(self.yaw) * i)
            block_y = int(self.y - self.pitch * 2)
            block_z = int(self.z + math.cos(self.yaw) * i)
            
            block_type = world.get_block(block_x, block_y, block_z)
            if block_type != 0:  # Found a block
                block_data = get_block_by_id(block_type)
                if block_data.drops:
                    inventory.add_item(block_data.drops)
                world.set_block(block_x, block_y, block_z, 0)  # Remove block
                return
    
    def place_block(self, world, inventory):
        """Place a block in front of the player (Right click)"""
        if not inventory.has_item(self.selected_block):
            return
        
        reach = 5
        for i in range(1, reach):
            block_x = int(self.x + math.sin(self.yaw) * i)
            block_y = int(self.y - self.pitch * 2)
            block_z = int(self.z + math.cos(self.yaw) * i)
            
            block_type = world.get_block(block_x, block_y, block_z)
            if block_type != 0:  # Found a solid block
                # Place block next to it
                place_x = int(self.x + math.sin(self.yaw) * (i + 1))
                place_z = int(self.z + math.cos(self.yaw) * (i + 1))
                
                world.set_block(place_x, block_y, place_z, self.selected_block)
                inventory.remove_item(self.selected_block)
                return
    
    def get_position(self):
        """Get player's current position"""
        return (self.x, self.y, self.z)
    
    def get_eye_position(self):
        """Get position of player's eyes"""
        current_eye_height = self.crouch_height if self.is_crouching else self.eye_height
        return (self.x, self.y - current_eye_height/2, self.z)
