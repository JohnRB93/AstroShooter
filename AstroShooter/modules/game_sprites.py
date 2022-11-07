import pygame
import sys

class GameSprites():
    """Class to hold sprite images."""

    def __init__(self, astrogame):
        """Initializes the loading of sprite images."""
        self.screen = astrogame.screen
        self.images = self._get_sprite_images_dict()

    def _get_sprite_images_dict(self):
        """
        Creates a dictionary to store the file path of each sprite image/sheet,
        then call on a helper method to return a dictionary of surfaces for
        each sprite/sheet.
        """
        path = 'images/'
        images = {}
        images['asteroid'] = path+'asteroid.bmp'
        images['asteroid_hit'] = path+'asteroid_hit.bmp'
        images['bullet'] = path+'bullet.bmp'
        images['enemy_bullet'] = path+'enemy_bullet.bmp'
        images['super_bullet'] = path+'super_bullet.bmp'
        images['enemy_red_yellow'] = path+'enemy_1.bmp'
        images['enemy_grey_purple'] = path+'enemy_2.bmp'
        images['enemy_hit'] = path+'enemy_1_2_hit.bmp'
        images['ship'] = path+'ship.bmp'
        images['ship_hit'] = path+'ship_clear.bmp'
        images['ship_power_up'] = path+'ship_power_up.bmp'
        images['power_up'] = path+'power-up.bmp'
        images['asteroid_explosion_sheet'] = path+'asteroid_explosion_sheet.bmp'
        images['ship_explosion_sheet'] = path+'ship_explosion_sheet_2.bmp'
        images['red_firework'] = path+'redshot_sprite_sheet.bmp'
        images['blue_firework'] = path+'blueshot_sprite_sheet.bmp'
        images['up_arrow'] = path+'up_arrow.bmp'
        images['down_arrow'] = path+'down_arrow.bmp'

        return self._get_surfaces_dict(images)

    def _get_surfaces_dict(self, images):
        """Returns a dictionary containing the sprites loaded onto surfaces."""
        surfaces = {}
        for key in images.keys():
            try:
                path = images[key]
                image = pygame.image.load(path, key+'.bmp').convert()
            except:
                print('There was a problem locating one or more of the image files.')
                sys.exit()
            else:
                surfaces[key] = image

        return surfaces