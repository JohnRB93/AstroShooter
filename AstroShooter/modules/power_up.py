import pygame

from pygame.sprite import Sprite
from random import randint

class PowerUp(Sprite):
    """Class to manage power-ups."""

    def __init__(self, game):
        """Initializes the power-up variables."""
        super().__init__()
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        
        self.image = game.sprite_images['power_up']
        self.image.set_colorkey(self.settings.color_key)
        self.rect = self.image.get_rect()

        self.rect.left = self.screen_rect.right + 1
        self.rect.top = randint(0, self.screen_rect.height - self.rect.height)

        self.screen.blit(self.image, self.rect)

    def update(self):
        """Updates the location of the power-up sprite."""
        self.rect.x -= self.settings.power_up_speed