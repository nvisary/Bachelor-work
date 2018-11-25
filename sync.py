import pygame
import time
from pydub import AudioSegment


import text_utils.book

CUTTED_MP3_PATH = "res/cutted.mp3"
PLAY_MUSIC = True


class Sync:
    def __init__(self, preprocessor_path, mp3_path, book_path):
        self.preprocessor_path = preprocessor_path
        self.mp3_path = mp3_path
        self.book_path = book_path

    def sync_from(self, second):
        mp3_audio = AudioSegment.from_mp3(self.mp3_path)
        book = text_utils.book.BookWorker(self.book_path)
        preprocessor_file = open(self.preprocessor_path, "r")

        book_text = book.get_book_text()

        mp3_audio = mp3_audio[second * 1000:]
        mp3_audio.export(CUTTED_MP3_PATH, format="mp3")

        if PLAY_MUSIC:
            pygame.init()

            DISPLAYSURF = pygame.display.set_mode((400, 300))
            pygame.display.set_caption(CUTTED_MP3_PATH)

            pygame.mixer.music.load(CUTTED_MP3_PATH)
            pygame.mixer.music.play()
            time.sleep(10)
            pygame.mixer.music.stop()

        preprocessor_parameters = []
        for line in preprocessor_file:
            preprocessor_parameters.append(int(line))

        block_size = preprocessor_parameters[0]
        count_seconds = (len(preprocessor_parameters) - 1) * block_size
        if second < count_seconds:
            count_blocks = second / block_size
            print(count_blocks)
            count_words = 0
            for i in range(int(round(count_blocks))):
                count_words += preprocessor_parameters[i + 1]
            book_text = book_text.split()
            book_text = book_text[count_words:]
            print(" ".join(book_text))
