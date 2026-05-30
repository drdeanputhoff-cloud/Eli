"""
World generation and management system
Handles voxel chunks, block data, and terrain generation
"""

import numpy as np
from perlin_noise import PerlinNoise
from blocks import Block, BLOCK_TYPES

class Chunk:
    """A chunk is a 16x16x16 section of the world"""
    CHUNK_SIZE = 16
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.blocks = np.zeros((self.CHUNK_SIZE, self.CHUNK_SIZE, self.CHUNK_SIZE), dtype=int)
        self.modified = False
    
    def set_block(self, x, y, z, block_type):
        if 0 <= x < self.CHUNK_SIZE and 0 <= y < self.CHUNK_SIZE and 0 <= z < self.CHUNK_SIZE:
            self.blocks[x, y, z] = block_type
            self.modified = True
    
    def get_block(self, x, y, z):
        if 0 <= x < self.CHUNK_SIZE and 0 <= y < self.CHUNK_SIZE and 0 <= z < self.CHUNK_SIZE:
            return self.blocks[x, y, z]
        return 0
    
    def is_solid(self, x, y, z):
        block_type = self.get_block(x, y, z)
        return block_type != 0  # 0 = air


class World:
    """Main world class managing all chunks and blocks"""
    
    def __init__(self, seed=42, render_distance=3):
        self.seed = seed
        self.render_distance = render_distance
        self.chunks = {}
        self.noise = PerlinNoise(octaves=4, seed=seed)
        self.height_map = {}
        self.generate_initial_world()
    
    def get_chunk_coords(self, x, y, z):
        """Convert world coordinates to chunk coordinates"""
        chunk_x = x // Chunk.CHUNK_SIZE
        chunk_y = y // Chunk.CHUNK_SIZE
        chunk_z = z // Chunk.CHUNK_SIZE
        return (chunk_x, chunk_y, chunk_z)
    
    def get_local_coords(self, x, y, z):
        """Convert world coordinates to local chunk coordinates"""
        local_x = x % Chunk.CHUNK_SIZE
        local_y = y % Chunk.CHUNK_SIZE
        local_z = z % Chunk.CHUNK_SIZE
        return (local_x, local_y, local_z)
    
    def get_chunk(self, chunk_x, chunk_y, chunk_z):
        """Get or create a chunk"""
        key = (chunk_x, chunk_y, chunk_z)
        if key not in self.chunks:
            self.chunks[key] = self.generate_chunk(chunk_x, chunk_y, chunk_z)
        return self.chunks[key]
    
    def generate_chunk(self, chunk_x, chunk_y, chunk_z):
        """Generate a chunk using Perlin noise"""
        chunk = Chunk(chunk_x, chunk_y, chunk_z)
        
        for x in range(Chunk.CHUNK_SIZE):
            for z in range(Chunk.CHUNK_SIZE):
                world_x = chunk_x * Chunk.CHUNK_SIZE + x
                world_z = chunk_z * Chunk.CHUNK_SIZE + z
                
                # Generate height using Perlin noise
                height = self.get_height(world_x, world_z)
                
                for y in range(Chunk.CHUNK_SIZE):
                    world_y = chunk_y * Chunk.CHUNK_SIZE + y
                    
                    if world_y < height - 3:
                        chunk.set_block(x, y, z, BLOCK_TYPES["stone"])
                    elif world_y < height:
                        chunk.set_block(x, y, z, BLOCK_TYPES["dirt"])
                    elif world_y == height:
                        chunk.set_block(x, y, z, BLOCK_TYPES["grass"])
                    elif world_y < 32:  # Water level
                        chunk.set_block(x, y, z, BLOCK_TYPES["water"])
        
        return chunk
    
    def get_height(self, x, z):
        """Generate terrain height at given x, z coordinates"""
        key = (x, z)
        if key not in self.height_map:
            noise_val = self.noise([x * 0.01, z * 0.01])
            height = int((noise_val + 1) * 32 + 40)  # Scale between 40 and 104
            self.height_map[key] = height
        return self.height_map[key]
    
    def set_block(self, x, y, z, block_type):
        """Set a block in the world"""
        chunk_x, chunk_y, chunk_z = self.get_chunk_coords(x, y, z)
        local_x, local_y, local_z = self.get_local_coords(x, y, z)
        
        chunk = self.get_chunk(chunk_x, chunk_y, chunk_z)
        chunk.set_block(local_x, local_y, local_z, block_type)
    
    def get_block(self, x, y, z):
        """Get a block from the world"""
        chunk_x, chunk_y, chunk_z = self.get_chunk_coords(x, y, z)
        local_x, local_y, local_z = self.get_local_coords(x, y, z)
        
        chunk = self.get_chunk(chunk_x, chunk_y, chunk_z)
        return chunk.get_block(local_x, local_y, local_z)
    
    def is_solid(self, x, y, z):
        """Check if a block is solid"""
        if y < 0:
            return True
        block_type = self.get_block(x, y, z)
        return block_type != 0 and block_type != BLOCK_TYPES.get("water", -1)
    
    def get_visible_chunks(self, player_pos):
        """Get chunks within render distance"""
        chunk_x, chunk_y, chunk_z = self.get_chunk_coords(*player_pos)
        visible = []
        
        for dx in range(-self.render_distance, self.render_distance + 1):
            for dy in range(-self.render_distance, self.render_distance + 1):
                for dz in range(-self.render_distance, self.render_distance + 1):
                    visible.append((chunk_x + dx, chunk_y + dy, chunk_z + dz))
        
        return visible
    
    def generate_initial_world(self):
        """Generate initial chunks around origin"""
        for x in range(-2, 3):
            for y in range(-1, 2):
                for z in range(-2, 3):
                    self.get_chunk(x, y, z)
