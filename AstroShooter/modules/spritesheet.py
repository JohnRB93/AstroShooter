import pygame

class SpriteSheet():
    """Class to manage sprite sheets."""

    def __init__(self, sheet_image, settings, columns, rows):
        """Initializes the sprite sheet."""
        self.settings = settings
        self.ROWS = rows
        self.COLUMNS = columns
        self.sprite_sheet = sheet_image

    def _get_image(self, width, height, frame_column, frame_row=0, scale=1):
        """Returns the specified frame from the sprite sheet as a surface image."""
        image = pygame.Surface((width, height))
        rect = image.get_rect()
        image.blit(self.sprite_sheet, rect,
                   (frame_column * width, frame_row * height, width, height))

        if scale != 1:
            image = pygame.transform.scale(image, (width * scale, height * scale))

        image.set_colorkey(self.settings.color_key)
        return image.convert()

    def get_image_list(self, width, height, scale=1):
        """Returns a list of surfaces from the sprite sheet for animation."""
        image_list = []

        if self.ROWS > 0:
            x = y = 0
            for row in range(1, self.ROWS+1):
                image_list.append(self._get_image(width, height, x, y, scale))
                for column in range(1, self.COLUMNS+1):
                    image_list.append(self._get_image(width, height, x, y, scale))
                    x += 1
                x = 0
                y += 1

        else:
            for column in range(0, self.COLUMNS):
                image_list.append(self._get_image(width, height, column, scale))

        return image_list
                 
                
            