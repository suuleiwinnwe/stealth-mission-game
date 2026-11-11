"""Game-wide settings. Tweak these numbers to change how the game feels."""

TILE = 50                      # size of one level tile in pixels
SCREEN_W, SCREEN_H = 1000, 550
FPS = 60

# Movement tuning
GRAVITY = 0.8
MAX_FALL_SPEED = 18
MOVE_SPEED = 5.0
GROUND_ACCEL = 0.9
AIR_ACCEL = 0.55
GROUND_FRICTION = 0.8
AIR_FRICTION = 0.92
JUMP_SPEED = -16.0             # more negative = higher jump
JUMP_CUT_GRAVITY = 2.2         # let go of jump early = shorter hop
COYOTE_FRAMES = 6              # can still jump this many frames after leaving a ledge
JUMP_BUFFER_FRAMES = 6         # jump pressed slightly before landing still counts

# Lives
START_LIVES = 3
MAX_LIVES = 5
INVULN_FRAMES = 90             # blinking, harmless time after getting hurt

# Colors
ORANGE = (255, 150, 20)
DARK = (60, 40, 50)
WHITE = (255, 255, 255)
