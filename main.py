"""
Minecraft-like Game in Python
Main entry point for the game
"""

import pygame
import sys
from world import World
from player import Player
from renderer import Renderer
from inventory import Inventory
from crafting import CraftingTable

class Game:
    def __init__(self):
        pygame.init()
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Eli - Minecraft Clone")
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        
        # Initialize game components
        self.world = World(seed=42)
        self.player = Player(self.world)
        self.renderer = Renderer(self.screen, self.width, self.height)
        self.inventory = Inventory()
        self.crafting_table = CraftingTable()
        
        # Game state
        self.show_inventory = False
        self.show_crafting = False
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_i:
                    self.show_inventory = not self.show_inventory
                if event.key == pygame.K_c:
                    self.show_crafting = not self.show_crafting
                if event.key == pygame.K_e:
                    self.player.move_forward(self.world)
                if event.key == pygame.K_q:
                    self.player.move_backward(self.world)
                if event.key == pygame.K_a:
                    self.player.move_left(self.world)
                if event.key == pygame.K_d:
                    self.player.move_right(self.world)
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click - break block
                    self.player.break_block(self.world, self.inventory)
                if event.button == 3:  # Right click - place block
                    self.player.place_block(self.world, self.inventory)
    
    def update(self):
        self.player.update(self.world)
        
    def draw(self):
        self.screen.fill((135, 206, 235))  # Sky blue
        
        # Draw world
        self.renderer.draw_world(self.world, self.player)
        
        # Draw HUD
        self.draw_hud()
        
        # Draw inventory if open
        if self.show_inventory:
            self.draw_inventory()
            
        # Draw crafting if open
        if self.show_crafting:
            self.draw_crafting()
        
        pygame.display.flip()
    
    def draw_hud(self):
        # Crosshair
        center_x, center_y = self.width // 2, self.height // 2
        pygame.draw.line(self.screen, (255, 255, 255), 
                        (center_x - 10, center_y), (center_x + 10, center_y), 2)
        pygame.draw.line(self.screen, (255, 255, 255), 
                        (center_x, center_y - 10), (center_x, center_y + 10), 2)
        
        # Selected item
        selected_text = self.small_font.render(
            f"Selected: {self.inventory.get_selected_item()}", True, (255, 255, 255))
        self.screen.blit(selected_text, (10, 10))
        
        # Controls
        controls = [
            "E/Q/A/D: Move | SPACE: Jump | I: Inventory | C: Craft",
            "Left Click: Break | Right Click: Place | ESC: Exit"
        ]
        for i, text in enumerate(controls):
            control_text = self.small_font.render(text, True, (255, 255, 255))
            self.screen.blit(control_text, (10, 50 + i * 30))
    
    def draw_inventory(self):
        inv_width, inv_height = 400, 300
        inv_x = (self.width - inv_width) // 2
        inv_y = (self.height - inv_height) // 2
        
        # Draw semi-transparent background
        s = pygame.Surface((inv_width, inv_height))
        s.set_alpha(200)
        s.fill((50, 50, 50))
        self.screen.blit(s, (inv_x, inv_y))
        
        # Draw border
        pygame.draw.rect(self.screen, (255, 255, 255), 
                        (inv_x, inv_y, inv_width, inv_height), 3)
        
        # Title
        title = self.font.render("Inventory", True, (255, 255, 255))
        self.screen.blit(title, (inv_x + 20, inv_y + 20))
        
        # Draw items
        items = self.inventory.get_all_items()
        y_offset = inv_y + 80
        for item, count in items.items():
            item_text = self.small_font.render(f"{item}: {count}", True, (200, 200, 200))
            self.screen.blit(item_text, (inv_x + 40, y_offset))
            y_offset += 30
    
    def draw_crafting(self):
        craft_width, craft_height = 500, 400
        craft_x = (self.width - craft_width) // 2
        craft_y = (self.height - craft_height) // 2
        
        # Draw semi-transparent background
        s = pygame.Surface((craft_width, craft_height))
        s.set_alpha(200)
        s.fill((60, 40, 20))
        self.screen.blit(s, (craft_x, craft_y))
        
        # Draw border
        pygame.draw.rect(self.screen, (139, 69, 19), 
                        (craft_x, craft_y, craft_width, craft_height), 3)
        
        # Title
        title = self.font.render("Crafting Table", True, (255, 200, 100))
        self.screen.blit(title, (craft_x + 20, craft_y + 20))
        
        # Draw recipes
        recipes = self.crafting_table.get_recipes()
        y_offset = craft_y + 80
        for i, (recipe, result) in enumerate(recipes.items()):
            recipe_text = self.small_font.render(
                f"{i+1}. {recipe} -> {result}", True, (200, 200, 100))
            self.screen.blit(recipe_text, (craft_x + 40, y_offset))
            y_offset += 30
        
        # Instructions
        instruction = self.small_font.render(
            "Press number to craft (if ingredients available)", True, (150, 150, 150))
        self.screen.blit(instruction, (craft_x + 20, craft_y + craft_height - 40))
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
