import pygame
from pygame.sprite import Sprite

from random import randint

class BackGroundStar(Sprite):
    """Class to manage the background."""

    def __init__(self, astroshooter):
        """Initializes the background variables."""
        super().__init__()
        self.screen = astroshooter.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = astroshooter.settings

        self.radius = randint(3, 10)
        self.image = pygame.Surface((self.radius, self.radius))
        self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect()

        self.x = float(self.screen_rect.right + 1)
        self.y = float(randint(10, self.screen_rect.bottom + 10))

        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        """Updates the star's location."""
        self.x -= self.settings.bg_star_speed
        self.rect.x = self.x
