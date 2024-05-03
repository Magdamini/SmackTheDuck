import pygame

BASE_SOUND_PATH = 'data/sounds/'


class SoundManager:
    _instance = None


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            pygame.mixer.init()
            cls._instance.sounds = {
                "stat_chosen": pygame.mixer.Sound(BASE_SOUND_PATH + "stat_chosen.wav"),}
            cls._instance.music = {
                "game": BASE_SOUND_PATH + "game.mp3",
                "battle": BASE_SOUND_PATH + "battle.mp3",}
        return cls._instance


    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    

    def play_music(self, music_name):
        if music_name in self.music:
            pygame.mixer.music.load(self.music[music_name])
            pygame.mixer.music.play(-1)
    

    def stop_music(self):
        pygame.mixer.music.fadeout(500)
        pygame.mixer.music.unload()
