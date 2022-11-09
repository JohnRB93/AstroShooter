import pygame

class GameIntro():
    """Class to manage the game's introductory screen."""

    def __init__(self, game):
        """Initializes the values of the game intro."""
        self.screen = game.screen
        self.screen_rect = game.screen_rect
        self.settings = game.settings
        self.stats = game.stats
        self.clock = game.clock
        self.FPS = game.FPS
        self.DURATION = 14_500
        self.game_msg_dict = {
            'title': 'Astro Shooter',
            'header': 'Produced by John Butler',
            'story_1': 'The year is 30XX.',
            'story_2': 'A planet within a lone solar system,',
            'story_3': 'rich with resources, has been discoverd.',
            'story_4': 'The planet, named "72X00B1",',
            'story_5': 'now commands the attention of two intergalactic species.',
            'story_6': 'One being Huemoids, the android descendants of humans, and',
            'story_7': 'the other being Temikulans from the Andromeda Galaxy.',
            'story_8': 'These two races, strapped for resources,',
            'story_9': 'are now on the brink of war!',
            'story_10': 'The battle is about to begin!!',
            'story_11': 'Show the Temikulans no mercy and win at all costs!!!',
        }
        
        self.title_font = pygame.font.SysFont(None, 78)
        self.header_font = pygame.font.SysFont(None, 54)
        self.story_font = pygame.font.SysFont(None, 36)
        self.text_images = []
        self.text_rects = []
        
        i = 1
        for line in self.game_msg_dict.values():
            if line == self.game_msg_dict['title']:
                self.text_images.append(self.title_font.render(
                    self.game_msg_dict['title'], True, (255, 255, 255)))
            elif line == self.game_msg_dict['header']:
                self.text_images.append(self.header_font.render(
                    self.game_msg_dict['header'], True, (255, 255, 255)))
            else:
                self.text_images.append(self.story_font.render(
                    self.game_msg_dict[f'story_{i}'], True, (255, 255, 255)))
                i += 1

        for image in self.text_images:
            self.text_rects.append(image.get_rect())

        self.intro_event_type = pygame.event.custom_type()
        self.args_dict = {
            'header speed': self.settings.header_speed,
            'story speed': self.settings.story_text_speed,
        }
        self.intro_event = pygame.event.Event(self.intro_event_type, self.args_dict)
        self._plot_init_text_coordinates()

    def _plot_init_text_coordinates(self):
        """Plots the coordinates for the text rectangles."""
        line_space = 1
        i = 0
        
        for text_rect in self.text_rects:
            if i == 0:
                text_rect.centerx = self.screen_rect.centerx
                text_rect.bottom = self.screen_rect.bottom - 160
                i += 1
            elif i == 1:
                text_rect.centerx = self.screen_rect.centerx
                text_rect.bottom = self.screen_rect.bottom - 25
                i += 1
            else:
                text_rect.centerx = self.screen_rect.centerx
                text_rect.top = self.screen_rect.bottom + line_space
                line_space += 55

    def display_game_intro(self, ticks):
        """Displays the game's introductory screen to the player."""
        initial_ticks = ticks
        while self.stats.game_intro_active:
            self.clock.tick(self.FPS)
            self.screen.fill((0, 0, 0))
            self._intro_events()
            pygame.display.flip()
            if pygame.time.get_ticks() >= initial_ticks + (self.DURATION - 15):
                self._draw_title()
            if pygame.time.get_ticks() >= initial_ticks + self.DURATION:
                self.stats.game_intro_active = False
                pygame.event.clear()

    def _intro_events(self):
        """Checks for events during the introductory sequence."""
        pygame.event.post(self.intro_event)
        for event in pygame.event.get():
            if event.type == self.intro_event_type:
                self._handle_intro(event)
                pygame.event.clear()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.stats.game_intro_active = False
                    pygame.event.clear()

    def _handle_intro(self, event):
        """Handles the logic for animating the intro sequence."""
        i = 0
        for text_rect in self.text_rects:
            if i >= 2:
                text_rect.y -= event.__dict__['story speed']
                self.screen.blit(self.text_images[i], text_rect)
                
            i += 1

    def _draw_title(self):
        """Draws the 'produced by' and 'title' texts to the screen."""
        self.screen.blit(self.text_images[0], self.text_rects[0])
        self.screen.blit(self.text_images[1], self.text_rects[1])