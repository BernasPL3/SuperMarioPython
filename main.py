import pygame
import sys
import random

pygame.init()

# --------------------
# CONFIG
# --------------------
WIDTH = 1000
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario Python")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)

# --------------------
# COLORS
# --------------------
SKY = (92, 148, 252)
GROUND = (111, 78, 55)
GREEN = (0, 200, 0)
RED = (255, 60, 60)
YELLOW = (255, 220, 0)
WHITE = (255, 255, 255)
BROWN = (160, 82, 45)

# --------------------
# PLAYER
# --------------------
player = pygame.Rect(100, 400, 45, 55)

player_vel_y = 0
gravity = 1
jump_power = -18

move_speed = 6

on_ground = False

lives = 3
score = 0

# --------------------
# WORLD
# --------------------
ground = pygame.Rect(0, 520, WIDTH, 80)

platforms = [
    pygame.Rect(250, 420, 120, 20),
    pygame.Rect(450, 340, 120, 20),
    pygame.Rect(700, 260, 120, 20)
]

# --------------------
# ENEMIES
# --------------------
enemies = [
    {
        "rect": pygame.Rect(500, 480, 40, 40),
        "dir": 1
    },
    {
        "rect": pygame.Rect(800, 480, 40, 40),
        "dir": -1
    }
]

enemy_speed = 3

# --------------------
# COINS
# --------------------
coins = []

for i in range(8):
    x = random.randint(150, 900)
    y = random.randint(150, 450)

    coins.append(
        pygame.Rect(x, y, 20, 20)
    )

# --------------------
# GAME LOOP
# --------------------
running = True

while running:

    clock.tick(60)

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # KEYS
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= move_speed

    if keys[pygame.K_RIGHT]:
        player.x += move_speed

    # JUMP
    if keys[pygame.K_SPACE] and on_ground:
        player_vel_y = jump_power
        on_ground = False

    # GRAVITY
    player_vel_y += gravity
    player.y += player_vel_y

    # LIMITS
    if player.left < 0:
        player.left = 0

    if player.right > WIDTH:
        player.right = WIDTH

    # GROUND COLLISION
    on_ground = False

    if player.colliderect(ground):
        player.bottom = ground.top
        player_vel_y = 0
        on_ground = True

    # PLATFORM COLLISION
    for platform in platforms:

        if player.colliderect(platform):

            if player_vel_y > 0:
                player.bottom = platform.top
                player_vel_y = 0
                on_ground = True

    # ENEMY MOVEMENT
    for enemy in enemies:

        enemy["rect"].x += enemy_speed * enemy["dir"]

        if enemy["rect"].x < 400:
            enemy["dir"] = 1

        if enemy["rect"].x > 900:
            enemy["dir"] = -1

        # COLLISION PLAYER / ENEMY
        if player.colliderect(enemy["rect"]):

            lives -= 1

            player.x = 100
            player.y = 400

            if lives <= 0:
                print("GAME OVER")
                pygame.quit()
                sys.exit()

    # COIN COLLISION
    for coin in coins[:]:

        if player.colliderect(coin):
            coins.remove(coin)
            score += 1

    # WIN
    if score == 8:

        win_text = font.render("YOU WIN!", True, WHITE)

        screen.blit(win_text, (400, 200))
        pygame.display.flip()

        pygame.time.delay(3000)

        pygame.quit()
        sys.exit()

    # --------------------
    # DRAW
    # --------------------
    screen.fill(SKY)

    # GROUND
    pygame.draw.rect(screen, GROUND, ground)

    # PLATFORMS
    for platform in platforms:
        pygame.draw.rect(screen, BROWN, platform)

    # PLAYER
    pygame.draw.rect(screen, WHITE, player)

    # ENEMIES
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy["rect"])

    # COINS
    for coin in coins:
        pygame.draw.ellipse(screen, YELLOW, coin)

    # UI
    score_text = font.render(f"Coins: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)

    screen.blit(score_text, (20, 20))
    screen.blit(lives_text, (20, 60))

    pygame.display.flip()

pygame.quit()
