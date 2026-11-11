import pygame


pygame.init()

WIDTH, HEIGHT = 800, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
level_complete = False

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface, camera_x):
     pygame.draw.rect(
        surface,
        (100, 200, 100),
        (
            self.rect.x - camera_x,
            self.rect.y,
            self.rect.width,
            self.rect.height
        )
    )




# Create platforms
platforms = [

    Platform(0, 400, 700, 50),

    Platform(900, 400, 700, 50),

    Platform(1800, 400, 1000, 50),

    Platform(850, 320, 120, 20),

    Platform(1200, 250, 150, 20),

    Platform(1500, 350, 150, 20),

    Platform(1900, 250, 150, 20),

    Platform(2300, 320, 150, 20)
]



# Flag
finish_flag = pygame.Rect(2700, 250, 40, 150)

# Start Sign
start_sign = pygame.Rect(50, 300, 20, 100)


#Player
player = pygame.Rect(100, 300, 40, 60)
velocity_y = 8
gravity = 0.6
jump_strength = -8
on_ground = True

jump_count = 0
max_jumps = 2


#Main game loop

running = True

while running:

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                velocity_y = jump_strength

    # Left / Right movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= 10

    if keys[pygame.K_RIGHT]:
        player.x += 10

    # Gravity
    velocity_y += gravity
    player.y += int(velocity_y)

    # Collision Detection
    on_ground = False

    for platform in platforms:

        if player.colliderect(platform.rect):

            if velocity_y > 0:
                player.bottom = platform.rect.top
                velocity_y = 0
                on_ground = True

       # Level Complete
    if player.colliderect(finish_flag):
        level_complete = True

    # Game Over
    if player.y > HEIGHT:
        screen.fill((135, 206, 235))

        game_over_text = font.render(
            "GAME OVER!",
            True,
            (255, 0, 0)
        )

        screen.blit(game_over_text, (300, 180))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    # Camera
    camera_x = max(0, player.centerx - WIDTH // 2)

    # Draw
    screen.fill((135, 206, 235))

    # Level Title
    level_text = font.render("LEVEL 1", True, (0, 0, 0))
    screen.blit(level_text, (20, 20))

    # Platforms
    for platform in platforms:
        platform.draw(screen, camera_x)

    # Start Sign Pole
    pygame.draw.rect(
        screen,
        (150, 150, 150),
        (
            start_sign.x - camera_x,
            start_sign.y,
            10,
            start_sign.height
        )
    )

    # Start Flag Triangle
    pygame.draw.polygon(
    screen,
    (0, 255, 0),
    [
        (start_sign.x - camera_x + 10, start_sign.y),
        (start_sign.x - camera_x + 60, start_sign.y + 20),
        (start_sign.x - camera_x + 10, start_sign.y + 40)
    ]
)

    # Start Text
    start_text = font.render("START", True, (0, 0, 0))
    screen.blit(
        start_text,
        (
            start_sign.x - camera_x - 10,
            start_sign.y - 50
        )
    )


    # Flag Pole
    pygame.draw.rect(
        screen,
        (150, 150, 150),
        (
            finish_flag.x - camera_x,
            finish_flag.y,
            10,
            finish_flag.height
        )
    )


    # Flag
    pygame.draw.polygon(
        screen,
        (255, 0, 0),
        [
            (finish_flag.x - camera_x + 10, finish_flag.y),
            (finish_flag.x - camera_x + 60, finish_flag.y + 20),
            (finish_flag.x - camera_x + 10, finish_flag.y + 40)
        ]
    )

    # Player
    pygame.draw.rect(
        screen,
        (255, 0, 0),
        (
            player.x - camera_x,
            player.y,
            player.width,
            player.height
        )
    )

    # Level Complete Message
    if level_complete:
        win_text = font.render(
            "LEVEL COMPLETE!",
            True,
            (255, 255, 0)
        )
        screen.blit(win_text, (250, 180))

    pygame.display.flip()

    if level_complete:
        pygame.time.wait(2000)
        running = False

    clock.tick(60)


pygame.quit()
