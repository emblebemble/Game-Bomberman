import pygame
import random
import time
import math

# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 40
GRID_WIDTH = 15
GRID_HEIGHT = 13
WINDOW_WIDTH = GRID_WIDTH * TILE_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * TILE_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 177, 76)
BROWN = (185, 122, 87)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
SKIN = (255, 198, 140)

# Create the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Bomberman")
clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.bombs_allowed = 1
        self.bomb_range = 2
        self.alive = True

    def draw(self, screen):
        # Body
        body_rect = pygame.Rect(
            self.rect.x + 10, 
            self.rect.y + 15, 
            TILE_SIZE - 20, 
            TILE_SIZE - 25
        )
        pygame.draw.rect(screen, BLUE, body_rect)
        
        # Head
        head_pos = (self.rect.centerx, self.rect.y + 12)
        pygame.draw.circle(screen, SKIN, head_pos, 8)
        
        # Eyes
        eye_color = BLACK
        left_eye = (head_pos[0] - 3, head_pos[1] - 2)
        right_eye = (head_pos[0] + 3, head_pos[1] - 2)
        pygame.draw.circle(screen, eye_color, left_eye, 2)
        pygame.draw.circle(screen, eye_color, right_eye, 2)
        
        # Legs
        leg_color = BLACK
        left_leg = pygame.Rect(self.rect.x + 12, self.rect.bottom - 10, 4, 8)
        right_leg = pygame.Rect(self.rect.right - 16, self.rect.bottom - 10, 4, 8)
        pygame.draw.rect(screen, leg_color, left_leg)
        pygame.draw.rect(screen, leg_color, right_leg)

    def move(self, dx, dy, walls, blocks):
        new_x = self.x + dx
        new_y = self.y + dy
        new_rect = pygame.Rect(new_x * TILE_SIZE, new_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        
        can_move = True
        for wall in walls:
            if new_rect.colliderect(wall):
                can_move = False
        for block in blocks:
            if new_rect.colliderect(block.rect):
                can_move = False
                
        if can_move and 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
            self.x = new_x
            self.y = new_y
            self.rect.x = new_x * TILE_SIZE
            self.rect.y = new_y * TILE_SIZE

class Bomb:
    def __init__(self, x, y, range):
        self.x = x
        self.y = y
        self.range = range
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.plant_time = time.time()
        self.exploded = False
        self.explosion_duration = 0.5
        self.explosion_start = None
        self.pulse_start = time.time()
        self.pulse_duration = 0.5

    def draw(self, screen):
        current_time = time.time()
        pulse_progress = (current_time - self.pulse_start) / self.pulse_duration
        if pulse_progress >= 1:
            self.pulse_start = current_time
            pulse_progress = 0

        # Calculate bomb size based on pulse
        base_size = TILE_SIZE * 0.6
        pulse_size = base_size + (base_size * 0.2 * abs(math.sin(pulse_progress * math.pi)))
        
        # Draw bomb body (circle)
        center_x = self.rect.centerx
        center_y = self.rect.centery
        pygame.draw.circle(screen, BLACK, (center_x, center_y), int(pulse_size))
        
        # Draw fuse
        fuse_start = (center_x, center_y - int(pulse_size))
        fuse_end = (center_x, center_y - int(pulse_size) - 8)
        pygame.draw.line(screen, RED, fuse_start, fuse_end, 3)
        pygame.draw.circle(screen, YELLOW, fuse_end, 4)

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

def create_level():
    walls = []
    blocks = []
    
    # Create fixed walls (every second tile)
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if x % 2 == 1 and y % 2 == 1:
                walls.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
    # Create random destructible blocks
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if (x, y) not in [(1,1), (1,2), (2,1)]:  # Keep starting area clear
                if random.random() < 0.3 and (x % 2 == 0 or y % 2 == 0):
                    blocks.append(Block(x, y))
    
    return walls, blocks

def get_explosion_areas(bomb):
    areas = [(bomb.x, bomb.y)]
    
    # Check all four directions
    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        for r in range(1, bomb.range + 1):
            new_x = bomb.x + (dx * r)
            new_y = bomb.y + (dy * r)
            if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                areas.append((new_x, new_y))
            
    return areas

def main():
    walls, blocks = create_level()
    player = Player(1, 1)
    bombs = []
    explosions = []
    
    running = True
    while running and player.alive:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if len(bombs) < player.bombs_allowed:
                        bombs.append(Bomb(player.x, player.y, player.bomb_range))
        
        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-1, 0, walls, blocks)
        if keys[pygame.K_RIGHT]:
            player.move(1, 0, walls, blocks)
        if keys[pygame.K_UP]:
            player.move(0, -1, walls, blocks)
        if keys[pygame.K_DOWN]:
            player.move(0, 1, walls, blocks)
        
        # Update bombs
        current_time = time.time()
        for bomb in bombs[:]:
            if not bomb.exploded and current_time - bomb.plant_time >= 3:
                bomb.exploded = True
                bomb.explosion_start = current_time
                explosion_areas = get_explosion_areas(bomb)
                explosions.extend(explosion_areas)
                
                # Destroy blocks and check player collision
                for ex, ey in explosion_areas:
                    # Check if player is caught in explosion
                    if player.x == ex and player.y == ey:
                        player.alive = False
                    
                    # Destroy blocks
                    for block in blocks[:]:
                        if block.x == ex and block.y == ey:
                            blocks.remove(block)
            
            # Remove expired explosions
            if bomb.exploded and current_time - bomb.explosion_start >= bomb.explosion_duration:
                bombs.remove(bomb)
                for pos in explosions[:]:
                    if pos in explosion_areas:
                        explosions.remove(pos)
        
        # Drawing
        screen.fill(GREEN)
        
        # Draw walls
        for wall in walls:
            pygame.draw.rect(screen, GRAY, wall)
        
        # Draw blocks
        for block in blocks:
            pygame.draw.rect(screen, BROWN, block.rect)
        
        # Draw bombs
        for bomb in bombs:
            bomb.draw(screen)
        
        # Draw explosions
        for ex, ey in explosions:
            center_x = ex * TILE_SIZE + TILE_SIZE // 2
            center_y = ey * TILE_SIZE + TILE_SIZE // 2
            pygame.draw.circle(screen, RED, (center_x, center_y), TILE_SIZE // 2)
        
        # Draw player
        if player.alive:
            player.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    # Game over screen
    if not player.alive:
        font = pygame.font.Font(None, 74)
        text = font.render('Game Over!', True, RED)
        screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, WINDOW_HEIGHT//2))
        pygame.display.flip()
        time.sleep(2)

    pygame.quit()

if __name__ == "__main__":
    main() 