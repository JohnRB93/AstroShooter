import pygame
import json

class Stats():
    """Class to manage score, statistics, etc."""

    def __init__(self, astroshooter):
        """Initializes score, statistics, etc."""
        self.screen = astroshooter.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = astroshooter.settings
        self.enemies_destroyed = 0
        self.asteroids_destroyed = 0
        self.game_intro_active = True
        self.game_over = False
        self.lost_ship = False
        self.game_active = False
        self.paused = False
        self.game_quit = False
        self.font = pygame.font.SysFont(None, 36)
        self.color_key = (0, 0, 0)
        self.initials = ''
        self.start_button_active = False
        self.about_button_active = False
        
        # Initialization and placement of score/stats rects.
        self.score = 0
        self.score_image = pygame.Surface((250, 50))
        self.score_image.set_colorkey(self.color_key)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.topleft = (0, 0)

        self.high_score = 0
        self.high_score_image = pygame.Surface((260, 50))
        self.high_score_image.set_colorkey(self.color_key)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.midtop = self.screen_rect.midtop

        self.level = 1
        self.level_image = pygame.Surface((250, 50))
        self.level_image.set_colorkey(self.color_key)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.topright = self.screen_rect.topright

        self.ships_left = 3
        self.ships_left_image = pygame.Surface((250, 50))
        self.ships_left_image.set_colorkey(self.color_key)
        self.ships_left_rect = self.ships_left_image.get_rect()
        self.ships_left_rect.bottomleft = self.screen_rect.bottomleft

    def load_high_score(self):
        """Loads the high score from a json-formatted txt file."""
        try:
            filepath = 'statistics/high_score.json'
            with open(filepath) as high_score_file:
                high_score_data = json.load(high_score_file)
                self.high_score = high_score_data['Player']['High Score']
        except:
            FileNotFoundError('The high score couldn\'n be loaded.')
            self.high_score = -1
            
    def save_high_score(self):
        """Saves the player's initials, level, and score into a json file."""
        high_score_data = None
        try:
            filepath = 'statistics/high_score.json'
            with open(filepath) as high_score_file:
                high_score_data = json.load(high_score_file)
                high_score_data['Player']['Initials'] = self.initials
                high_score_data['Player']['Level'] = self.level
                high_score_data['Player']['High Score'] = self.score
        except:
            FileNotFoundError('The high score couldn\'n be saved.')

        try:
            filepath = 'statistics/high_score.json'
            with open(filepath, 'w') as high_score_file:
                json.dump(high_score_data, high_score_file)
        except:
            FileNotFoundError('The high score couldn\'n be saved.')
        finally:
            self.high_score = high_score_data['Player']['High Score']
    def render_stats(self):
        """Calls on the helper methods to render each stat on to the screen."""
        self._render_score('Score: ' + str(self.score))
        self._render_high_score('High Score: ' + str(self.high_score))
        self._render_level('Level: ' + str(self.level))
        self._render_ships_left('Ships Left: ' + str(self.ships_left))

    def _render_score(self, score):
        """Draws the score onto the score rectangle."""
        self.score_image.fill((0, 0, 0))
        _image = self.font.render(score, True, (255, 255, 254))
        self.score_image.blit(_image, (30, 17.5))

    def _render_high_score(self, high_score):
        """Draws the high score onto the high score rectangle."""
        self.high_score_image.fill((0, 0, 0))
        _image = self.font.render(high_score, True, (255, 255, 254))
        self.high_score_image.blit(_image, (30, 17.5))

    def _render_level(self, level):
        """Draws the level onto the level rectangle."""
        self.level_image.fill((0, 0, 0))
        _image = self.font.render(level, True, (255, 255, 254))
        self.level_image.blit(_image, (30, 17.5))

    def _render_ships_left(self, ships_left):
        """Draws the ships left onto the score rectangle."""
        self.ships_left_image.fill((0, 0, 0))
        _image = self.font.render(ships_left, True, (255, 255, 254))
        self.ships_left_image.blit(_image, (30, 17.5))

    def blit_stats(self):
        """Draws the statistics rects onto the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.ships_left_image, self.ships_left_rect)