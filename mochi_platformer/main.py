"""Mochi's Jump Quest - run this file to play:  python main.py

Controls: LEFT/RIGHT or A/D to move, SPACE / UP / W to jump (hold for a higher jump).
R restarts the level, ESC goes back to the title screen.
"""
import sys
import pygame
from settings import (SCREEN_W, SCREEN_H, FPS, START_LIVES, MAX_LIVES, INVULN_FRAMES,
                      ORANGE, DARK, WHITE)
from level import Level
from player import Player
from background import Background
import sprites
from levels import LEVELS


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Mochi's Jump Quest")
        self.clock = pygame.time.Clock()
        self.bg = Background()
        self.font_huge = pygame.font.Font(None, 130)
        self.font_big = pygame.font.Font(None, 90)
        self.font_mid = pygame.font.Font(None, 44)
        self.font_small = pygame.font.Font(None, 30)
        self.state = "title"          # title, play, win, over
        self.tick = 0
        self.level_index = 0
        self.load_level(0)

    # ------------------------------------------------------------ setup
    def load_level(self, index):
        self.level_index = index
        self.level = Level(LEVELS[index])
        self.player = Player(*self.level.start)
        self.respawn_point = self.level.start
        self.lives = START_LIVES
        self.frames = 0
        self.flash = 0
        self.message = ""
        self.message_timer = 0
        self.cam_x = 0.0
        self.cam_y = 0.0
        self.update_camera(snap=True)

    def start(self, index):
        self.load_level(index)
        self.state = "play"

    # ------------------------------------------------------------ game logic
    def hurt(self):
        self.lives -= 1
        self.flash = 18
        if self.lives <= 0:
            self.state = "over"
        else:
            self.player.respawn(self.respawn_point)
            self.player.invuln = INVULN_FRAMES

    def say(self, text):
        self.message = text
        self.message_timer = 90

    def step(self, keys, jump_pressed):
        """One frame of game logic (kept separate from drawing so it can be tested)."""
        self.tick += 1
        if self.state != "play":
            return
        self.frames += 1
        p = self.player
        p.update(self.level, keys, jump_pressed)
        if p.invuln > 0:
            p.invuln -= 1

        coins, hearts = self.level.collect(p.rect)
        if hearts:
            self.lives = min(MAX_LIVES, self.lives + hearts)
            self.say("+1 life!")

        spawn = self.level.touch_checkpoint(p.rect)
        if spawn:
            self.respawn_point = spawn
            self.say("Checkpoint!")

        if p.rect.top > self.level.height + 200:
            self.hurt()
        elif p.invuln == 0 and self.level.hazard_hit(p.rect):
            self.hurt()

        if self.state == "play" and p.rect.colliderect(self.level.goal):
            self.state = "win"

        if self.flash > 0:
            self.flash -= 1
        if self.message_timer > 0:
            self.message_timer -= 1
        self.update_camera()

    def update_camera(self, snap=False):
        p = self.player.rect
        lvl = self.level
        target_x = p.centerx - SCREEN_W * 0.4
        max_x = max(0, lvl.width - SCREEN_W)
        target_x = max(0, min(max_x, target_x))
        if lvl.height <= SCREEN_H:
            target_y = lvl.height - SCREEN_H
        else:
            target_y = max(0, min(lvl.height - SCREEN_H, p.centery - SCREEN_H * 0.55))
        k = 1.0 if snap else 0.12
        self.cam_x += (target_x - self.cam_x) * k
        self.cam_y += (target_y - self.cam_y) * k

    # ------------------------------------------------------------ drawing
    def outlined_text(self, text, font, color, center, outline=DARK, width=3):
        base = font.render(text, True, color)
        edge = font.render(text, True, outline)
        rect = base.get_rect(center=center)
        for dx in range(-width, width + 1):
            for dy in range(-width, width + 1):
                if dx * dx + dy * dy <= width * width:
                    self.screen.blit(edge, rect.move(dx, dy))
        self.screen.blit(base, rect)

    def draw_hud(self):
        total = max(START_LIVES, self.lives)
        full = sprites.heart_surface(34, (255, 70, 90))
        empty = sprites.heart_surface(34, (190, 190, 200), outline=(110, 110, 120))
        for i in range(total):
            self.screen.blit(full if i < self.lives else empty, (16 + i * 40, 14))

        coin_text = f"{self.level.coins_collected} / {len(self.level.coins)}"
        sprites.draw_coin(self.screen, (SCREEN_W - 120, 30), self.tick)
        self.outlined_text(coin_text, self.font_mid, WHITE, (SCREEN_W - 60, 30), width=2)
        secs = self.frames / FPS
        self.outlined_text(f"{secs:5.1f}s", self.font_small, WHITE, (SCREEN_W - 70, 66), width=2)
        self.outlined_text(f"Level {self.level_index + 1}: {self.level.name}", self.font_small, WHITE,
                           (SCREEN_W // 2, 24), width=2)
        if self.message_timer > 0:
            self.outlined_text(self.message, self.font_mid, ORANGE, (SCREEN_W // 2, 80), width=3)

    def draw_title(self):
        self.bg.draw(self.screen, self.tick * 0.6)
        self.outlined_text("Mochi's Jump Quest", self.font_big, ORANGE, (SCREEN_W // 2, 110), width=4)
        mochi = pygame.transform.scale(sprites.player_frames()[1]["idle"], (108, 126))
        bounce = abs(pygame.math.Vector2(0, 1).rotate(self.tick * 3).y) * 18
        self.screen.blit(mochi, mochi.get_rect(midbottom=(SCREEN_W // 2, 330 - bounce)))
        self.outlined_text("Press SPACE to start", self.font_mid, WHITE, (SCREEN_W // 2, 380), width=2)
        names = "   ".join(f"{i + 1}: {m.NAME}" for i, m in enumerate(LEVELS))
        self.outlined_text(f"Pick a level:  {names}", self.font_small, WHITE, (SCREEN_W // 2, 430), width=2)
        self.outlined_text("Move: arrows / A D     Jump: SPACE     Restart: R", self.font_small,
                           WHITE, (SCREEN_W // 2, 480), width=2)

    def draw(self):
        if self.state == "title":
            self.draw_title()
            return
        self.bg.draw(self.screen, self.cam_x)
        cx, cy = int(self.cam_x), int(self.cam_y)
        self.level.draw(self.screen, cx, cy, self.tick)
        self.player.draw(self.screen, cx, cy, self.tick)
        self.draw_hud()

        if self.flash > 0:
            tint = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            tint.fill((255, 40, 40, int(110 * self.flash / 18)))
            self.screen.blit(tint, (0, 0))

        if self.state == "win":
            self.outlined_text("You Win!!", self.font_huge, ORANGE, (SCREEN_W // 2, 170), width=5)
            stats = (f"Time {self.frames / FPS:.1f}s     Coins {self.level.coins_collected}"
                     f"/{len(self.level.coins)}     Lives left {self.lives}")
            self.outlined_text(stats, self.font_mid, WHITE, (SCREEN_W // 2, 250), width=2)
            more = "N: next level     " if self.level_index + 1 < len(LEVELS) else ""
            self.outlined_text(more + "R: play again     ESC: menu", self.font_small, WHITE,
                               (SCREEN_W // 2, 295), width=2)
        elif self.state == "over":
            self.outlined_text("Game Over", self.font_huge, (230, 70, 80), (SCREEN_W // 2, 190), width=5)
            self.outlined_text("R: try again     ESC: menu", self.font_small, WHITE,
                               (SCREEN_W // 2, 260), width=2)

    # ------------------------------------------------------------ main loop
    def run(self):
        while True:
            jump_pressed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type != pygame.KEYDOWN:
                    continue
                if event.key == pygame.K_ESCAPE:
                    if self.state == "title":
                        pygame.quit()
                        sys.exit()
                    self.state = "title"
                elif self.state == "title":
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.start(self.level_index)
                    elif pygame.K_1 <= event.key <= pygame.K_9:
                        index = event.key - pygame.K_1
                        if index < len(LEVELS):
                            self.start(index)
                else:
                    if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                        jump_pressed = True
                    elif event.key == pygame.K_r:
                        self.start(self.level_index)
                    elif event.key == pygame.K_n and self.state == "win" \
                            and self.level_index + 1 < len(LEVELS):
                        self.start(self.level_index + 1)
            self.step(pygame.key.get_pressed(), jump_pressed)
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()
