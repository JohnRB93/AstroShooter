import pygame
import random
from pygame.sprite import Sprite

class Asteroid(Sprite):
    """Class to manage an astriod."""

    def __init__(self, astroshooter):
        """Initializes the asteriod."""
        super().__init__()
        self.screen = astroshooter.screen
        self.settings = astroshooter.settings
        self.screen_rect = astroshooter.screen.get_rect()
        self.sprite_images = astroshooter.sprite_images
        
        self.original_image = self.sprite_images['asteroid']
        self.original_image.set_colorkey(self.settings.color_key)
        self.hit_original_image = self.sprite_images['asteroid_hit']
        self.hit_original_image.set_colorkey(self.settings.color_key)

        self.image = self.original_image.copy()
        self.rect = self.original_image.get_rect(left = self.screen_rect.right - 1)
        self.rect.y = float(random.choice(range(0, self.screen_rect.bottom-self.rect.h)))
        
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        self.radius = float(self.rect.width / 2)

        self.hits = 5
        self.hit = False
        self.hit_number = 1
        self.init_hit_ticks = 0
        self.HIT_TICK_LIMIT = 100

        self.degrees_total = 0
        self.degrees = 1.3

    def update(self):
        """Updates the location of the asteroids in the group."""
        if self.hits != 0:
            self.centerx -= self.settings.asteroid_speed
            self.rect.centerx = self.centerx
            self.rect.centery = self.centery

    def update_individual(self, current_ticks=0):
        """Updates the asteroid instance, seperately from the group."""
        if current_ticks > 0:
            if current_ticks - self.init_hit_ticks >= self.HIT_TICK_LIMIT:
                self.hit = False
                self.hit_number = 2
                self._update_hit_image()

        if self.hit:
            self._update_hit_image()
            self.hit_number += 1
        else:
            new_rect = self._rotate_asteroid()
            self.rect = new_rect

    def _update_hit_image(self):
        """Updates the image if the asteroid has been hit."""
        if self.hit_number % 2 != 0:
            image_copy = self.sprite_images['asteroid_hit']
            image_copy.set_colorkey(self.settings.color_key)
            self.image = pygame.transform.rotate(image_copy, self.degrees_total)
            self.rect = self.image.get_rect()
            self.rect.centerx = self.centerx
            self.rect.centery = self.centery
            self.degrees_total += self.degrees
        else:
            image_copy = self.sprite_images['asteroid']
            image_copy.set_colorkey(self.settings.color_key)
            self.image = pygame.transform.rotate(image_copy, self.degrees_total)
            self.rect = self.image.get_rect()
            self.rect.centerx = self.centerx
            self.rect.centery = self.centery
            self.degrees_total += self.degrees

    def _rotate_asteroid(self):
        """Rotates the asteroid from its center."""
        image_copy = self.original_image
        self.image = pygame.transform.rotate(image_copy, self.degrees_total)
        self.degrees_total += self.degrees
        return self.image.get_rect(center = (self.centerx, self.centery))