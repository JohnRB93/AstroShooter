import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	"""Class to manage the player's ship."""

	def __init__(self, astroshooter):
		"""Initialize the ship image and set its starting position."""
		super().__init__()
		self.screen = astroshooter.screen
		self.settings = astroshooter.settings
		self.screen_rect = astroshooter.screen.get_rect()

		self.sprite_images = astroshooter.sprite_images
		self.image = self.sprite_images['ship']
		self.rect = self.image.get_rect()
		self.rect.midleft = self.screen_rect.midleft
		self.image.set_colorkey(self.settings.color_key)
		
		self.y = float(self.rect.y)

		self.move = {
			'up': False,
			'down': False,
		}

		self.hits = 3
		self.hit_buffer = False
		self.hb_number = 1
		self.hit_init_ticks = 0
		self.HIT_TICK_LIMIT = 2_000

		self.radius = float(self.rect.width / 2)

		self.powered_up = False
		self.POWER_UP_TICK_LIMIT = 7_000
		self.init_power_up_tick = self.current_power_up_tick = 0

	def update(self):
		"""Update the ship's position and direction based on the movement flags."""
		if self.move['up'] and self.rect.top > self.screen_rect.top:
			self.y -= self.settings.ship_speed
			self.rect.y = self.y

		if self.move['down'] and self.rect.bottom < self.screen_rect.bottom:
			self.y += self.settings.ship_speed
			self.rect.y = self.y

		if self.hit_buffer:
			self.update_hit_buffer_image(pygame.time.get_ticks())

		if self.powered_up:
			self.current_power_up_tick = pygame.time.get_ticks()
			if self.current_power_up_tick - self.init_power_up_tick >= self.POWER_UP_TICK_LIMIT:
				self.powered_up = False
				self.update_power_up()

	def update_hit_buffer_image(self, current_ticks):
		"""
		Causes the ship's image to blink rapidly if hit buffer is true.
		Default argument value of 1 loads the normal image.
		"""
		if current_ticks - self.hit_init_ticks > self.HIT_TICK_LIMIT:
			self.hit_buffer = False
			self.hb_number = 1

		if self.hb_number % 2 == 0:
			self.image = self.sprite_images['ship_hit']
			self.image.set_colorkey(self.settings.color_key)
		else:
			self.image = self.sprite_images['ship']
			self.image.set_colorkey(self.settings.color_key)

		self.hb_number += 1

	def update_power_up(self):
		"""Updates the power up."""
		if self.powered_up:
			self.init_power_up_tick = pygame.time.get_ticks()
			self.image = self.sprite_images['ship_power_up']
			self.image.set_colorkey(self.settings.color_key)
		else:
			self.image = self.sprite_images['ship']
			self.image.set_colorkey(self.settings.color_key)
			
	def blitme(self):
		"""Draw the ship at its current location."""
		self.screen.blit(self.image, self.rect)