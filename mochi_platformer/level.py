"""Turns an ASCII level layout (see levels/level1.py) into a playable level."""
import pygame
from settings import TILE
import sprites


class Level:
    def __init__(self, module):
        self.name = module.NAME
        rows = list(module.LAYOUT)
        self.rows = len(rows)
        self.cols = max(len(r) for r in rows)
        self.width = self.cols * TILE
        self.height = self.rows * TILE

        self.solid = set()
        self.saws = []          # (center_x, center_y, hit_radius)
        self.spikes = []        # hit rects
        self.coins = []         # [x, y, collected]
        self.hearts = []        # [x, y, collected]
        self.checkpoints = []   # {"rect", "spawn", "active"}
        self.goal = None
        self.start = (TILE * 1.5, TILE * 2)

        for r, row in enumerate(rows):
            for c, ch in enumerate(row):
                x, y = c * TILE, r * TILE
                if ch == "#":
                    self.solid.add((c, r))
                elif ch == "S":
                    self.start = (x + TILE // 2, y + TILE)
                elif ch == "F":
                    self.goal = pygame.Rect(x, y - 40, TILE, TILE + 40)
                elif ch == "*":
                    self.saws.append((x + TILE // 2, y + TILE // 2, 19))
                elif ch == "^":
                    self.spikes.append(pygame.Rect(x + 6, y + TILE - 24, TILE - 12, 22))
                elif ch == "o":
                    self.coins.append([x + TILE // 2, y + TILE // 2, False])
                elif ch == "H":
                    self.hearts.append([x + TILE // 2, y + TILE // 2, False])
                elif ch == "C":
                    self.checkpoints.append({
                        "rect": pygame.Rect(x, y - 10, TILE, TILE + 10),
                        "spawn": (x + TILE // 2, y + TILE),
                        "active": False,
                    })
        if self.goal is None:
            raise ValueError(f"{self.name}: layout needs an 'F' (goal flag)")

    # ------------------------------------------------------------ collision helpers
    def solid_rects_near(self, rect):
        c0, c1 = rect.left // TILE - 1, rect.right // TILE + 1
        r0, r1 = rect.top // TILE - 1, rect.bottom // TILE + 1
        for c in range(c0, c1 + 1):
            for r in range(r0, r1 + 1):
                if (c, r) in self.solid:
                    yield pygame.Rect(c * TILE, r * TILE, TILE, TILE)

    def hazard_hit(self, rect):
        for spike in self.spikes:
            if rect.colliderect(spike):
                return True
        for cx, cy, radius in self.saws:
            nx = max(rect.left, min(cx, rect.right))
            ny = max(rect.top, min(cy, rect.bottom))
            if (nx - cx) ** 2 + (ny - cy) ** 2 < radius * radius:
                return True
        return False

    def collect(self, rect):
        """Returns (coins_picked_up, hearts_picked_up) this frame."""
        coins = hearts = 0
        reach = rect.inflate(16, 16)  # a little generous so coins feel easy to grab
        for coin in self.coins:
            if not coin[2] and reach.collidepoint(coin[0], coin[1]):
                coin[2] = True
                coins += 1
        for heart in self.hearts:
            if not heart[2] and rect.inflate(16, 16).collidepoint(heart[0], heart[1]):
                heart[2] = True
                hearts += 1
        return coins, hearts

    def touch_checkpoint(self, rect):
        """Returns the new spawn point if a fresh checkpoint was touched."""
        for cp in self.checkpoints:
            if not cp["active"] and rect.colliderect(cp["rect"]):
                for other in self.checkpoints:
                    other["active"] = False
                cp["active"] = True
                return cp["spawn"]
        return None

    @property
    def coins_collected(self):
        return sum(1 for c in self.coins if c[2])

    # ------------------------------------------------------------ drawing
    def draw(self, surf, cam_x, cam_y, tick):
        view = pygame.Rect(cam_x - TILE, cam_y - TILE, 1000 + TILE * 2, 550 + TILE * 2)

        c0, c1 = max(0, int(cam_x) // TILE), min(self.cols, int(cam_x + 1000) // TILE + 1)
        r0, r1 = max(0, int(cam_y) // TILE), min(self.rows, int(cam_y + 550) // TILE + 1)
        for r in range(r0, r1):
            for c in range(c0, c1):
                if (c, r) in self.solid:
                    img = sprites.stone_tile((c, r - 1) not in self.solid)
                    surf.blit(img, (c * TILE - cam_x, r * TILE - cam_y))

        spike_img = sprites.spikes_surface()
        for spike in self.spikes:
            if view.colliderect(spike):
                surf.blit(spike_img, (spike.x - 6 - cam_x, spike.y + 24 - TILE - cam_y))

        saw_imgs = sprites.saw_frames()
        saw_img = saw_imgs[tick % len(saw_imgs)]
        for cx, cy, _ in self.saws:
            if view.collidepoint(cx, cy):
                surf.blit(saw_img, saw_img.get_rect(center=(cx - cam_x, cy - cam_y)))

        for cp in self.checkpoints:
            sprites.draw_checkpoint(surf, cp["rect"].move(-cam_x, -cam_y), cp["active"], tick)
        for x, y, got in self.coins:
            if not got and view.collidepoint(x, y):
                sprites.draw_coin(surf, (x - cam_x, y - cam_y), tick)
        for x, y, got in self.hearts:
            if not got and view.collidepoint(x, y):
                sprites.draw_heart_pickup(surf, (x - cam_x, y - cam_y), tick)
        sprites.draw_goal(surf, self.goal.move(-cam_x, -cam_y), tick)
