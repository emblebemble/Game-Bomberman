import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NEON_GREEN = (57, 255, 20)
NEON_PINK = (255, 20, 147)
NEON_BLUE = (20, 255, 236)
NEON_YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

FPS = 60

# Create the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Neon Pong")
clock = pygame.time.Clock()

# Game objects
class Paddle:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.score = 0
        self.speed = 7
        self.color = color

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WINDOW_WIDTH // 2 - BALL_SIZE // 2,
                              WINDOW_HEIGHT // 2 - BALL_SIZE // 2,
                              BALL_SIZE, BALL_SIZE)
        self.speed_x = 7 * random.choice((1, -1))
        self.speed_y = 7 * random.choice((1, -1))
        self.color = NEON_YELLOW

    def reset(self):
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.speed_x = 7 * random.choice((1, -1))
        self.speed_y = 7 * random.choice((1, -1))
        # Change ball color on reset
        self.color = random.choice([NEON_YELLOW, NEON_PINK, NEON_GREEN, NEON_BLUE])

# Create game objects
player = Paddle(50, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2, NEON_PINK)
computer = Paddle(WINDOW_WIDTH - 50 - PADDLE_WIDTH, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2, NEON_BLUE)
ball = Ball()

# Font for score display
font = pygame.font.Font(None, 74)

def draw_game():
    screen.fill(BLACK)
    
    # Draw background grid lines
    for y in range(0, WINDOW_HEIGHT, 20):
        pygame.draw.line(screen, PURPLE, (0, y), (WINDOW_WIDTH, y), 1)
    
    # Draw paddles and ball
    pygame.draw.rect(screen, player.color, player.rect)
    pygame.draw.rect(screen, computer.color, computer.rect)
    pygame.draw.ellipse(screen, ball.color, ball.rect)
    
    # Draw center line
    pygame.draw.line(screen, NEON_GREEN, 
                    (WINDOW_WIDTH // 2, 0),
                    (WINDOW_WIDTH // 2, WINDOW_HEIGHT), 3)
    
    # Draw scores with glowing effect
    player_text = font.render(str(player.score), True, player.color)
    computer_text = font.render(str(computer.score), True, computer.color)
    screen.blit(player_text, (WINDOW_WIDTH // 4, 20))
    screen.blit(computer_text, (3 * WINDOW_WIDTH // 4, 20))

def update_game():
    # Move ball
    ball.rect.x += ball.speed_x
    ball.rect.y += ball.speed_y
    
    # Ball collision with top and bottom
    if ball.rect.top <= 0 or ball.rect.bottom >= WINDOW_HEIGHT:
        ball.speed_y *= -1
    
    # Ball collision with paddles
    if ball.rect.colliderect(player.rect) or ball.rect.colliderect(computer.rect):
        ball.speed_x *= -1.1  # Increase speed slightly on paddle hits
        ball.speed_y *= 1.1
    
    # Score points
    if ball.rect.left <= 0:
        computer.score += 1
        ball.reset()
    elif ball.rect.right >= WINDOW_WIDTH:
        player.score += 1
        ball.reset()
    
    # Move computer paddle (AI)
    if computer.rect.centery < ball.rect.centery and computer.rect.bottom < WINDOW_HEIGHT:
        computer.rect.y += computer.speed * 0.5  # Made AI slower for better gameplay
    elif computer.rect.centery > ball.rect.centery and computer.rect.top > 0:
        computer.rect.y -= computer.speed * 0.5

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Move player paddle with keyboard
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.rect.top > 0:
        player.rect.y -= player.speed
    if keys[pygame.K_DOWN] and player.rect.bottom < WINDOW_HEIGHT:
        player.rect.y += player.speed
    
    # Update game state
    update_game()
    
    # Draw everything
    draw_game()
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit() 