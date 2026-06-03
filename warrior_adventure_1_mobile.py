"""
WARRIOR ADVENTURE 1 - MOBILE VERSION
A 2D Platformer Game with 1000+ Levels, Boss Battles, and Epic Adventures!
Optimized for Mobile Devices (Touch Controls)

Mobile Controls:
- Tap LEFT side of screen to move left
- Tap RIGHT side of screen to move right
- Tap TOP of screen to jump
- Tap CENTER to attack with sword
"""

import pygame
import sys
import math
import random

# ============================================================================
# INITIALIZE PYGAME
# ============================================================================

pygame.init()

# Mobile optimized screen size
SCREEN_WIDTH = 800
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
LIGHT_GRAY = (200, 200, 200)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("WARRIOR ADVENTURE 1 - MOBILE")
clock = pygame.time.Clock()
font_huge = pygame.font.Font(None, 60)
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 32)
font_small = pygame.font.Font(None, 20)

# ============================================================================
# TOUCH BUTTON CLASS
# ============================================================================

class TouchButton:
    def __init__(self, x, y, width, height, label, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.color = color
        self.pressed = False
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def draw(self, surface):
        color = tuple(min(c + 50, 255) for c in self.color) if self.pressed else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 3)
        
        text = font_small.render(self.label, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

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
        
        # Mobile input
        self.move_left = False
        self.move_right = False
        self.want_jump = False
        
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
        # Handle mobile input
        self.vel_x = 0
        
        if self.move_left:
            self.vel_x = -self.move_speed
            self.facing_right = False
        if self.move_right:
            self.vel_x = self.move_speed
            self.facing_right = True
        
        if self.want_jump and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
            self.want_jump = False
        
        self.attack_cooldown -= 1
        if self.attack_cooldown < 0:
            self.is_attacking = False
        
        self.vel_y = min(self.vel_y + self.gravity, self.max_fall_speed)
        self.on_ground = False
        
        self.rect.x += self.vel_x
        self.check_collisions(platforms, boxes)
        
        self.rect.y += self.vel_y
        self.check_collisions(platforms, boxes)
        
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
        pygame.draw.rect(surface, DARK_RED, (5, 20, 70, 60))
        pygame.draw.circle(surface, DARK_RED, (40, 15), 12)
        
        pygame.draw.circle(surface, YELLOW, (30, 12), 3)
        pygame.draw.circle(surface, YELLOW, (50, 12), 3)
        pygame.draw.circle(surface, BLACK, (30, 12), 1)
        pygame.draw.circle(surface, BLACK, (50, 12), 1)
        
        for i in range(0, 70, 20):
            pygame.draw.polygon(surface, ORANGE, [(i+5, 20), (i+10, 5), (i+15, 20)])
        
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
        self.drop_cycle = 200
        self.is_falling = False
        self.vel_y = 0
        self.gravity = 0.8
        
    def update(self):
        self.drop_timer += 1
        
        cycle_pos = self.drop_timer % self.drop_cycle
        
        if cycle_pos < self.drop_cycle * 0.5:
            self.is_falling = True
            self.vel_y = 5
        else:
            self.is_falling = False
            self.vel_y = -5
        
        self.rect.y += self.vel_y
        
        if self.rect.y < self.start_y:
            self.rect.y = self.start_y
            self.vel_y = 0
        
        if self.rect.y > SCREEN_HEIGHT - 50:
            self.rect.y = SCREEN_HEIGHT - 50
    
    def draw(self):
        self.image.fill(DARK_RED)
        pygame.draw.rect(self.image, RED, (0, 0, self.width, self.height), 3)
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
        self.is_boss_level = (level_num % 100 == 0)
        
        self.create_level()
    
    def create_level(self):
        for x in range(0, SCREEN_WIDTH, 40):
            self.platforms.add(Platform(x, SCREEN_HEIGHT - 40, 40, 40, "normal"))
        
        if self.is_boss_level:
            self.create_boss_level()
        else:
            self.create_normal_level()
    
    def create_normal_level(self):
        difficulty = min(self.level_num // 10, 10)
        
        num_platforms = 3 + (self.level_num // 20)
        num_enemies = 1 + (self.level_num // 50)
        num_coins = 5 + (self.level_num // 10)
        num_boxes = min(3 + (self.level_num // 30), 8)
        num_spikes = (self.level_num // 40)
        
        platform_y_positions = []
        for i in range(num_platforms):
            y = 500 - (i * 100)
            x = random.randint(50, SCREEN_WIDTH - 250)
            width = random.randint(100, 250)
            self.platforms.add(Platform(x, y, width, 30, "normal"))
            platform_y_positions.append((x, y, width))
        
        for i in range(num_spikes):
            y = 300 - random.randint(0, 100)
            x = random.randint(50, SCREEN_WIDTH - 150)
            self.platforms.add(Platform(x, y, 100, 30, "spike"))
        
        for i in range(num_enemies):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, 400)
            enemy_type = "goblin" if random.random() > 0.3 else "orc"
            self.enemies.add(Enemy(x, y, enemy_type))
        
        for i in range(num_coins):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, 400)
            trapped = random.random() < 0.2
            self.coins.add(Coin(x, y, trapped))
        
        for i in range(num_boxes):
            x = random.randint(100, SCREEN_WIDTH - 150)
            y = random.randint(100, 300)
            self.boxes.add(DroppingBox(x, y))
        
        self.player = Player(50, 450)
        self.level_end = LevelEnd(SCREEN_WIDTH - 100, 450)
    
    def create_boss_level(self):
        self.platforms.add(Platform(50, 480, 120, 30, "normal"))
        self.platforms.add(Platform(350, 420, 120, 30, "normal"))
        self.platforms.add(Platform(650, 420, 120, 30, "normal"))
        self.platforms.add(Platform(200, 350, 150, 30, "normal"))
        self.platforms.add(Platform(500, 350, 150, 30, "normal"))
        
        for i in range(15):
            self.coins.add(Coin(random.randint(100, SCREEN_WIDTH - 100), random.randint(100, 400)))
        
        self.boss = Boss(SCREEN_WIDTH // 2 - 40, 250)
        
        self.player = Player(50, 450)
        self.level_end = LevelEnd(SCREEN_WIDTH - 100, 250)
    
    def update(self):
        level_complete = self.player.update(self.platforms, self.enemies, self.coins, self.boxes, self.level_end)
        
        for box in self.boxes:
            box.update()
        
        if self.is_boss_level:
            if self.boss.update(self.platforms, self.boxes):
                self.player.score += 500
                return level_complete
            
            if self.player.rect.colliderect(self.boss.rect):
                self.player.health -= 1
        else:
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
        
        # Mobile touch buttons
        self.left_button = TouchButton(0, SCREEN_HEIGHT - 120, SCREEN_WIDTH // 3, 120, "LEFT", BLUE)
        self.jump_button = TouchButton(SCREEN_WIDTH // 3, SCREEN_HEIGHT - 120, SCREEN_WIDTH // 3, 120, "JUMP", GREEN)
        self.right_button = TouchButton(2 * SCREEN_WIDTH // 3, SCREEN_HEIGHT - 120, SCREEN_WIDTH // 3, 120, "RIGHT", BLUE)
        
        self.attack_button = TouchButton(SCREEN_WIDTH - 120, 20, 100, 100, "ATTACK", RED)
    
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
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                
                if self.state == "menu":
                    # Start button
                    if pygame.Rect(SCREEN_WIDTH // 2 - 100, 500, 200, 60).collidepoint(pos):
                        self.start_game()
                
                if self.state == "playing":
                    # Touch controls
                    if self.left_button.is_clicked(pos):
                        self.level.player.move_left = True
                    if self.right_button.is_clicked(pos):
                        self.level.player.move_right = True
                    if self.jump_button.is_clicked(pos):
                        self.level.player.want_jump = True
                    if self.attack_button.is_clicked(pos):
                        if self.level.player.attack_cooldown <= 0:
                            self.level.player.is_attacking = True
                            self.level.player.attack_cooldown = 15
                            self.level.player.attack_enemies(self.level.enemies)
                
                if self.state == "game_over":
                    if pygame.Rect(SCREEN_WIDTH // 2 - 100, 500, 200, 60).collidepoint(pos):
                        self.start_game()
                
                if self.state == "level_complete":
                    if pygame.Rect(SCREEN_WIDTH // 2 - 150, 500, 300, 60).collidepoint(pos):
                        self.next_level()
                
                if self.state == "ultimate_win":
                    if pygame.Rect(SCREEN_WIDTH // 2 - 100, 500, 200, 60).collidepoint(pos):
                        self.start_game()
            
            if event.type == pygame.MOUSEBUTTONUP:
                self.level.player.move_left = False
                self.level.player.move_right = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
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
            self.draw_mobile_controls()
        elif self.state == "game_over":
            self.draw_game_over()
        elif self.state == "level_complete":
            self.draw_level_complete()
        elif self.state == "ultimate_win":
            self.draw_ultimate_win()
    
    def draw_menu(self):
        title = font_large.render("WARRIOR", True, RED)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        title2 = font_large.render("ADVENTURE 1", True, ORANGE)
        screen.blit(title2, (SCREEN_WIDTH // 2 - title2.get_width() // 2, 110))
        
        subtitle = font_medium.render("1000+ LEVELS!", True, YELLOW)
        screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 200))
        
        controls = [
            "Touch LEFT/RIGHT to move",
            "Tap JUMP to jump",
            "Tap ATTACK to fight",
            "Reach the flag to win!"
        ]
        
        y = 280
        for control in controls:
            text = font_small.render(control, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y))
            y += 35
        
        # Start button
        pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH // 2 - 100, 500, 200, 60))
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 100, 500, 200, 60), 3)
        start = font_medium.render("START", True, BLACK)
        screen.blit(start, (SCREEN_WIDTH // 2 - start.get_width() // 2, 515))
    
    def draw_mobile_controls(self):
        self.left_button.draw(screen)
        self.jump_button.draw(screen)
        self.right_button.draw(screen)
        self.attack_button.draw(screen)
    
    def draw_hud(self):
        health_text = font_small.render(f"HP: {int(self.level.player.health)}", True, RED)
        screen.blit(health_text, (10, 10))
        
        level_text = font_small.render(f"Lvl {self.current_level}", True, WHITE)
        screen.blit(level_text, (10, 40))
        
        score_text = font_small.render(f"Score: {self.level.player.score}", True, YELLOW)
        screen.blit(score_text, (SCREEN_WIDTH - 200, 10))
        
        if self.level.is_boss_level:
            boss_text = font_medium.render("BOSS!", True, RED)
            screen.blit(boss_text, (SCREEN_WIDTH // 2 - boss_text.get_width() // 2, 10))
    
    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        game_over_text = font_large.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 80))
        
        level_text = font_medium.render(f"Level: {self.current_level}", True, YELLOW)
        screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 180))
        
        score_text = font_medium.render(f"Score: {self.level.player.score}", True, YELLOW)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 240))
        
        pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH // 2 - 100, 500, 200, 60))
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 100, 500, 200, 60), 3)
        restart = font_medium.render("RETRY", True, BLACK)
        screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 515))
    
    def draw_level_complete(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        complete_text = font_large.render("LEVEL CLEAR!", True, GREEN)
        screen.blit(complete_text, (SCREEN_WIDTH // 2 - complete_text.get_width() // 2, 80))
        
        score_text = font_medium.render(f"Score: {self.level.player.score}", True, YELLOW)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 220))
        
        pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH // 2 - 150, 500, 300, 60))
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 150, 500, 300, 60), 3)
        next_level = font_medium.render("NEXT LEVEL", True, BLACK)
        screen.blit(next_level, (SCREEN_WIDTH // 2 - next_level.get_width() // 2, 515))
    
    def draw_ultimate_win(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        win_text = font_large.render("LEGEND!", True, YELLOW)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, 80))
        
        win_text2 = font_medium.render("All 1000 levels conquered!", True, ORANGE)
        screen.blit(win_text2, (SCREEN_WIDTH // 2 - win_text2.get_width() // 2, 180))
        
        score_text = font_medium.render(f"Final Score: {self.total_score}", True, GREEN)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 260))
        
        pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH // 2 - 100, 500, 200, 60))
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 100, 500, 200, 60), 3)
        restart = font_medium.render("REPLAY", True, BLACK)
        screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 515))
    
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
