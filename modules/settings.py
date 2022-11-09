class Settings:
    """Class to store the settings for the game."""

    def __init__(self):
        """Initilaizes the game's static settings."""

        # Screen settings.
        self.bg_color = (0, 0, 40)
        self.color_key = (255, 255, 255)
        self.bg_star_speed = 10.1
        self.bg_stars_allowed = 80

        # Intro settings.
        self.header_speed = 1.5
        self.story_text_speed = 0.6
        
        # Ship settings.
        self.ship_speed = 12.7

        # Bullet settings.
        self.bullet_speed = 15.5

        # Astroid settings.
        self.asteroids_allowed = 6
        self.asteroid_speed = 5.2
        self.asteroid_points = 250

        # Enemy(all) settings.
        self.enemies_allowed = 24

        # Enemy(red/yellow) settings.
        self.ry_enemy_speed = 5.5
        self.ry_enemy_points = 600

        # Enemy(purple/gray) settings.
        self.pg_enemy_speed = 4.8
        self.pg_enemy_points = 400

        # Power-up settings.
        self.power_ups_allowed = 1
        self.power_up_speed = 3.0

        # Boss settings.
        self.boss_speed = 2.4
        self.boss_points = 750_000

        # Sprite collide ratios.
        self.sp_coll_ratio = 0.77

        # SoundTrack/Sound Effects settings.
        self.background_music_vol = 0.1
        self.fire_bullet_sound_vol = 0.15
        self.power_up_sound_vol = 0.09
        self.ship_explosion_vol = 0.19
        self.asteroid_explosion_vol = 0.34
        self.path = 'audio/'
        self.intro_music = self.path + 'intro_soundtrack.wav'
        self.background_music = self.path + 'background_soundtrack.wav'
        self.fire_bullet_sound = self.path + 'laser9.mp3'
        self.fire_super_bullet_sound = self.path + 'laser1.mp3'
        self.asteroid_explosion_sound = (self.path + 
                                         'asteroid_explosion_sound_effect.wav')
        self.ship_explosion_sound = (self.path + 
                                     'ship_explosion_sound_effect.wav')
        self.game_over_soundtrack = self.path + 'game_over_soundtrack.wav'
        self.power_up_sound = self.path + 'power_up_sound_effect.wav'

        # Text Characters List.
        self.characters = [
            ' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
            'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
            'Z',
        ]