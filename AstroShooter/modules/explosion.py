import pygame
from pygame.sprite import Sprite

from modules.spritesheet import SpriteSheet

class AsteroidExplosion(Sprite):
    """Class to manage asteroid explosions."""

    def __init__(self, astroshooter, asteroid, ticks):
        """Initializes the class."""
        super().__init__()
        self.screen = astroshooter.screen
        self.settings = astroshooter.settings
        self.sprite_images = astroshooter.sprite_images
        self.sheet = self.sprite_images['asteroid_explosion_sheet']
        self.asteroid = asteroid

        self.WIDTH = self.HEIGHT = 288
        self.ROWS = 2
        self.COLUMNS = 5
        self.FRAMES = 10

        self.row = self.column = 0

        self.explosion_sheet = SpriteSheet(self.sheet, self.settings,
                                           self.COLUMNS, self.ROWS)
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(self.settings.color_key)
        self.image.set_colorkey(self.settings.color_key)

        self.rect = pygame.Rect((0, 0), (self.WIDTH, self.HEIGHT))
        self.rect.x = float(self.asteroid.rect.x)
        self.rect.y = float(self.asteroid.rect.y)
        
        self.last_update = ticks
        self.animation_cooldown = 50
        self.frame = 0

        self.frame_list = self.explosion_sheet.get_image_list(
            self.WIDTH, self.HEIGHT)

    def update(self, current_ticks):
        """Updates the frame of the explosion animation based on ticks passed."""
        if current_ticks - self.last_update >= self.animation_cooldown:
            if self.frame < self.FRAMES:
                self.frame += 1
                self.last_update = current_ticks
        
        image = pygame.Surface((self.WIDTH, self.HEIGHT))
        image.fill(self.settings.color_key)
        image.set_colorkey(self.settings.color_key)
        image.blit(self.frame_list[self.frame], (0, 0))
        self.image = image.copy()


class ShipExplosion(Sprite):
    """Class to manage ship explosions."""
    def __init__(self, astroshooter, ship, ticks):
        """Initializes the class."""
        super().__init__()
        self.screen = astroshooter.screen
        self.settings = astroshooter.settings
        self.sprite_images = astroshooter.sprite_images
        self.sheet = self.sprite_images['ship_explosion_sheet']
        self.ship = ship

        self.WIDTH = self.HEIGHT = 144
        self.ROWS = 1
        self.COLUMNS = 6
        self.FRAMES = 6

        self.row = self.column = 0

        self.explosion_sheet = SpriteSheet(self.sheet, self.settings,
                                           self.COLUMNS, self.ROWS)
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(self.settings.color_key)
        self.image.set_colorkey(self.settings.color_key)

        self.rect = pygame.Rect((0, 0), (self.WIDTH, self.HEIGHT))
        self.rect.centerx = float(self.ship.rect.centerx)
        self.rect.centery = float(self.ship.rect.centery)
        
        self.last_update = ticks
        self.animation_cooldown = 50
        self.frame = 0

        self.frame_list = self.explosion_sheet.get_image_list(
            self.WIDTH, self.HEIGHT)

    def update(self, current_ticks):
        """Updates the frame of the explosion(Group) animation based on ticks passed."""
        if current_ticks - self.last_update >= self.animation_cooldown:
            if self.frame < self.FRAMES:
                self.frame += 1
                self.last_update = current_ticks
        
        image = pygame.Surface((self.WIDTH, self.HEIGHT))
        image.fill(self.settings.color_key)
        image.set_colorkey(self.settings.color_key)
        image.blit(self.frame_list[self.frame], (0, 0))
        self.image = image.copy()
