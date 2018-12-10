import pygame
from pydub import AudioSegment
import time

CUTTED_MP3_PATH = "res/cutted.mp3"


class Player:
    def __init__(self, path_to_mp3):
        self.mp3_path = path_to_mp3

    def play_from(self, second, duration):
        mp3_audio = AudioSegment.from_mp3(self.mp3_path)

        # cut audio by sec and save it
        mp3_audio = mp3_audio[second * 1000:]
        mp3_audio.export(CUTTED_MP3_PATH, format="mp3")

        pygame.init()
        DISPLAYSURF = pygame.display.set_mode((400, 300))
        pygame.display.set_caption(CUTTED_MP3_PATH)

        pygame.mixer.music.load(CUTTED_MP3_PATH)
        pygame.mixer.music.play()
        time.sleep(duration)
        pygame.mixer.music.stop()
