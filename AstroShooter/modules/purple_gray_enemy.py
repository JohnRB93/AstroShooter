import pygame

from pygame.sprite import Sprite
from random import randint

from modules.bullet import EnemyBullet

class PurpleGrayEnemy(Sprite):
    """Class to manage enemies that moves left on the screen."""

    def __init__(self, astroshooter):
        """Initializes the puple/gray enemy."""
        super().__init__()
        self.settings = astroshooter.settings
        self.screen_rect = astroshooter.screen_rect
        self.sprite_images = astroshooter.sprite_images

        self.direction = {
            'up': False,
            'down': False,
            'left': True,
            'right': False,
        }
        self.image = self.sprite_images['enemy_grey_purple']
        self.image.set_colorkey(self.settings.color_key)
        self.rect = self.image.get_rect()
        
        self.rect.left = self.screen_rect.right
        self.rect.top = randint(0, self.screen_rect.height - self.rect.height)

        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)
        self.radius = float(self.rect.width / 2)

        self.hits = 3
        self.hit = False
        self.hit_number = 1

        self.init_hit_ticks = 0
        self.HIT_TICK_LIMIT = 100
        
    def update(self):
        """Updates the location and direction of all enemies in the Group."""
        if self.direction['left']:
            self.x -= self.settings.pg_enemy_speed
            self.rect.x = self.x

    def update_individual(self, astroshooter, current_ticks=0):
        """Updates the individual instance of enemy, seperate from the Group."""
        if current_ticks > 0:
            if current_ticks - self.init_hit_ticks >= self.HIT_TICK_LIMIT:
                self.hit = False
                self.hit_number = 2
                self._update_hit_image()

        if self.hit:
            self._update_hit_image()
            self.hit_number += 1
        else:
            number = randint(1, 231)
            if number == 1:
                self._fire_enemy_bullet(astroshooter)

    def _update_hit_image(self):
        """
        Updates the image to indicate the enemy has taken damage or to return
        to normal image.
        """
        if self.hit_number % 2 != 0:
            self.image = self.sprite_images['enemy_hit']
            self.image.set_colorkey(self.settings.color_key)
        else:
            self.image = self.sprite_images['enemy_grey_purple']
            self.image.set_colorkey(self.settings.color_key)

    def _fire_enemy_bullet(self, astroshooter):
        """Creates enemy bullets and adds them to game's sprite group."""
        astroshooter.enemy_bullets.add(EnemyBullet(self, astroshooter))
        astroshooter.play_sound_effect(self.settings.fire_bullet_sound,
                                       self.settings.fire_bullet_sound_vol)