"""Mochi, the player character: running, jumping, tile collision and animation."""
import pygame
from settings import (GRAVITY, MAX_FALL_SPEED, MOVE_SPEED, GROUND_ACCEL, AIR_ACCEL,
                      GROUND_FRICTION, AIR_FRICTION, JUMP_SPEED, JUMP_CUT_GRAVITY,
                      COYOTE_FRAMES, JUMP_BUFFER_FRAMES)
import sprites


class Player:
    W, H = 30, 42  # hitbox is a bit smaller than the picture, which feels fair

    def __init__(self, x, y):
        """x, y is where the feet start (bottom middle of the hitbox)."""
        self.rect = pygame.Rect(0, 0, self.W, self.H)
        self.frames = sprites.player_frames()
        self.respawn((x, y))

    def respawn(self, pos):
        self.rect.midbottom = (int(pos[0]), int(pos[1]))
        self.px = float(self.rect.x)
        self.py = float(self.rect.y)
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.facing = 1
        self.coyote = 0
        self.jump_buffer = 0
        self.anim_t = 0.0
        self.invuln = 0

    # ------------------------------------------------------------ update
    def update(self, level, keys, jump_pressed):
        left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        jump_held = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]
        direction = int(bool(right)) - int(bool(left))

        # left / right
        accel = GROUND_ACCEL if self.on_ground else AIR_ACCEL
        if direction:
            self.vx += accel * direction
            self.vx = max(-MOVE_SPEED, min(MOVE_SPEED, self.vx))
            self.facing = direction
        else:
            self.vx *= GROUND_FRICTION if self.on_ground else AIR_FRICTION
            if abs(self.vx) < 0.1:
                self.vx = 0.0

        # jump with coyote time and jump buffering
        if jump_pressed:
            self.jump_buffer = JUMP_BUFFER_FRAMES
        elif self.jump_buffer > 0:
            self.jump_buffer -= 1
        if self.on_ground:
            self.coyote = COYOTE_FRAMES
        elif self.coyote > 0:
            self.coyote -= 1
        if self.jump_buffer > 0 and self.coyote > 0:
            self.vy = JUMP_SPEED
            self.jump_buffer = 0
            self.coyote = 0
            self.on_ground = False

        # gravity (stronger when jump is released early = variable jump height)
        g = GRAVITY
        if self.vy < 0 and not jump_held:
            g *= JUMP_CUT_GRAVITY
        self.vy = min(self.vy + g, MAX_FALL_SPEED)

        # move on x, then fix collisions
        self.px += self.vx
        self.rect.x = round(self.px)
        for tile in level.solid_rects_near(self.rect):
            if self.rect.colliderect(tile):
                if self.vx > 0:
                    self.rect.right = tile.left
                elif self.vx < 0:
                    self.rect.left = tile.right
                self.px = float(self.rect.x)
                self.vx = 0.0
        if self.rect.left < 0:
            self.rect.left = 0
            self.px = float(self.rect.x)
            self.vx = 0.0
        if self.rect.right > level.width:
            self.rect.right = level.width
            self.px = float(self.rect.x)
            self.vx = 0.0

        # move on y, then fix collisions
        self.py += self.vy
        self.rect.y = round(self.py)
        self.on_ground = False
        for tile in level.solid_rects_near(self.rect):
            if self.rect.colliderect(tile):
                if self.vy > 0:
                    self.rect.bottom = tile.top
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = tile.bottom
                self.py = float(self.rect.y)
                self.vy = 0.0

        self.anim_t += abs(self.vx) * 0.08

    # ------------------------------------------------------------ draw
    def draw(self, surf, cam_x, cam_y, tick):
        if self.invuln > 0 and (self.invuln // 4) % 2 == 0:
            return  # blink while invulnerable
        frames = self.frames[self.facing]
        if not self.on_ground:
            img = frames["jump"] if self.vy < 0 else frames["fall"]
        elif abs(self.vx) > 0.5:
            img = frames["run"][int(self.anim_t) % 4]
        else:
            img = frames["blink"] if (tick % 200) < 8 else frames["idle"]
        pos = img.get_rect(midbottom=(self.rect.centerx - cam_x, self.rect.bottom - cam_y + 4))
        surf.blit(img, pos)
