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


class Sync:
    def __init__(self, preprocessor_path, mp3_path, book_path):
        self.preprocessor_path = preprocessor_path
        self.mp3_path = mp3_path
        self.book_path = book_path

        # load audio, open book, open preprocessor file
        self.mp3_audio = AudioSegment.from_mp3(self.mp3_path)
        self.book = text_utils.book.BookWorker(self.book_path)
        self.preprocessor_file = open(self.preprocessor_path, "rb")

        # get book text (for fb2 return text between body tag)
        self.book_text = self.book.get_book_text_from_tree()

        # parse preprocessor file
        self.db_data = self.preprocessor_file.read()

        # data decrypt
        text_cipher = TextCipher("Hello world")
        decoded_data = text_cipher.decrypt(self.db_data)
        decoded_data = decoded_data.split("\n")
        self.preprocessor_parameters = []
        for line in decoded_data:
            if line == '':
                break
            self.preprocessor_parameters.append(int(line.strip()))

        # get min block size from preprocessor
        self.block_size = self.preprocessor_parameters[0]

        # count blocks * block_size = how long audio
        self.count_seconds = (len(self.preprocessor_parameters) - 1) * self.block_size

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
            count_blocks = second / self.block_size

            # count words in blocks (how many words in count_blocks)
            count_words = 0
            for i in range(int(round(count_blocks))):
                count_words += self.preprocessor_parameters[i + 1]

            if count_blocks - int(count_blocks) > 0:
                print(self.preprocessor_parameters[int(count_blocks) + 2] * (count_blocks - int(count_blocks)))
                count_words += int(self.preprocessor_parameters[int(count_blocks) + 2] * (count_blocks - int(count_blocks)))

            # print text from count_words
            book_text = self.book_text.split()
            book_text = book_text[count_words:]


            if play:
                print(" ".join(book_text))
            else:
                return count_words

    def sync_from_text(self, word_number, play=True):
        # parse preprocessor file
        preprocessor_file = open(self.preprocessor_path, "rb")
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
        seconds_block_size = preprocessor_parameters[0]
        current_sec = 0
        current_count_words = 0
        last_count_words = 0
        result_second = 0
        for i in range(1, len(preprocessor_parameters)):
            current_sec += seconds_block_size
            current_count_words += preprocessor_parameters[i]
            if current_count_words > word_number:
                speech_speed = (current_count_words - last_count_words) / seconds_block_size
                words_to_limit = word_number - last_count_words
                result_second = words_to_limit / speech_speed + current_sec - seconds_block_size

                break

            last_count_words = current_count_words
            print("sec:{} count:{} limit:{}".format(current_sec, current_count_words, word_number))

        # cut audio by sec and save it
        if play:
            mp3_audio = AudioSegment.from_mp3(self.mp3_path)
            mp3_audio = mp3_audio[result_second * 1000:]
            mp3_audio.export(os.path.dirname(__file__) + "/res/cutted.wav", format="wav")

            import sys
            sys.argv = [sys.argv[0]]
            from gui.audio_player import AudioPlayer

            player = AudioPlayer()
            player.run()
        else:
            return result_second
        # pygame.init()

        # DISPLAYSURF = pygame.display.set_mode((400, 300))
        # pygame.display.set_caption(CUTTED_MP3_PATH)

        # pygame.mixer.music.load(CUTTED_MP3_PATH)
        # pygame.mixer.music.play()
        # time.sleep(PLAY_MUSIC_TIME)
        # pygame.mixer.music.stop()




