import pygame

class Button():
    """Class to manage buttons that may appear on screen."""

    def __init__(self, astroshooter, color, x, y):
        """Initializes the button's values."""
        self.screen = astroshooter.screen

        self.WIDTH, self.HEIGHT = 250, 50

        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.rect = pygame.draw.rect(self.image, color,
                                     self.image.get_rect(),
                                     width=0, border_radius=5)
        self.rect.centerx = x
        self.rect.centery = y
        self.font = pygame.font.SysFont(None, 48)

    def render_text(self, text):
        """Displays the text on the button."""
        text_image = self.font.render(text, True, (255, 255, 255))
        text_image_rect = text_image.get_rect()
        text_image_rect.centerx = self.rect.centerx
        text_image_rect.centery = self.rect.centery

        x = text_image_rect.x - self.rect.x
        y = text_image_rect.y - self.rect.y

        self.image.blit(text_image, (x, y))

    def blitme(self):
        """Draws the button onto the screen."""
        self.screen.blit(self.image, self.rect)