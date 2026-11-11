"""Every picture in the game is drawn with code, so no image files are needed.

To use your own art later, replace the functions here with
pygame.image.load("assets/your_file.png").convert_alpha().
"""
import math
import pygame
from settings import TILE

_cache = {}


def _cached(key, builder):
    if key not in _cache:
        _cache[key] = builder()
    return _cache[key]


# ---------------------------------------------------------------- Mochi (player)
def _mochi(pose="idle", dl=0, dr=0, bob=0, blink=False):
    """Draw the cute character big (3x), then shrink it so edges look smooth."""
    S = 3
    s = pygame.Surface((36 * S, 42 * S), pygame.SRCALPHA)
    OUT = (112, 80, 72)
    CREAM = (255, 246, 230)
    PINK = (255, 170, 185)
    DARKC = (58, 40, 46)
    jump = pose == "jump"
    lift = 8 if jump else (-4 if pose == "fall" else 0)
    fx = 4  # face shifted slightly so Mochi looks where it is heading

    # tail
    pygame.draw.circle(s, CREAM, (16, 100 + bob), 10)
    pygame.draw.circle(s, OUT, (16, 100 + bob), 10, 4)

    # feet
    for cx, d in ((40, dl), (70, dr)):
        rect = (cx - 13, 106 - d, 26, 16)
        pygame.draw.ellipse(s, (232, 196, 170), rect)
        pygame.draw.ellipse(s, OUT, rect, 4)

    # ears
    ear_l = [(22, 66 + bob), (27, 16 - lift + bob), (52, 48 + bob)]
    ear_r = [(86, 66 + bob), (81, 16 - lift + bob), (56, 48 + bob)]
    for ear in (ear_l, ear_r):
        pygame.draw.polygon(s, CREAM, ear)
        pygame.draw.polygon(s, OUT, ear, 4)
    pygame.draw.polygon(s, PINK, [(31, 58 + bob), (32, 30 - lift + bob), (45, 50 + bob)])
    pygame.draw.polygon(s, PINK, [(77, 58 + bob), (76, 30 - lift + bob), (63, 50 + bob)])

    # body
    body = (16, 48 + bob, 76, 64)
    pygame.draw.ellipse(s, CREAM, body)
    pygame.draw.ellipse(s, OUT, body, 4)

    # blush
    for cx in (30 + fx, 78 + fx):
        pygame.draw.ellipse(s, PINK, (cx - 9, 90 + bob, 18, 11))

    # eyes
    ey = 78 + bob
    for cx in (40 + fx, 68 + fx):
        if blink:
            pygame.draw.line(s, DARKC, (cx - 6, ey), (cx + 6, ey), 3)
        else:
            rx, ry = (7, 11) if jump else (6, 9)
            pygame.draw.ellipse(s, DARKC, (cx - rx, ey - ry, rx * 2, ry * 2))
            pygame.draw.circle(s, (255, 255, 255), (cx - 2, ey - 4), 3)

    # mouth
    if jump:
        pygame.draw.ellipse(s, (190, 80, 95), (54 + fx - 5, 92 + bob, 10, 12))
    else:
        pygame.draw.arc(s, DARKC, (48 + fx, 88 + bob, 7, 7), math.pi, 2 * math.pi, 3)
        pygame.draw.arc(s, DARKC, (55 + fx, 88 + bob, 7, 7), math.pi, 2 * math.pi, 3)

    return pygame.transform.smoothscale(s, (42, 49))


def player_frames():
    """Returns {1: frames facing right, -1: frames facing left}."""
    def build():
        right = {
            "idle": _mochi(),
            "blink": _mochi(blink=True),
            "jump": _mochi("jump", dl=6, dr=6),
            "fall": _mochi("fall"),
            "run": [_mochi("run", dl, dr, bob) for dl, dr, bob in
                    [(0, 7, 0), (3, 3, -3), (7, 0, 0), (3, 3, -3)]],
        }
        left = {}
        for k, v in right.items():
            if isinstance(v, list):
                left[k] = [pygame.transform.flip(i, True, False) for i in v]
            else:
                left[k] = pygame.transform.flip(v, True, False)
        return {1: right, -1: left}
    return _cached("player", build)


# ---------------------------------------------------------------- tiles
def stone_tile(top_grass):
    def build():
        s = pygame.Surface((TILE, TILE))
        s.fill((138, 141, 150))
        mortar = (98, 101, 111)
        bh = TILE // 4
        for i in range(4):
            y = i * bh
            pygame.draw.line(s, mortar, (0, y), (TILE, y), 1)
            x = 0 if i % 2 == 0 else TILE // 4
            while x < TILE:
                pygame.draw.line(s, mortar, (x, y), (x, y + bh), 1)
                x += TILE // 2
        pygame.draw.rect(s, (88, 91, 101), s.get_rect(), 1)
        if top_grass:
            pygame.draw.rect(s, (104, 196, 84), (0, 0, TILE, 9))
            pygame.draw.rect(s, (70, 150, 60), (0, 9, TILE, 2))
            for x in range(4, TILE, 10):
                pygame.draw.rect(s, (140, 220, 110), (x, 2, 4, 2))
        return s
    return _cached(("stone", top_grass), build)


# ---------------------------------------------------------------- hazards
def saw_frames(radius=24):
    def build():
        frames = []
        size = radius * 2 + 4
        c = (size / 2, size / 2)
        teeth = 12
        for k in range(6):  # 6 frames x 5 degrees = one 30 degree tooth cycle
            s = pygame.Surface((size, size), pygame.SRCALPHA)
            a0 = math.radians(5 * k)
            pts = []
            for i in range(teeth * 2):
                a = a0 + math.pi * i / teeth
                r = radius if i % 2 == 0 else radius - 6
                pts.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a)))
            pygame.draw.polygon(s, (176, 178, 186), pts)
            pygame.draw.polygon(s, (90, 92, 100), pts, 2)
            pygame.draw.circle(s, (206, 208, 214), c, radius - 9)
            pygame.draw.circle(s, (120, 122, 130), c, radius - 9, 2)
            pygame.draw.circle(s, (225, 110, 95), c, 6)
            pygame.draw.circle(s, (120, 40, 40), c, 6, 1)
            frames.append(s)
        return frames
    return _cached("saw", build)


def spikes_surface():
    def build():
        s = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
        n = 3
        w = TILE / n
        for i in range(n):
            pts = [(i * w + 1, TILE), (i * w + w / 2, TILE - 26), ((i + 1) * w - 1, TILE)]
            pygame.draw.polygon(s, (205, 208, 215), pts)
            pygame.draw.polygon(s, (90, 92, 100), pts, 2)
        return s
    return _cached("spikes", build)


# ---------------------------------------------------------------- pickups and flags
def heart_surface(size, color, outline=(90, 20, 30)):
    def build():
        s = pygame.Surface((size, size), pygame.SRCALPHA)

        def shape(col, grow):
            r = size * 0.22 + grow
            pygame.draw.circle(s, col, (size * 0.3, size * 0.34), r)
            pygame.draw.circle(s, col, (size * 0.7, size * 0.34), r)
            pygame.draw.polygon(s, col, [(size * 0.08 - grow, size * 0.42),
                                         (size * 0.92 + grow, size * 0.42),
                                         (size * 0.5, size * 0.92 + grow)])
        shape(outline, 1.5)
        shape(color, 0)
        pygame.draw.circle(s, (255, 255, 255), (int(size * 0.28), int(size * 0.28)), max(2, size // 10))
        return s
    return _cached(("heart", size, color), build)


def draw_coin(surface, center, tick):
    widths = [20, 15, 8, 15]
    w = widths[(tick // 8 + int(center[0]) // 50) % 4]
    bob = 3 * math.sin(tick * 0.08 + center[0] * 0.01)
    rect = pygame.Rect(0, 0, w, 20)
    rect.center = (center[0], center[1] + bob)
    pygame.draw.ellipse(surface, (255, 200, 40), rect)
    pygame.draw.ellipse(surface, (170, 110, 10), rect, 2)
    if w > 10:
        inner = rect.inflate(-8, -8)
        pygame.draw.ellipse(surface, (255, 235, 130), inner)


def draw_heart_pickup(surface, center, tick):
    img = heart_surface(28, (255, 70, 90))
    bob = 4 * math.sin(tick * 0.07)
    surface.blit(img, img.get_rect(center=(center[0], center[1] + bob)))


def draw_goal(surface, rect, tick):
    cx = rect.centerx
    bottom = rect.bottom
    top = bottom - 100
    pygame.draw.rect(surface, (90, 90, 100), (cx - 14, bottom - 8, 28, 8))
    pygame.draw.rect(surface, (120, 80, 50), (cx - 3, top, 6, 100))
    pygame.draw.circle(surface, (255, 200, 40), (cx, top), 6)
    wave = 4 * math.sin(tick * 0.15)
    pts = [(cx + 3, top + 6), (cx + 38, top + 18 + wave), (cx + 3, top + 32)]
    pygame.draw.polygon(surface, (255, 110, 130), pts)
    pygame.draw.polygon(surface, (150, 40, 60), pts, 2)


def draw_checkpoint(surface, rect, active, tick):
    cx = rect.centerx
    bottom = rect.bottom
    top = bottom - 46
    pygame.draw.rect(surface, (150, 150, 160), (cx - 2, top, 4, 46))
    color = (90, 210, 110) if active else (170, 170, 180)
    wave = 3 * math.sin(tick * 0.15) if active else 0
    pts = [(cx + 2, top + 2), (cx + 24, top + 10 + wave), (cx + 2, top + 20)]
    pygame.draw.polygon(surface, color, pts)
    pygame.draw.polygon(surface, (60, 70, 70), pts, 1)
