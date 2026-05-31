"""
WARRIOR ADVENTURE 1
A 2D Platformer Game with 1000+ Levels, Boss Battles, and Epic Adventures!
Created for aspiring game developers everywhere!

Controls:
A/D or Arrows - Move Left/Right
W/Up Arrow - Jump
SPACE - Attack with Sword
ESC - Quit Game
"""

import pygame
import sys
import math
import random

# ============================================================================
# INITIALIZE PYGAME
# ============================================================================

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
DARK_RED = (139, 0, 0)
ORANGE = (255, 165, 0)
DARK_GREEN = (34, 139, 34)
SKIN = (255, 200, 150)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("WARRIOR ADVENTURE 1")
clock = pygame.time.Clock()
font_huge = pygame.font.Font(None, 80)
font_large = pygame.font.Font(None, 60)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

# ============================================================================
# PLAYER CLASS
# ============================================================================

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 40
        self.height = 60
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(SKIN)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.6
        self.max_fall_speed = 15
        self.on_ground = False
        self.jump_power = -12
        self.move_speed = 5
        
        self.health = 100
        self.max_health = 100
        self.score = 0
        self.attack_cooldown = 0
        self.is_attacking = False
        self.attack_range = 50
        self.facing_right = True
        
    def draw_warrior(self, surface):
        pygame.draw.rect(surface, SKIN, (5, 15, 30, 25))
        pygame.draw.circle(surface, SKIN, (20, 10), 7)
        pygame.draw.rect(surface, BROWN, (8, 40, 6, 20))
        pygame.draw.rect(surface, BROWN, (26, 40, 6, 20))
        
        if self.is_attacking:
            if self.facing_right:
                pygame.draw.line(surface, SKIN, (35, 22), (50, 15), 4)
            else:
                pygame.draw.line(surface, SKIN, (5, 22), (-10, 15), 4)
        else:
            pygame.draw.line(surface, SKIN, (35, 22), (45, 28), 3)
            pygame.draw.line(surface, SKIN, (5, 22), (-5, 28), 3)
        
        if self.is_attacking:
            if self.facing_right:
                pygame.draw.line(surface, YELLOW, (50, 15), (55, 5), 4)
            else:
                pygame.draw.line(surface, YELLOW, (-10, 15), (-15, 5), 4)
    
    def update(self, platforms, enemies, coins, boxes, level_end):
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x = -self.move_speed
            self.facing_right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x = self.move_speed
            self.facing_right = True
        
        if keys[pygame.K_SPACE] and self.attack_cooldown <= 0:
            self.is_attacking = True
            self.attack_cooldown = 15
            self.attack_enemies(enemies)
        
        self.attack_cooldown -= 1
        if self.attack_cooldown < 0:
            self.is_attacking = False
        
        self.vel_y = min(self.vel_y + self.gravity, self.max_fall_speed)
        self.on_ground = False
        
        self.rect.x += self.vel_x
        self.check_collisions(platforms, boxes)
        
        self.rect.y += self.vel_y
        self.check_collisions(platforms, boxes)
        
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
        
        # Collect coins
        for coin in coins[:]:
            if self.rect.colliderect(coin.rect):
                self.score += coin.value
                coins.remove(coin)
        
        # Check level end
        if self.rect.colliderect(level_end.rect):
            return True
        
        if self.rect.y > SCREEN_HEIGHT + 50:
            self.health = 0
        
        return False
    
    def check_collisions(self, platforms, boxes):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
                elif self.vel_x > 0:
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0:
                    self.rect.left = platform.rect.right
        
        for box in boxes:
            if self.rect.colliderect(box.rect):
                if self.vel_y > 0:
                    self.rect.bottom = box.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = box.rect.bottom
                    self.vel_y = 0
                elif self.vel_x > 0:
                    self.rect.right = box.rect.left
                elif self.vel_x < 0:
                    self.rect.left = box.rect.right
    
    def attack_enemies(self, enemies):
        for enemy in enemies:
            dx = enemy.rect.centerx - self.rect.centerx
            dy = enemy.rect.centery - self.rect.centery
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < self.attack_range:
                if (self.facing_right and dx > 0) or (not self.facing_right and dx < 0):
                    enemy.health -= 30
    
    def draw(self):
        self.image.fill(WHITE)
        if not self.facing_right:
            flipped_surface = pygame.Surface((self.width, self.height))
            flipped_surface.fill(WHITE)
            self.draw_warrior(flipped_surface)
            self.image = pygame.transform.flip(flipped_surface, True, False)
        else:
            self.draw_warrior(self.image)

# ============================================================================
# ENEMY CLASS
# ============================================================================

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type="goblin"):
        super().__init__()
        self.width = 35
        self.height = 45
        self.enemy_type = enemy_type
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.vel_y = 0
        self.gravity = 0.6
        self.vel_x = random.choice([-2, 2])
        
        self.health = 50 if enemy_type == "goblin" else 80
        self.max_health = self.health
        self.move_range = 150
        self.start_x = x
        self.patrol_direction = 1
        
    def draw_enemy(self, surface):
        if self.enemy_type == "goblin":
            pygame.draw.rect(surface, DARK_GREEN, (5, 15, 25, 25))
            pygame.draw.circle(surface, DARK_GREEN, (17, 10), 6)
            pygame.draw.rect(surface, RED, (17, 12), (1, 1))
            pygame.draw.line(surface, DARK_GREEN, (30, 20), (40, 22), 3)
        else:
            pygame.draw.rect(surface, RED, (5, 12, 25, 30))
            pygame.draw.circle(surface, RED, (17, 7), 7)
            pygame.draw.circle(surface, WHITE, (14, 6), 2)
            pygame.draw.circle(surface, BLACK, (14, 6), 1)
            pygame.draw.circle(surface, WHITE, (20, 6), 2)
            pygame.draw.circle(surface, BLACK, (20, 6), 1)
    
    def update(self, platforms, boxes):
        self.vel_x = 2 * self.patrol_direction
        
        if abs(self.rect.x - self.start_x) > self.move_range:
            self.patrol_direction *= -1
        
        self.vel_y = min(self.vel_y + self.gravity, 15)
        
        self.rect.x += self.vel_x
        self.check_collisions(platforms, boxes)
        
        self.rect.y += self.vel_y
        self.check_collisions(platforms, boxes)
        
        return self.health <= 0
    
    def check_collisions(self, platforms, boxes):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                elif self.vel_x > 0:
                    self.patrol_direction = -1
                elif self.vel_x < 0:
                    self.patrol_direction = 1
        
        for box in boxes:
            if self.rect.colliderect(box.rect):
                if self.vel_y > 0:
                    self.rect.bottom = box.rect.top
                    self.vel_y = 0
                elif self.vel_x > 0:
                    self.patrol_direction = -1
                elif self.vel_x < 0:
                    self.patrol_direction = 1
    
    def draw(self):
        self.image.fill(WHITE)
        self.draw_enemy(self.image)
        health_percentage = self.health / self.max_health
        pygame.draw.rect(self.image, RED, (2, 2, self.width - 4, 4))
        pygame.draw.rect(self.image, GREEN, (2, 2, (self.width - 4) * health_percentage, 4))

# ============================================================================
# BOSS CLASS
# ============================================================================

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 80
        self.height = 100
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.vel_y = 0
        self.gravity = 0.6
        self.vel_x = random.choice([-2, 2])
        
        self.health = 500
        self.max_health = 500
        self.move_range = 300
        self.start_x = x
        self.patrol_direction = 1
        self.attack_timer = 0
        self.attack_interval = 60
        
    def draw_boss(self, surface):
        # Large boss body
        pygame.draw.rect(surface, DARK_RED, (5, 20, 70, 60))
        pygame.draw.circle(surface, DARK_RED, (40, 15), 12)
        
        # Eyes
        pygame.draw.circle(surface, YELLOW, (30, 12), 3)
        pygame.draw.circle(surface, YELLOW, (50, 12), 3)
        pygame.draw.circle(surface, BLACK, (30, 12), 1)
        pygame.draw.circle(surface, BLACK, (50, 12), 1)
        
        # Spikes
        for i in range(0, 70, 20):
            pygame.draw.polygon(surface, ORANGE, [(i+5, 20), (i+10, 5), (i+15, 20)])
        
        # Attack glow
        if self.attack_timer > self.attack_interval - 20:
            pygame.draw.circle(surface, YELLOW, (40, 50), 40, 2)
    
    def update(self, platforms, boxes):
        self.attack_timer += 1
        
        self.vel_x = 1.5 * self.patrol_direction
        
        if abs(self.rect.x - self.start_x) > self.move_range:
            self.patrol_direction *= -1
        
        self.vel_y = min(self.vel_y + self.gravity, 15)
        
        self.rect.x += self.vel_x
        self.check_collisions(platforms, boxes)
        
        self.rect.y += self.vel_y
        self.check_collisions(platforms, boxes)
        
        return self.health <= 0
    
    def check_collisions(self, platforms, boxes):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                elif self.vel_x > 0:
                    self.patrol_direction = -1
                elif self.vel_x < 0:
                    self.patrol_direction = 1
        
        for box in boxes:
            if self.rect.colliderect(box.rect):
                if self.vel_y > 0:
                    self.rect.bottom = box.rect.top
                    self.vel_y = 0
    
    def draw(self):
        self.image.fill(WHITE)
        self.draw_boss(self.image)
        health_percentage = self.health / self.max_health
        pygame.draw.rect(self.image, RED, (2, 2, self.width - 4, 4))
        pygame.draw.rect(self.image, GREEN, (2, 2, (self.width - 4) * health_percentage, 4))

# ============================================================================
# PLATFORM CLASS
# ============================================================================

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, platform_type="normal"):
        super().__init__()
        self.width = width
        self.height = height
        self.platform_type = platform_type
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        
        if platform_type == "normal":
            self.image.fill(BROWN)
            pygame.draw.rect(self.image, ORANGE, (0, 0, width, height), 3)
            for i in range(0, width, 20):
                for j in range(0, height, 20):
                    pygame.draw.line(self.image, ORANGE, (i, 0), (i, height), 1)
                    pygame.draw.line(self.image, ORANGE, (0, j), (width, j), 1)
        elif platform_type == "spike":
            self.image.fill(RED)
            for i in range(0, width, 15):
                pygame.draw.polygon(self.image, ORANGE, [(i, height), (i+7, 0), (i+15, height)])

# ============================================================================
# DROPPING BOX CLASS
# ============================================================================

class DroppingBox(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 50
        self.height = 50
        self.start_y = y
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.drop_timer = 0
        self.drop_cycle = 200  # 10 seconds at 60 FPS = 600 frames, but we'll use 200 for faster gameplay
        self.is_falling = False
        self.vel_y = 0
        self.gravity = 0.8
        
    def update(self):
        # Update drop cycle
        self.drop_timer += 1
        
        # Drop every 10 seconds, fall for 5 seconds, go back up for 5 seconds
        cycle_pos = self.drop_timer % self.drop_cycle
        
        if cycle_pos < self.drop_cycle * 0.5:  # Falling phase
            self.is_falling = True
            self.vel_y = 5
        else:  # Going back up phase
            self.is_falling = False
            self.vel_y = -5
        
        self.rect.y += self.vel_y
        
        # Clamp to start position when going back up
        if self.rect.y < self.start_y:
            self.rect.y = self.start_y
            self.vel_y = 0
        
        # Stop falling at ground
        if self.rect.y > SCREEN_HEIGHT - 50:
            self.rect.y = SCREEN_HEIGHT - 50
    
    def draw(self):
        self.image.fill(DARK_RED)
        pygame.draw.rect(self.image, RED, (0, 0, self.width, self.height), 3)
        # Draw a skull or danger symbol
        pygame.draw.circle(self.image, YELLOW, (15, 15), 5)
        pygame.draw.circle(self.image, YELLOW, (35, 15), 5)
        pygame.draw.circle(self.image, YELLOW, (25, 30), 5)

# ============================================================================
# COIN CLASS
# ============================================================================

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, trapped=False):
        super().__init__()
        self.width = 15
        self.height = 15
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(YELLOW)
        pygame.draw.circle(self.image, ORANGE, (7, 7), 6)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.value = 10
        self.trapped = trapped
        
    def draw(self):
        if self.trapped:
            # Draw X over trapped coins
            pygame.draw.line(self.image, RED, (0, 0), (15, 15), 2)
            pygame.draw.line(self.image, RED, (15, 0), (0, 15), 2)

# ============================================================================
# LEVEL END FLAG
# ============================================================================

class LevelEnd(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 40
        self.height = 80
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(topleft=(x, y))
        
        pygame.draw.rect(self.image, BROWN, (35, 0, 5, 80))
        pygame.draw.polygon(self.image, GREEN, [(40, 10), (40, 25), (60, 17)])
        pygame.draw.circle(self.image, YELLOW, (40, 30), 4)

# ============================================================================
# LEVEL MANAGER
# ============================================================================

class Level:
    def __init__(self, level_num):
        self.level_num = level_num
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.boxes = pygame.sprite.Group()
        self.boss = None
        self.player = None
        self.level_end = None
        self.is_boss_level = (level_num % 100 == 0)  # Boss every 100 levels
        
        self.create_level()
    
    def create_level(self):
        # Ground
        for x in range(0, SCREEN_WIDTH, 40):
            self.platforms.add(Platform(x, SCREEN_HEIGHT - 40, 40, 40, "normal"))
        
        if self.is_boss_level:
            self.create_boss_level()
        else:
            self.create_normal_level()
    
    def create_normal_level(self):
        # Generate random platforms based on level difficulty
        difficulty = min(self.level_num // 10, 10)  # Increase difficulty every 10 levels
        
        # More platforms and enemies as level increases
        num_platforms = 3 + (self.level_num // 20)
        num_enemies = 1 + (self.level_num // 50)
        num_coins = 5 + (self.level_num // 10)
        num_boxes = min(3 + (self.level_num // 30), 8)
        num_spikes = (self.level_num // 40)
        
        # Create platforms
        platform_y_positions = []
        for i in range(num_platforms):
            y = 500 - (i * 100)
            x = random.randint(50, SCREEN_WIDTH - 250)
            width = random.randint(150, 350)
            self.platforms.add(Platform(x, y, width, 30, "normal"))
            platform_y_positions.append((x, y, width))
        
        # Add spike platforms
        for i in range(num_spikes):
            y = 300 - random.randint(0, 100)
            x = random.randint(50, SCREEN_WIDTH - 150)
            self.platforms.add(Platform(x, y, 100, 30, "spike"))
        
        # Create enemies
        for i in range(num_enemies):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, 400)
            enemy_type = "goblin" if random.random() > 0.3 else "orc"
            self.enemies.add(Enemy(x, y, enemy_type))
        
        # Create coins (some trapped in boxes)
        for i in range(num_coins):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, 400)
            trapped = random.random() < 0.2  # 20% chance of being trapped
            self.coins.add(Coin(x, y, trapped))
        
        # Create dropping boxes
        for i in range(num_boxes):
            x = random.randint(150, SCREEN_WIDTH - 150)
            y = random.randint(100, 300)
            self.boxes.add(DroppingBox(x, y))
        
        # Player start
        self.player = Player(50, 450)
        
        # Level end
        self.level_end = LevelEnd(1050, 450)
    
    def create_boss_level(self):
        # Boss level setup
        self.platforms.add(Platform(100, 480, 150, 30, "normal"))
        self.platforms.add(Platform(500, 420, 150, 30, "normal"))
        self.platforms.add(Platform(900, 420, 150, 30, "normal"))
        self.platforms.add(Platform(300, 350, 200, 30, "normal"))
        self.platforms.add(Platform(700, 350, 200, 30, "normal"))
        
        # Create coins as rewards
        for i in range(20):
            self.coins.add(Coin(random.randint(100, 1100), random.randint(100, 400)))
        
        # Create the boss
        self.boss = Boss(SCREEN_WIDTH // 2 - 40, 250)
        
        self.player = Player(50, 450)
        self.level_end = LevelEnd(1050, 250)
    
    def update(self):
        level_complete = self.player.update(self.platforms, self.enemies, self.coins, self.boxes, self.level_end)
        
        # Update boxes
        for box in self.boxes:
            box.update()
        
        if self.is_boss_level:
            # Boss level
            if self.boss.update(self.platforms, self.boxes):
                self.player.score += 500
                return level_complete
            
            # Check collision with boss
            if self.player.rect.colliderect(self.boss.rect):
                self.player.health -= 1
            
            # Draw boss attack warning
            if self.boss.attack_timer > self.boss.attack_interval - 20:
                pass  # Visual effect handled in draw
        else:
            # Normal enemies
            to_remove = []
            for enemy in self.enemies:
                if enemy.update(self.platforms, self.boxes):
                    to_remove.append(enemy)
                    self.player.score += 50
            for enemy in to_remove:
                self.enemies.remove(enemy)
            
            for enemy in self.enemies:
                if self.player.rect.colliderect(enemy.rect):
                    self.player.health -= 0.5
        
        return level_complete
    
    def draw(self, surface):
        for platform in self.platforms:
            surface.blit(platform.image, platform.rect)
        
        for box in self.boxes:
            box.draw()
            surface.blit(box.image, box.rect)
        
        for coin in self.coins:
            coin.draw()
            surface.blit(coin.image, coin.rect)
        
        for enemy in self.enemies:
            enemy.draw()
            surface.blit(enemy.image, enemy.rect)
        
        if self.is_boss_level and self.boss:
            self.boss.draw()
            surface.blit(self.boss.image, self.boss.rect)
        
        surface.blit(self.level_end.image, self.level_end.rect)
        
        self.player.draw()
        surface.blit(self.player.image, self.player.rect)

# ============================================================================
# GAME MANAGER
# ============================================================================

class Game:
    def __init__(self):
        self.state = "menu"
        self.current_level = 1
        self.level = None
        self.running = True
        self.total_score = 0
    
    def start_game(self):
        self.state = "playing"
        self.current_level = 1
        self.total_score = 0
        self.level = Level(self.current_level)
    
    def next_level(self):
        self.total_score += self.level.player.score
        self.current_level += 1
        
        if self.current_level > 1000:
            self.state = "ultimate_win"
        else:
            self.level = Level(self.current_level)
            self.state = "playing"
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if self.state == "menu" and event.key == pygame.K_SPACE:
                    self.start_game()
                if self.state == "game_over" and event.key == pygame.K_SPACE:
                    self.start_game()
                if self.state == "level_complete" and event.key == pygame.K_SPACE:
                    self.next_level()
                if self.state == "ultimate_win" and event.key == pygame.K_SPACE:
                    self.start_game()
    
    def update(self):
        if self.state == "playing":
            level_complete = self.level.update()
            
            if self.level.player.health <= 0:
                self.state = "game_over"
            elif level_complete:
                self.state = "level_complete"
    
    def draw(self):
        screen.fill(CYAN)
        
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "playing":
            self.level.draw(screen)
            self.draw_hud()
        elif self.state == "game_over":
            self.draw_game_over()
        elif self.state == "level_complete":
            self.draw_level_complete()
        elif self.state == "ultimate_win":
            self.draw_ultimate_win()
    
    def draw_menu(self):
        title = font_huge.render("WARRIOR", True, RED)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        title2 = font_huge.render("ADVENTURE 1", True, ORANGE)
        screen.blit(title2, (SCREEN_WIDTH // 2 - title2.get_width() // 2, 130))
        
        subtitle = font_medium.render("1000+ EPIC LEVELS AWAIT!", True, YELLOW)
        screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 230))
        
        controls = [
            "A/D or ARROWS - Move | W/UP - Jump | SPACE - Attack",
            "Defeat enemies, collect coins, avoid traps!",
            "Boss battles every 100 levels!",
            "Can you reach level 1000?"
        ]
        
        y = 310
        for control in controls:
            text = font_small.render(control, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y))
            y += 35
        
        start = font_medium.render("Press SPACE to Start Your Adventure!", True, GREEN)
        screen.blit(start, (SCREEN_WIDTH // 2 - start.get_width() // 2, 550))
    
    def draw_hud(self):
        health_text = font_small.render(f"Health: {int(self.level.player.health)}", True, RED)
        screen.blit(health_text, (10, 10))
        
        level_text = font_small.render(f"Level: {self.current_level}", True, WHITE)
        screen.blit(level_text, (10, 50))
        
        score_text = font_small.render(f"Score: {self.level.player.score}", True, YELLOW)
        screen.blit(score_text, (SCREEN_WIDTH - 300, 10))
        
        total_score_text = font_small.render(f"Total: {self.total_score + self.level.player.score}", True, YELLOW)
        screen.blit(total_score_text, (SCREEN_WIDTH - 300, 50))
        
        if self.level.is_boss_level:
            boss_text = font_medium.render("BOSS LEVEL!", True, RED)
            screen.blit(boss_text, (SCREEN_WIDTH // 2 - boss_text.get_width() // 2, 10))
    
    def draw_game_over(self):
        game_over_text = font_large.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 100))
        
        level_text = font_medium.render(f"Reached Level: {self.current_level}", True, YELLOW)
        screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 220))
        
        score_text = font_medium.render(f"Level Score: {self.level.player.score}", True, YELLOW)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 280))
        
        total_text = font_medium.render(f"Total Score: {self.total_score + self.level.player.score}", True, ORANGE)
        screen.blit(total_text, (SCREEN_WIDTH // 2 - total_text.get_width() // 2, 340))
        
        restart = font_medium.render("Press SPACE to Try Again", True, GREEN)
        screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 480))
    
    def draw_level_complete(self):
        complete_text = font_large.render("LEVEL COMPLETE!", True, GREEN)
        screen.blit(complete_text, (SCREEN_WIDTH // 2 - complete_text.get_width() // 2, 100))
        
        level_text = font_medium.render(f"Level {self.current_level}", True, YELLOW)
        screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 220))
        
        score_text = font_medium.render(f"Score: {self.level.player.score}", True, YELLOW)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 280))
        
        next_level = font_medium.render("Press SPACE for Next Adventure", True, GREEN)
        screen.blit(next_level, (SCREEN_WIDTH // 2 - next_level.get_width() // 2, 480))
    
    def draw_ultimate_win(self):
        win_text = font_large.render("YOU ARE A LEGEND!", True, YELLOW)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, 80))
        
        win_text2 = font_medium.render("You conquered all 1000 levels!", True, ORANGE)
        screen.blit(win_text2, (SCREEN_WIDTH // 2 - win_text2.get_width() // 2, 200))
        
        score_text = font_medium.render(f"Final Score: {self.total_score}", True, GREEN)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))
        
        thanks = font_small.render("Thank you for playing WARRIOR ADVENTURE 1!", True, WHITE)
        screen.blit(thanks, (SCREEN_WIDTH // 2 - thanks.get_width() // 2, 380))
        
        restart = font_medium.render("Press SPACE to Play Again", True, CYAN)
        screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 500))
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    game = Game()
    game.run()
