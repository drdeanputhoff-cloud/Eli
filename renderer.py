"""
Rendering system
Handles 3D projection and block rendering
"""

import pygame
import math
from blocks import get_block_by_id, is_transparent

class Renderer:
    """Renders the 3D voxel world"""
    
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.fov = 70  # Field of view
        self.near_plane = 0.1
        self.far_plane = 200
    
    def project_point(self, x, y, z, camera_x, camera_y, camera_z, yaw, pitch):
        """Project a 3D point onto 2D screen"""
        # Translate to camera space
        dx = x - camera_x
        dy = y - camera_y
        dz = z - camera_z
        
        # Rotate by yaw (horizontal)
        cos_yaw = math.cos(yaw)
        sin_yaw = math.sin(yaw)
        rotated_x = dx * cos_yaw - dz * sin_yaw
        rotated_z = dx * sin_yaw + dz * cos_yaw
        
        # Rotate by pitch (vertical)
        cos_pitch = math.cos(pitch)
        sin_pitch = math.sin(pitch)
        rotated_y = dy * cos_pitch - rotated_z * sin_pitch
        rotated_z_final = dy * sin_pitch + rotated_z * cos_pitch
        
        # Perspective projection
        if rotated_z_final <= self.near_plane:
            return None
        
        scale = self.height / (2 * math.tan(math.radians(self.fov / 2)))
        screen_x = self.width / 2 + (rotated_x / rotated_z_final) * scale
        screen_y = self.height / 2 - (rotated_y / rotated_z_final) * scale
        
        return (screen_x, screen_y, rotated_z_final)
    
    def draw_block(self, world, bx, by, bz, camera_pos, yaw, pitch):
        """Draw a single block"""
        block_type = world.get_block(bx, by, bz)
        if block_type == 0:  # Skip air blocks
            return
        
        block_data = get_block_by_id(block_type)
        block_size = 1
        
        # Define cube vertices (relative to block)
        vertices = [
            (bx, by, bz),
            (bx + block_size, by, bz),
            (bx + block_size, by + block_size, bz),
            (bx, by + block_size, bz),
            (bx, by, bz + block_size),
            (bx + block_size, by, bz + block_size),
            (bx + block_size, by + block_size, bz + block_size),
            (bx, by + block_size, bz + block_size),
        ]
        
        # Project vertices
        projected = []
        for v in vertices:
            proj = self.project_point(v[0], v[1], v[2], camera_pos[0], camera_pos[1], camera_pos[2], yaw, pitch)
            if proj:
                projected.append(proj)
            else:
                projected.append(None)
        
        # Draw cube faces if all vertices are visible
        if all(p is not None for p in projected):
            # Choose color based on brightness
            r, g, b = block_data.color
            
            # Draw front face
            front_points = [projected[i][:2] for i in [0, 1, 2, 3]]
            if len(front_points) == 4:
                pygame.draw.polygon(self.screen, (int(r*0.8), int(g*0.8), int(b*0.8)), front_points)
            
            # Draw top face (lighter)
            top_points = [projected[i][:2] for i in [3, 2, 6, 7]]
            if len(top_points) == 4:
                pygame.draw.polygon(self.screen, block_data.color, top_points)
            
            # Draw side face (darker)
            side_points = [projected[i][:2] for i in [1, 5, 6, 2]]
            if len(side_points) == 4:
                pygame.draw.polygon(self.screen, (int(r*0.6), int(g*0.6), int(b*0.6)), side_points)
    
    def draw_world(self, world, player):
        """Draw all visible blocks in the world"""
        camera_pos = player.get_eye_position()
        
        # Get visible chunks
        visible_chunks = world.get_visible_chunks(camera_pos)
        
        # Collect all blocks to render with depth
        blocks_to_render = []
        
        for chunk_coords in visible_chunks:
            chunk = world.get_chunk(*chunk_coords)
            cx, cy, cz = chunk_coords
            
            for x in range(16):
                for y in range(16):
                    for z in range(16):
                        block_type = chunk.get_block(x, y, z)
                        if block_type == 0:
                            continue
                        
                        world_x = cx * 16 + x
                        world_y = cy * 16 + y
                        world_z = cz * 16 + z
                        
                        # Calculate distance to player
                        dx = world_x - camera_pos[0]
                        dy = world_y - camera_pos[1]
                        dz = world_z - camera_pos[2]
                        distance = dx*dx + dy*dy + dz*dz
                        
                        # Only render blocks within render distance
                        if distance < 2000:  # ~45 block radius
                            blocks_to_render.append((distance, world_x, world_y, world_z))
        
        # Sort by distance (farthest first for painter's algorithm)
        blocks_to_render.sort(reverse=True)
        
        # Draw blocks from back to front
        for _, bx, by, bz in blocks_to_render:
            self.draw_block(world, bx, by, bz, camera_pos, player.yaw, player.pitch)
    
    def draw_crosshair(self):
        """Draw aiming crosshair at screen center"""
        center_x = self.width // 2
        center_y = self.height // 2
        size = 10
        color = (255, 255, 255)
        
        pygame.draw.line(self.screen, color, 
                        (center_x - size, center_y), 
                        (center_x + size, center_y), 2)
        pygame.draw.line(self.screen, color, 
                        (center_x, center_y - size), 
                        (center_x, center_y + size), 2)
