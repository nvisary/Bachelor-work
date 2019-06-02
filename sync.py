import pygame
import time
from pydub import AudioSegment
from text_utils.TextCipher import TextCipher
import os
import text_utils.book

CUTTED_MP3_PATH = os.path.dirname(__file__) + "/res/cutted.mp3"
PLAY_MUSIC = True
PYGAME_PLAYER = False
PLAY_MUSIC_TIME = 10  # play first seconds
ENCRYPTION_KEY = "Hello world"
ENCRYPTION = False


class Sync:
    def __init__(self, preprocessor_path, mp3_path, book_path):
        self.preprocessor_path = preprocessor_path
        self.mp3_path = mp3_path
        self.book_path = book_path

        # load audio, open book, open preprocessor file
        # self.mp3_audio = AudioSegment.from_mp3(self.mp3_path)
        self.book = text_utils.book.BookWorker(self.book_path)
        if ENCRYPTION:
            self.preprocessor_file = open(self.preprocessor_path, "rb")
        else:
            self.preprocessor_file = open(self.preprocessor_path, "r")
        # get book text (for fb2 return text between body tag)
        self.book_text = self.book.get_book_text_from_tree()

        # parse preprocessor file
        self.db_data = self.preprocessor_file.read()

        if ENCRYPTION:
            # data decrypt
            text_cipher = TextCipher(ENCRYPTION_KEY)
            decoded_data = text_cipher.decrypt(self.db_data)
            self.db_data = decoded_data
        self.db_data = self.db_data.split("\n")
        self.preprocessor_parameters = []
        for line in self.db_data:
            if line == '':
                break
            self.preprocessor_parameters.append(int(line.strip()))
        # get min block size from preprocessor
        self.block_size = self.preprocessor_parameters[0]
        self.padding_size = self.preprocessor_parameters[1]

        # count blocks * (block_size + padding) = how long audio
        self.count_seconds = (len(self.preprocessor_parameters) - 2) * (self.block_size + self.padding_size)

    def sync_from_audio(self, second, play=True):

        # cut audio by sec and save it
        if play:
            mp3_audio = self.mp3_audio[second * 1000:]
            mp3_audio.export(CUTTED_MP3_PATH, format="mp3")

        # use pygame to play cutted audio
        if PLAY_MUSIC and play:
            pygame.init()

            DISPLAYSURF = pygame.display.set_mode((400, 300))
            pygame.display.set_caption(CUTTED_MP3_PATH)

            pygame.mixer.music.load(CUTTED_MP3_PATH)
            pygame.mixer.music.play()
            time.sleep(PLAY_MUSIC_TIME)
            pygame.mixer.music.stop()

        if second < self.count_seconds:
            print("Your sec:{}".format(second))
            block_number = second / (self.block_size + self.padding_size)
            print("I think this is block [{}] {}".format(block_number, self.preprocessor_parameters[int(block_number) + 2]))
            word_number = self.preprocessor_parameters[int(block_number) + 2]
            if block_number - int(block_number) > 0:
                print("Block num is not int")
                next_count = self.preprocessor_parameters[int(block_number) + 3]
                current_count = self.preprocessor_parameters[int(block_number) + 2]
                print("Current block: ", current_count)
                print("Next block: ", next_count)
                word_number += (next_count - current_count) * (block_number - int(block_number))
                print("I think it is word: ", word_number)

            book_text = self.book_text.split()
            book_text = book_text[int(word_number):int(word_number) + 10]
            print(book_text)

            if play:
                print(" ".join(book_text))
            else:
                return int(word_number)

    def sync_from_text(self, search_word, play=True):

        # get min block size from preprocessor
        seconds_block_size = self.block_size
        padding = self.padding_size
        result = 0
        second = 0
        for i in range(3, len(self.preprocessor_parameters)):
            second += padding + seconds_block_size
            current_word = self.preprocessor_parameters[i]
            if current_word >= search_word:
                result = int(second * search_word / current_word)


        # cut audio by sec and save it
        if play:
            mp3_audio = AudioSegment.from_mp3(self.mp3_path)
            mp3_audio = mp3_audio[result * 1000:]
            mp3_audio.export(os.path.dirname(__file__) + "/res/cutted.wav", format="wav")

            import sys
            sys.argv = [sys.argv[0]]
            from gui.audio_player import AudioPlayer

            player = AudioPlayer()
            player.run()
        else:
            return result
        # pygame.init()

        # DISPLAYSURF = pygame.display.set_mode((400, 300))
        # pygame.display.set_caption(CUTTED_MP3_PATH)

        # pygame.mixer.music.load(CUTTED_MP3_PATH)
        # pygame.mixer.music.play()
        # time.sleep(PLAY_MUSIC_TIME)
        # pygame.mixer.music.stop()
