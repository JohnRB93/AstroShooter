import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Class to manage bullets on screen."""

    def __init__(self, astrogame):
        """Initializes bullet properties."""
        super().__init__()
        self.settings = astrogame.settings
        self.ship = astrogame.ship.sprite
        self.screen = astrogame.screen
        self.sprite_images = astrogame.sprite_images

        if not self.ship.powered_up:
            self.image = self.sprite_images['bullet']
        else:
            self.image = self.sprite_images['super_bullet']
            
        self.image.set_colorkey(self.settings.color_key)
        self.rect = self.image.get_rect()
        self.rect.midright = self.ship.rect.midright
        self.x = float(self.rect.x)
        self.radius = float(self.rect.width / 2)

        self.IS_SUPER = self.ship.powered_up

    def update(self):
        """Updates the location of the bullt."""
        self.x += self.settings.bullet_speed
        self.rect.x = self.x
        

class EnemyBullet(Sprite):
    """Class to manage enemy bullets on screen."""

    def __init__(self, enemy, astrogame):
        """Initializes bullet properties."""
        super().__init__()
        self.settings = astrogame.settings
        self.screen = astrogame.screen
        self.sprite_images = astrogame.sprite_images
        self.sprite_images = self.sprite_images
        self.image = self.sprite_images['enemy_bullet']
        self.image.set_colorkey(self.settings.color_key)
        self.rect = self.image.get_rect()

        # Initialization of rect that will be used to draw/update the bullets.
        self.x = float(enemy.rect.left)
        self.y = float(enemy.rect.centery + 1)
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        """Updates the location of the bullt."""
        self.x -= self.settings.bullet_speed
        self.rect.x = self.x