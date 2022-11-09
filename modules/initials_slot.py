import pygame

class InitialsSlot():
    """Class to manage the initials slots when the player enters their initials."""

    def __init__(self, game):
        """Initializes the initial slots."""
        self.screen = game.screen
        self.screen_rect = game.screen_rect
        self.settings = game.settings
        self.stats = game.stats
        self.font = pygame.font.SysFont(None, 75)

        self.init_1_index = 1
        self.init_2_index = 1
        self.init_3_index = 1
        
        self.up_arrow_image = game.sprite_images['up_arrow']
        self.up_arrow_image.set_colorkey(self.settings.color_key)
        self.up_arrow_rect = self.up_arrow_image.get_rect()
        self.down_arrow_image = game.sprite_images['down_arrow']
        self.down_arrow_image.set_colorkey(self.settings.color_key)
        self.down_arrow_rect = self.down_arrow_image.get_rect()

        self.init_1_selected = True
        self.init_2_selected = False
        self.init_3_selected = False
        self.initials_confirmed = False
        
    def display_initials_box(self, y_pos):
        """Displays the box for the player to enter their initials into."""
        self.init_image_1 = self.font.render(
            self.settings.characters[self.init_1_index], True, (255, 255, 255))
        self.init_image_2 = self.font.render(
            self.settings.characters[self.init_2_index], True, (255, 255, 255))
        self.init_image_3 = self.font.render(
            self.settings.characters[self.init_3_index], True, (255, 255, 255))
        
        inits_rect = pygame.Rect(0, y_pos, 225, 75)
        inits_rect.centerx = self.screen_rect.centerx
        
        self.init_1_rect = self.init_image_1.get_rect(topleft = (inits_rect.topleft))
        self.init_2_rect = self.init_image_2.get_rect(midtop = (inits_rect.midtop))
        self.init_3_rect = self.init_image_3.get_rect(topright = (inits_rect.topright))
        
        self.screen.blits(((self.init_image_1, self.init_1_rect),
                          (self.init_image_2, self.init_2_rect),
                          (self.init_image_3, self.init_3_rect),
                          (self.up_arrow_image, self.up_arrow_rect),
                          (self.down_arrow_image, self.down_arrow_rect)))

        if self.init_1_selected:
            self.up_arrow_rect.midbottom = self.init_1_rect.midtop
            self.down_arrow_rect.midtop = self.init_1_rect.midbottom
        elif self.init_2_selected:
            self.up_arrow_rect.midbottom = self.init_2_rect.midtop
            self.down_arrow_rect.midtop = self.init_2_rect.midbottom
        elif self.init_3_selected:
            self.up_arrow_rect.midbottom = self.init_3_rect.midtop
            self.down_arrow_rect.midtop = self.init_3_rect.midbottom

    def change_character(self, direction):
        """Changes the character on the active slot according to player's input."""
        if self.init_1_selected:
            if direction == 'up' and self.init_1_index != len(self.settings.characters)-1:
                self.init_1_index += 1
            elif direction == 'up' and self.init_1_index == len(self.settings.characters)-1:
                self.init_1_index = 0
            elif direction == 'down' and self.init_1_index != 0:
                self.init_1_index -= 1
            elif direction == 'down' and self.init_1_index == 0:
                self.init_1_index = len(self.settings.characters)-1
            elif direction == 'right':
                self.change_slot(direction, 1)
        elif self.init_2_selected:
            if direction == 'up' and self.init_2_index != len(self.settings.characters)-1:
                self.init_2_index += 1
            elif direction == 'up' and self.init_2_index == len(self.settings.characters)-1:
                self.init_2_index = 0
            elif direction == 'down' and self.init_2_index != 0:
                self.init_2_index -= 1
            elif direction == 'down' and self.init_2_index == 0:
                self.init_2_index = len(self.settings.characters)-1
            elif direction == 'right':
                self.change_slot(direction, 2)
            elif direction == 'left':
                self.change_slot(direction, 2)
        elif self.init_3_selected:
            if direction == 'up' and self.init_3_index != len(self.settings.characters)-1:
                self.init_3_index += 1
            elif direction == 'up' and self.init_3_index == len(self.settings.characters)-1:
                self.init_3_index = 0
            elif direction == 'down' and self.init_3_index != 0:
                self.init_3_index -= 1
            elif direction == 'down' and self.init_3_index == 0:
                self.init_3_index = len(self.settings.characters)-1
            elif direction == 'left':
                self.change_slot(direction, 3)

    def change_slot(self, direction, selected_slot):
        """Changes which slot is the active one."""
        if direction == 'right' and selected_slot == 1:
            self.init_1_selected = False
            self.init_2_selected = True
        elif direction == 'right' and selected_slot == 2:
            self.init_2_selected = False
            self.init_3_selected = True
        elif direction == 'left' and selected_slot == 2:
            self.init_2_selected = False
            self.init_1_selected = True
        elif direction == 'left' and selected_slot == 3:
            self.init_3_selected = False
            self.init_2_selected = True

    def confirm_initials(self):
        """
        Assigns the selected elements of the characters list to the initials
        variable and assigns initials_confirmed to True.
        """
        self.stats.initials += (self.settings.characters[self.init_1_index] +
                                self.settings.characters[self.init_2_index] +
                                self.settings.characters[self.init_3_index])
        self.initials_confirmed = True