import pygame

from pygame.sprite import Sprite
from random import randint

from modules.bullet import EnemyBullet

class RedYellowEnemy(Sprite):
    """Class to manage enemies that move up and down the screen."""

    def __init__(self, astroshooter):
        """Initializes the red/yellow enemy."""
        super().__init__()
        self.settings = astroshooter.settings
        self.screen_rect = astroshooter.screen_rect
        self.sprite_images = astroshooter.sprite_images

        self.direction = {
            'up': False,
            'down': False,
            'left': False,
            'right': False,
        }
        self.image = self.sprite_images['enemy_red_yellow']
        self.image.set_colorkey(self.settings.color_key)
        self.rect = self.image.get_rect()
        
        # Sets up variables for the travel path for the enemy to follow.
        self.vertical_distance = float(self.screen_rect.bottom -
                                  self.screen_rect.top + self.rect.height)
        self.vd_copy = self.vertical_distance
        self.horizontal_distance = float(self.screen_rect.width / 5)
        self.hd_copy = self.horizontal_distance
        self.rect.midtop = (self.horizontal_distance * 4, self.screen_rect.bottom)

        self.direction['up'] = True
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
        if self.rect.left < self.screen_rect.left:
            return

        if self.direction['up']:
            self.y -= self.settings.ry_enemy_speed
            self.rect.centery = self.y
            self.vertical_distance -= self.settings.ry_enemy_speed
            if self.vertical_distance <= 0:
                self.vertical_distance = self.vd_copy
                self.direction['up'] = False
                self.direction['left'] = True
        elif self.direction['down']:
            self.y += self.settings.ry_enemy_speed
            self.rect.centery = self.y
            self.vertical_distance -= self.settings.ry_enemy_speed
            if self.vertical_distance <= 0:
                self.vertical_distance = self.vd_copy
                self.direction['down'] = False
                self.direction['left'] = True
        elif self.direction['left']:
            self.x -= self.settings.ry_enemy_speed
            self.rect.centerx = self.x
            self.horizontal_distance -= self.settings.ry_enemy_speed
            if self.horizontal_distance <= 0:
                self.horizontal_distance = self.hd_copy
                self.direction['left'] = False
                if self.rect.centery > 0:
                    self.direction['up'] = True
                else:
                    self.direction['down'] = True

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
            number = randint(1, 201)
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
            self.image = self.sprite_images['enemy_red_yellow']
            self.image.set_colorkey(self.settings.color_key)

    def _fire_enemy_bullet(self, astroshooter):
        """Creates enemy bullets and adds them to game's sprite group."""
        astroshooter.enemy_bullets.add(EnemyBullet(self, astroshooter))
        astroshooter.play_sound_effect(self.settings.fire_bullet_sound,
                                       self.settings.fire_bullet_sound_vol)