from pygame import mixer

class Sounds():
	"""Class to manage the game's music and sound effects."""

	def change_music(self, next_soundtrack, volume, loop=True):
		"""
		Unloads the currently playing music(if any)
		and loads the next music to play.
		volume parameter controls the volume of the music.
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

	def unload_music(self):
		"""Unloads the music if there is any playing currently."""
		if mixer.music.get_busy():
			mixer.music.unload()

	def set_paused_music(self, paused_bool):
		"""
		Pauses the currently playing music if paused_bool is true,
		else unpauses the music.
		"""
		if paused_bool:
			mixer.music.pause()
		else:
			mixer.music.unpause()

	def stop_music(self):
		"""Stops the music currently playing, if any."""
		if mixer.music.get_busy():
			mixer.music.stop()