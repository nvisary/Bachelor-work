import pygame
import time
from pydub import AudioSegment
from text_utils.TextCipher import TextCipher

import text_utils.book

CUTTED_MP3_PATH = "res/cutted.mp3"
PLAY_MUSIC = True

PLAY_MUSIC_TIME = 10  # play first seconds


class Sync:
    def __init__(self, preprocessor_path, mp3_path, book_path):
        self.preprocessor_path = preprocessor_path
        self.mp3_path = mp3_path
        self.book_path = book_path

    def sync_from(self, second):
        # load audio, open book, open preprocessor file
        mp3_audio = AudioSegment.from_mp3(self.mp3_path)
        book = text_utils.book.BookWorker(self.book_path)
        preprocessor_file = open(self.preprocessor_path, "rb")

        # get book text (for fb2 return text between body tag)
        book_text = book.get_book_text_from_tree()

        # cut audio by sec and save it
        mp3_audio = mp3_audio[second * 1000:]
        mp3_audio.export(CUTTED_MP3_PATH, format="mp3")

        # use pygame to play cutted audio
        if PLAY_MUSIC:
            pygame.init()

            DISPLAYSURF = pygame.display.set_mode((400, 300))
            pygame.display.set_caption(CUTTED_MP3_PATH)

            pygame.mixer.music.load(CUTTED_MP3_PATH)
            pygame.mixer.music.play()
            time.sleep(PLAY_MUSIC_TIME)
            pygame.mixer.music.stop()

        # parse preprocessor file
        db_data = preprocessor_file.read()

        # data decrypt
        text_cipher = TextCipher("Hello world")
        decoded_data = text_cipher.decrypt(db_data)
        decoded_data = decoded_data.split("\n")
        preprocessor_parameters = []
        for line in decoded_data:
            if line == '':
                break
            preprocessor_parameters.append(int(line.strip()))

        # get min block size from preprocessor
        block_size = preprocessor_parameters[0]

        # count blocks * block_size = how long audio
        count_seconds = (len(preprocessor_parameters) - 1) * block_size
        if second < count_seconds:
            count_blocks = second / block_size

            # count words in blocks (how many words in count_blocks)
            count_words = 0
            for i in range(int(round(count_blocks))):
                count_words += preprocessor_parameters[i + 1]

            # print text from count_words
            book_text = book_text.split()
            book_text = book_text[count_words:]
            print(" ".join(book_text))
