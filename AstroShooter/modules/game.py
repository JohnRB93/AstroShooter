"""
TODO:
      Implement online high score funcionality.
      Implement levels.
      Implement boss at end of levels.
"""

import sys
import pygame

from pygame import mixer
from random import randint

from modules.settings import Settings
from modules.game_sprites import GameSprites
from modules.ship import Ship
from modules.bullet import Bullet
from modules.asteroid import Asteroid
from modules.red_yellow_enemy import RedYellowEnemy
from modules.purple_gray_enemy import PurpleGrayEnemy
from modules.explosion import AsteroidExplosion, ShipExplosion
from modules.bgstar import BackGroundStar
from modules.stats import Stats
from modules.button import Button
from modules.power_up import PowerUp
from modules.firework import FireWork
from modules.initials_slot import InitialsSlot
from modules.game_intro import GameIntro

class AstroShooter:
    """Class that oversees the overall game behaviour and resources."""

    def __init__(self):
        """Initializes the game and creates game resources."""
        pygame.init()
        pygame.mixer.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.screen_size = pygame.display.get_window_size()
        self.screen.fill(self.settings.bg_color)
        game_sprites = GameSprites(self)
        self.sprite_images = game_sprites.images
        pygame.display.set_caption("Astro Shooter")
        
        self.ship = pygame.sprite.GroupSingle(Ship(self))
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.player_explosion = pygame.sprite.GroupSingle()
        self.bg_stars = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        self.fireworks = pygame.sprite.Group()

        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.stats = Stats(self)
        self.stats.load_high_score()
        self.start_button = Button(self, (76, 177, 34),
                                   self.screen_rect.centerx-185,
                                   self.screen_rect.centery)
        self.about_button = Button(self, (76, 177, 34),
                                   self.screen_rect.centerx+185,
                                   self.screen_rect.centery)
        self.init_slots = InitialsSlot(self)
        self.game_intro = GameIntro(self)

#=========================================================== Main Game Loop ===
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self.clock.tick(self.FPS)

            if self.stats.game_intro_active:
                self.intro_screen()
                self.start_screen()
                self.stats.game_active = True

            if self.stats.game_active:
                self.check_events()
                self.make_sprites()
                self.update_game()
                self.check_collisions()

            if self.stats.paused:
                self.pause_screen()

            if self.stats.lost_ship and not self.stats.game_over:
                mixer.music.stop()
                self.reset_screen()

            if self.stats.game_over:
                mixer.music.stop()
                self._empty_screen()
                self._self_explode()
                if self.stats.score > self.stats.high_score:
                    self.high_score_screen()
                    self.stats.save_high_score()
                self.game_over_screen()
                if self.stats.game_active:
                    self.change_music(self.settings.background_music,
                                      self.settings.background_music_vol)
                    continue
                sys.exit()
                
#======================================================= Main Game Loop End ===

#============================================================= Game Screens ===

    def intro_screen(self):
        """Displays the introductory sequence."""
        self.change_music(self.settings.intro_music,
                          self.settings.background_music_vol+.1, False)
        self.game_intro.display_game_intro(pygame.time.get_ticks())

    def start_screen(self):
        """Displays the start screen to allow the player to start the game."""
        if mixer.music.get_busy():
            mixer.music.unload()

        self.ship.sprite.blitme()
        self.start_button.render_text('Start')
        self.about_button.render_text('About')
        self.start_button.blitme()
        self.about_button.blitme()
        self.stats.start_button_active = True
        self.stats.about_button_active = True
        self.stats.render_stats()
        self._plot_initial_stars()
        pygame.display.flip()

        while self.stats.start_button_active and self.stats.about_button_active:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_mouse_click()

    def _plot_initial_stars(self):
        """Plots and displays the initial stars."""
        i = 0
        while i < 40:
            self.bg_stars.add(BackGroundStar(self))
            i += 1

        for star in self.bg_stars.copy():
            star.x = randint(0, self.screen_rect.right)
            star.y = randint(0, self.screen_rect.bottom)

        self.bg_stars.update()
        self.bg_stars.draw(self.screen)

    def pause_screen(self):
        """
        Displays the paused screen whenever the player pauses the game
        until the player unpauses the game.
        """
        mixer.music.pause()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.stats.paused = False
                        mixer.music.unpause()
                        return

    def reset_screen(self):
        """Resets the screen to allow the player to start again."""
        self._empty_screen()

        if not self.stats.game_over:
            self._self_explode()

        self.stats.lost_ship = False
        self._plot_initial_stars()
        self.ship.add(Ship(self))
        self.ship.sprite.rect.midleft = self.screen_rect.midleft
        self.change_music(self.settings.background_music,
                          self.settings.background_music_vol)
        pygame.event.clear()
        self.stats.game_active = True

    def _empty_screen(self):
        """Removes all sprites from the screen."""
        self.enemies.empty()
        self.asteroids.empty()
        self.bullets.empty()
        self.enemy_bullets.empty()
        self.bg_stars.empty()
        self.explosions.empty()
        self.power_ups.empty()
        pygame.display.flip()

    def _self_explode(self):
        """Creates a separate animation for the player's ship's explosion."""
        init_ticks = pygame.time.get_ticks()
        self.player_explosion.add(ShipExplosion(self, self.ship.sprite, init_ticks))
        self.player_explosion.draw(self.screen)
        self.ship.empty()
        while True:
            self.screen.fill(self.settings.bg_color)
            self.player_explosion.update(pygame.time.get_ticks())
            self.player_explosion.draw(self.screen)
            pygame.display.flip()
            if self.player_explosion.sprite.frame == self.player_explosion.sprite.FRAMES:
                self.player_explosion.empty()
                self.screen.fill(self.settings.bg_color)
                pygame.display.flip()
                pygame.time.wait(2_000)
                return

    def game_over_screen(self):
        """Creates a game over screen when the player runs out of ships."""
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 212)
        font_text = font.render("Game Over!", True, (255, 55, 105))
        font_text_rect = font_text.get_rect()
        font_text_rect.center = self.screen_rect.center
        self.screen.blit(font_text, font_text_rect)
        pygame.display.flip()
        self.change_music(self.settings.game_over_soundtrack,
                          self.settings.background_music_vol)
        pygame.time.wait(1200)
        self._get_choice(font_text_rect)

    def _get_choice(self, game_over_rect):
        """Lets the player choose if they want to continue or not."""
        cont_centerx = game_over_rect.left
        cont_centery = game_over_rect.bottom + 60
        continue_button = Button(self, (10, 240, 24),
                                 cont_centerx, cont_centery)
        continue_button.render_text("Continue")

        end_centerx = game_over_rect.right
        end_centery = game_over_rect.bottom + 60
        end_button = Button(self, (255, 10, 10),
                            end_centerx, end_centery)
        end_button.render_text("Quit")

        continue_button.blitme()
        end_button.blitme()
        pygame.mouse.set_visible = True
        pygame.display.flip()

        while self.stats.game_over:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_mouse_click(continue_button, end_button)

    def high_score_screen(self):
        """
        Displays the screen that informs the player that they have acheived a
        high score and prompts for their initials.
        """
        number = 1
        while True:
            if number == randint(1, 16):
                self.fireworks.add(FireWork(self, pygame.time.get_ticks()))
                
            self.update_fireworks()
            self.fireworks.draw(self.screen)
            self.display_high_score_message()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        sys.exit()
                    elif event.key == pygame.K_UP:
                        self.init_slots.change_character('up')
                    elif event.key == pygame.K_DOWN:
                        self.init_slots.change_character('down')
                    elif event.key == pygame.K_LEFT:
                        self.init_slots.change_character('left')
                    elif event.key == pygame.K_RIGHT:
                        self.init_slots.change_character('right')
                    elif event.key == pygame.K_RETURN:
                        self.init_slots.confirm_initials()

            self.screen.fill(self.settings.bg_color)
            if self.init_slots.initials_confirmed:
                break
            
    def display_high_score_message(self):
        """
        Displays messages informing the player that they have acheived a
        new high score.
        """
        messages = [
            'Congratulations!!!',
            'You have acheived a new high score!',
            str(self.stats.score),
            'Enter your initials below',
        ]

        font = pygame.font.SysFont(None, 98)
        y_space = 75

        for message in messages:
            text_image = font.render(message, True, (255, 255, 255))
            text_image_rect = text_image.get_rect()
            
            text_image_rect.top = self.screen_rect.top + y_space
            text_image_rect.centerx = self.screen_rect.centerx

            self.screen.blit(text_image, (text_image_rect.x, text_image_rect.y))
            y_space += text_image_rect.height + 35

        self.init_slots.display_initials_box(y_space)

    def display_about_screen(self):
        """Displays the about screen to the player."""
        self.stats.start_button_active = False
        self.stats.about_button_active = False
        font = pygame.font.SysFont(None, 34)
        credits = []
        filepath = 'credits/credits.txt'
        try:
            with open(filepath, 'r', encoding='utf-8') as credit_file:
                for line in credit_file:
                    credits.append(line)
        except:
            FileNotFoundError('Credits file could not be found.')
        finally:
            y_pos = 85
            self.screen.fill((0, 0, 0))
            for line in credits:
                print(line)
                line_image = font.render(line, True, (255, 255, 255))
                line_rect = line_image.get_rect(center = (self.screen_rect.centerx, y_pos))
                self.screen.blit(line_image, line_rect)
                y_pos += 35
            self.start_button.rect.x = self.screen_rect.left+25
            self.screen.blit(self.start_button.image, self.start_button.rect)
            pygame.display.flip()
            self.stats.start_button_active = True
            self.stats.about_button_active = True
        
#========================================================= Game Screens End ===
    
#=================================================================== Events ===

    def check_events(self):
        """Respond to keypress, mouse, and custom events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.game_active = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.check_mouse_click()
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._handle_keyup_events(event)
                
    def _handle_keydown_events(self, event):
        """Sets move values to true based on keys pressed."""
        if event.key == pygame.K_q:
            self.stats.game_quit = True
            sys.exit()
        elif event.key == pygame.K_UP:
            self.ship.sprite.move['up'] = True
        elif event.key == pygame.K_DOWN:
            self.ship.sprite.move['down'] = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self.stats.paused = True

    def _handle_keyup_events(self, event):
        """Sets move values to false based on keys not pressed."""
        if event.key == pygame.K_UP:
            self.ship.sprite.move['up'] = False
        elif event.key == pygame.K_DOWN:
            self.ship.sprite.move['down'] = False

    def _handle_reset_ship_buffer(self):
        """Resets the ship's hit buffer value."""
        self.ship.sprite.hit_buffer = False
        self.ship.sprite.hb_number = 1
        self.ship.sprite.update_hit_buffer_image()

    def _handle_reset_enemy_hit(self):
        """Resets the enemy's hit values."""
        for enemy in self.enemies.copy():
            if enemy.hit:
                enemy.hit_number = 2
                enemy.update_individual(self)
                enemy.hit = False

    def check_mouse_click(self, cont_button=None, end_button=None):
        """Checks the location of a mouse click."""
        click_pos = pygame.mouse.get_pos()
        if self.stats.game_over:
            if cont_button.rect.collidepoint(click_pos[0], click_pos[1]):
                self.reset_screen()
                self.stats.ships_left = 3
                self.stats.score = 0
                self.stats.level = 1
                self.stats.game_over = False
                self.stats.lost_ship = False
                self.stats.game_active = True
                pygame.mouse.set_visible = False
            elif end_button.rect.collidepoint(click_pos[0], click_pos[1]):
                sys.exit()

        if self.stats.start_button_active and self.stats.about_button_active:
            if self.start_button.rect.collidepoint(click_pos[0], click_pos[1]):
                self.stats.game_active = True
                self.stats.start_button_active = False
                self.stats.about_button_active = False
                self.change_music(self.settings.background_music,
                                  self.settings.background_music_vol)
                pygame.mouse.set_visible = False
            elif self.about_button.rect.collidepoint(click_pos[0], click_pos[1]):
                self.display_about_screen()
                
#=============================================================== Events End ===

#======================================= Create/Update Sprites/Sounds/Music ===

    def make_sprites(self):
        """Creates the sprites of the game at random times."""
        self.make_asteroids()
        self.make_enemies()
        self.make_bg_stars()
        self.make_power_ups()

    def _fire_bullet(self):
        """Creates a bullet and adds it to the bullet group."""
        self.bullets.add(Bullet(self))
        if not self.ship.sprite.powered_up:
            bullet_sound = mixer.Sound(self.settings.fire_bullet_sound)
        else:
            bullet_sound = mixer.Sound(self.settings.fire_super_bullet_sound)

        bullet_sound.set_volume(self.settings.fire_bullet_sound_vol)
        bullet_sound.play()

    def update_game(self):
        """Calls update methods to update game attributes."""
        self.ship.sprite.update()
        self.update_bullets()
        self.update_asteroids()
        self.update_enemies()
        self.update_explosions()
        self.update_bg_stars()
        self.update_power_ups()
        self.stats.render_stats()
        self.update_screen()
                
    def change_music(self, next_soundtrack, volume, loop=True):
        """
        Unloads the currently playing music(if any)
        and loads the next music to play.
        """
        if mixer.music.get_busy():
            mixer.music.unload()

        try:
            mixer.music.load(next_soundtrack)
        except:
            FileNotFoundError('The audio file was not found.')
        finally:
            mixer.music.set_volume(volume)
            if loop:
                mixer.music.play(-1)
            else:
                mixer.music.play()

    def play_sound_effect(self, sound_effect, volume):
        """
        Plays the sound effect file provided in the first argument, sets the
        volume to the specified value in the second argument.
        """
        try:
            sound = mixer.Sound(sound_effect)
        except:
            FileNotFoundError('The audio file was not found.')
        finally:
            sound.set_volume(volume)
            sound.play()

    def update_bullets(self):
        """Updates the position of bullets and gets rid of old ones."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.left > self.screen_rect.right:
                self.bullets.remove(bullet)

        self.enemy_bullets.update()
        for enemy_bullet in self.enemy_bullets.copy():
            if enemy_bullet.rect.right < self.screen_rect.left:
                self.enemy_bullets.remove(enemy_bullet)

    def make_asteroids(self):
        """
        Creates asteroids on the right end of the screen and directs them
        toward the player's side of the screen.
        """
        number = randint(1, 76)
        if len(self.asteroids) < self.settings.asteroids_allowed and number == 1:
            self.asteroids.add(Asteroid(self))

    def update_asteroids(self):
        """Updates the location of the asteroids and gets rid of old ones."""
        self.asteroids.update()
        for asteroid in self.asteroids.copy():
            if not asteroid.hit:
                asteroid.update_individual()
            else:
                asteroid.update_individual(pygame.time.get_ticks())

            if asteroid.rect.right < self.screen_rect.left:
                self.asteroids.remove(asteroid)

    def make_enemies(self):
        """Creates enemies on the screen."""
        number = randint(1, 121)
        if len(self.enemies) < self.settings.enemies_allowed:
            if number == 1:
                self.enemies.add(RedYellowEnemy(self))
            elif number == 2:
                self.enemies.add(PurpleGrayEnemy(self))

    def update_enemies(self):
        """Updates the location of the enemies and gets rid of old ones."""
        self.enemies.update()
        for enemy in self.enemies.copy():
            if not enemy.hit:
                enemy.update_individual(self)
            else:
                enemy.update_individual(self, pygame.time.get_ticks())

            if enemy.rect.right < self.screen_rect.left:
                self.enemies.remove(enemy)

    def update_explosions(self):
        """Updates the image of the explosions and gets rid of old ones."""
        self.explosions.update(pygame.time.get_ticks())
        for explosion in self.explosions.copy():
            if explosion.frame == explosion.FRAMES:
                self.explosions.remove(explosion)

    def make_bg_stars(self):
        """Creates stars for the background."""
        number = randint(1, 4)
        if (len(self.bg_stars) < self.settings.bg_stars_allowed
             and number == 1):
            self.bg_stars.add(BackGroundStar(self))

    def update_bg_stars(self):
        """
        Updates the location of all the stars in the group and gets
        rid of old ones.
        """
        self.bg_stars.update()
        for star in self.bg_stars.copy():
            if star.rect.right < self.screen_rect.left:
                self.bg_stars.remove(star)

    def make_power_ups(self):
        """Sometimes creates a power-up for the player to grab."""
        number = randint(1, 1_501)
        if number == 1 and len(self.power_ups) < self.settings.power_ups_allowed:
            if not self.ship.sprite.powered_up:
                self.power_ups.add(PowerUp(self))

    def update_power_ups(self):
        """Updates the location of all power ups and gets rid of old ones."""
        self.power_ups.update()
        for power_up in self.power_ups.copy():
            if power_up.rect.right < self.screen_rect.left:
                self.power_ups.remove(power_up)

    def update_fireworks(self):
        """Updates the image of the fireworks and gets rid of old ones."""
        self.fireworks.update(pygame.time.get_ticks())
        for firework in self.fireworks.copy():
            if firework.frame == firework.FRAMES:
                self.fireworks.remove(firework)

#================================================ Create/Update Sprites End ===

#=============================================================== Collisions ===

    def check_collisions(self):
        """Check if there are any collisions between any sprites on screen."""
        if not self.ship.sprite.hit_buffer:
            self._ship_collisions()

        self._bullet_collisions()
    
    def _ship_collisions(self):
        """Check if player's ship collides with other sprites (excluding stars)."""
        if not self.ship.sprite.powered_up:

            # Collision with enemy bullets.
            ship_bullet_collisions = pygame.sprite.spritecollide(
               self.ship.sprite, self.enemy_bullets,True)
            if ship_bullet_collisions:
                self._ship_hit()
                
            # Collision with asteroids.
            ship_asteroid_collisions = pygame.sprite.spritecollide(
              self.ship.sprite, self.asteroids, False, pygame.sprite.collide_circle_ratio(
              self.settings.sp_coll_ratio))
            if ship_asteroid_collisions:
                self._ship_hit()

            # Collision with enemy ships.
            ship_enemy_ship_collisions = pygame.sprite.spritecollide(
              self.ship.sprite, self.enemies, False, pygame.sprite.collide_circle_ratio(
              self.settings.sp_coll_ratio))
            if ship_enemy_ship_collisions:
                self._ship_hit()

            # Collision with power-up icon.
            ship_power_up_contact = pygame.sprite.spritecollide(
              self.ship.sprite, self.power_ups, True)
            if ship_power_up_contact:
                self._ship_gain_power_up()
        
    def _ship_hit(self):
        """Handles logic for when the player's ship is hit."""
        self.ship.sprite.hit_buffer = True
        self.ship.sprite.hit_init_ticks = pygame.time.get_ticks()
        self.ship.sprite.hits -= 1
        if self.ship.sprite.hits == 0:
            self._lose_ship()

    def _ship_gain_power_up(self):
        """Grants the player a temporary power-up."""
        self.power_ups.empty()
        self.play_sound_effect(self.settings.power_up_sound,
                               self.settings.power_up_sound_vol)
        self.ship.sprite.powered_up = True
        self.ship.sprite.update_power_up()

    def _bullet_collisions(self):
        """Check collisions with bullets."""
        for bullet in self.bullets.copy():

            # Bullet collisions with enemies.
            bullet_enemy_collision = pygame.sprite.spritecollide(
                                    bullet, self.enemies, False)
            if bullet_enemy_collision:
                self._handle_collision(bullet, bullet_enemy_collision,
                                       self.enemies, 'enemy') 

            # Bullet collisions with asteroids.
            bullet_asteroid_collision = pygame.sprite.spritecollide(
              bullet, self.asteroids, False, pygame.sprite.collide_circle_ratio(
              self.settings.sp_coll_ratio))
            if bullet_asteroid_collision:
                self._handle_collision(bullet, bullet_asteroid_collision,
                                       self.asteroids, 'asteroid') 

    def _handle_collision(self, bullet, coll_dict, sprite_group, sprite_str):
        """Handles the collision logic between the players' bullet and any sprite/group."""
        self.bullets.remove(bullet)
        for sprite in coll_dict:

            if bullet.IS_SUPER:
                sprite.hits = 0

            sprite.hits -= 1
            if sprite.hits <= 0:
                ticks = pygame.time.get_ticks()
                if sprite_str == 'enemy':
                    self.explosions.add(ShipExplosion(self, sprite, ticks))
                    self.stats.score += self.settings.ry_enemy_points
                    self.play_sound_effect(self.settings.ship_explosion_sound,
                                           self.settings.ship_explosion_vol)
                elif sprite_str == 'asteroid':
                    self.explosions.add(AsteroidExplosion(self, sprite, ticks))
                    self.stats.score += self.settings.asteroid_points
                    self.play_sound_effect(self.settings.asteroid_explosion_sound,
                                           self.settings.asteroid_explosion_vol)
                sprite_group.remove(sprite)

            sprite.hit = True
            sprite.init_hit_ticks = pygame.time.get_ticks()
            
#=========================================================== Collisions End ===

    def _lose_ship(self):
        """Handles statistics for when a ship is lost."""
        self.stats.ships_left -= 1
        self.stats.game_active = False
        self.stats.lost_ship = True
        self.play_sound_effect(self.settings.ship_explosion_sound,
                               self.settings.ship_explosion_vol)
        if self.stats.ships_left == 0:
            self.stats.game_over = True
            
    def update_screen(self):
        """Draws the new location and state of each sprite/game element."""
        self.screen.fill(self.settings.bg_color)
        self.stats.blit_stats()
        self.bg_stars.draw(self.screen)
        self.power_ups.draw(self.screen)
        self.bullets.draw(self.screen)
        self.ship.sprite.blitme()
        self.enemy_bullets.draw(self.screen)
        self.enemies.draw(self.screen)
        self.power_ups.draw(self.screen)
        self.asteroids.draw(self.screen)
        self.explosions.draw(self.screen)
        pygame.display.flip()

if __name__ == '__main__':
    astroshooter = AstroShooter()
    astroshooter.run_game()