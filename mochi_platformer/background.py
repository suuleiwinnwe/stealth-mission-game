
"""Scrolling landscape image background."""

from pathlib import Path
import pygame
from settings import SCREEN_W, SCREEN_H

IMAGE_PATH = Path(__file__).resolve().parent / "assets" / "forest.png"


class Background:
    def __init__(self):
        image = pygame.image.load(str(IMAGE_PATH)).convert()

        # Keep the original image proportions.
        scale = SCREEN_H / image.get_height()
        width = max(SCREEN_W, int(image.get_width() * scale))

        self.image = pygame.transform.smoothscale(
            image, (width, SCREEN_H)
        )
        self.width = width

    def draw(self, screen, cam_x):
        # Move the scenery more slowly than the player.
        offset = int(cam_x * 0.3) % self.width

        screen.blit(self.image, (-offset, 0))
        screen.blit(self.image, (self.width - offset, 0))

        # Fill any remaining space for narrow images.
        x = 2 * self.width - offset
        while x < SCREEN_W:
            screen.blit(self.image, (x, 0))
            x += self.width
