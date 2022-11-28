import pygame
from pygame.sprite import Sprite

from modules.spritesheet import SpriteSheet

from random import randint

class FireWork(Sprite):
    """Manages fireworks."""

    def __init__(self, game, ticks):
        """Initializes the firework."""
        super().__init__()
        self.screen = game.screen
        self.screen_rect = game.screen_rect
        self.settings = game.settings
        self.sprite_images = game.sprite_images
        self.sheet = self._get_firework_sheet()
        self.coordinate = self._get_coordinate()
        self.WIDTH = self.HEIGHT = 200
        self.ROWS = 1
        self.COLUMNS = 8
        self.FRAMES = 8

        self.firework_sheet = SpriteSheet(self.sheet, self.settings,
                                          self.COLUMNS, self.ROWS)
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(self.settings.color_key)
        self.image.set_colorkey(self.settings.color_key)

        self.rect = pygame.Rect((0, 0), (self.WIDTH, self.HEIGHT))
        self.rect.centerx = float(self.coordinate[0])
        self.rect.centery = float(self.coordinate[1])
        
        self.last_update = ticks
        self.animation_cooldown = 60
        self.frame = 0

        self.frame_list = self.firework_sheet.get_image_list(
            self.WIDTH, self.HEIGHT)

    def update(self, current_ticks):
        """Updates the frame of the firework animation based on ticks passed."""
        if current_ticks - self.last_update >= self.animation_cooldown:
            if self.frame < self.FRAMES:
                self.frame += 1
                self.last_update = current_ticks
        
        image = pygame.Surface((self.WIDTH, self.HEIGHT))
        image.fill(self.settings.color_key)
        image.set_colorkey(self.settings.color_key)
        image.blit(self.frame_list[self.frame], (0, 0))
        self.image = image.copy()

    def _get_firework_sheet(self):
        """Returns a sprite sheet of a randomly colored firework."""
        number = randint(1,2)
        if number == 1:
            return self.sprite_images['red_firework']
        elif number == 2:
            return self.sprite_images['blue_firework']

    def _get_coordinate(self):
        """Returns a randomly chosen coordinate for the firework to be placed."""
        x = randint(0, self.screen_rect.right)
        y = randint(0, self.screen_rect.bottom)
        return (x, y)