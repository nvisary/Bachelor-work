from pydub import AudioSegment
import speech_recognition as sr
import os
import datetime
import text_utils.book as book
import text_utils.text_analyzer as analyzer

COUNT_WORDS_SEARCH = 3


class SoundRecognizer:
    """Class recognize speech from audio mp3"""

    def __init__(self, path_to_mp3, min_block_size, padding, book_path, count_words_search=COUNT_WORDS_SEARCH):
        """"""
        self.block_counts = []
        self.AUDIO_IN = path_to_mp3
        self.WAV_FOLDER = "tmp/"
        self.audio_mp3 = AudioSegment.from_mp3(self.AUDIO_IN)
        self.MIN_BLOCK_SIZE = min_block_size  # seconds
        self.speech_speed = 124  # words in minute
        self.padding = padding
        self.book_path = book_path
        self.count_words_search = count_words_search

        self.search_success = 0
        self.search_fail = 0
        self.searches = 0

    def recognize_on_time(self, time1, time2):
        cutted_audio = self.cut_file(time1, time2)
        self._save_audio_to_wav(cutted_audio)
        r = sr.Recognizer()
        with sr.AudioFile(self.wav_file_name) as source:
            audio = r.record(source)
            recognized_text = r.recognize_google(audio, language="ru_RU")

        return recognized_text

    def recognize(self, show_steps=False):
        audio_length = self.get_audio_length()
        recognized_text = ""
        count_blocks = int(audio_length / (self.MIN_BLOCK_SIZE + self.padding))
        # self.speech_speed = self.compute_speech_speed()
        book_worker = book.BookWorker(self.book_path)
        book_text = book_worker.get_book_text_from_tree()
        book_text = book_text.split()
        print(book_text)
        last = 0
        founds = 0
        not_founds = 0
        count = 0
        if show_steps:
            print("Recognition file: " + self.AUDIO_IN)
        for i in range(count_blocks):
            time1 = i * (self.MIN_BLOCK_SIZE + self.padding)
            time2 = time1 + self.MIN_BLOCK_SIZE
            print("{}:{}".format(time1, time2))

            recognized_block = self.recognize_on_time(time1, time2)
            recognized_block_array = recognized_block.split()
            if show_steps:
                print("Block: " + str(i + 1) + "/" + str(count_blocks))

            speech_speed_in_second = self.speech_speed / 60
            left_search_border = int(speech_speed_in_second * time1 - 200)
            right_search_border = int(speech_speed_in_second * time2 + 200)
            if left_search_border < 0:
                left_search_border = 0

            i = left_search_border
            found = False
            count_words = 0
            j = 0

            while j + 3 < len(recognized_block_array):
                while i < right_search_border:
                    lev = analyzer.get_levenshtein(recognized_block_array[j:j + self.count_words_search],
                                                   book_text[i: i + self.count_words_search])
                    if lev > 0.6:
                        print(recognized_block_array[j:j + self.count_words_search])
                        print(book_text[i: i + self.count_words_search])
                        count_words = i

                        found = True
                        break
                    i += 1
                if found:
                    break
                j += 1
            count += 1
            if found:
                founds += 1
                print("Found")
                self.search_success += 1
            else:
                not_founds += 1
                print("Not found")
                self.search_fail += 1
                count_words = int(speech_speed_in_second * time1)
            self.searches += 1
            last += count_words
            print("count:", last)
            self.block_counts.append(count_words)
            recognized_text += " " + recognized_block
        print("Founds: ", founds)
        print("Not founds: ", not_founds)
        print("Words: ", count)
        print(self.block_counts)
        return recognized_text

    def compute_speech_speed(self):
        print("Speech speed computing")
        audio_length = self.get_audio_length()
        first = self.recognize_on_time(10, 70)
        second = self.recognize_on_time(int(audio_length / 2), int(audio_length / 2) + 60)
        speech_speed = int((len(first.split()) + len(second.split())) / 2)
        return speech_speed

    def get_data(self):
        return {"searches" : self.searches, "success": self.search_success, "fail": self.search_fail}

    def cut_file(self, time1, time2):
        return self.audio_mp3[time1 * 1000: time2 * 1000]

    def _save_audio_to_wav(self, audio_to_save):
        if not os.path.exists(self.WAV_FOLDER):
            os.mkdir(self.WAV_FOLDER)
        self.wav_file_name = self.WAV_FOLDER + "/" + "tmp.wav"
        audio_to_save.export(self.wav_file_name, format="wav")

    def get_audio_length(self):
        return len(self.audio_mp3) / 1000

    def get_block_counts(self):
        return self.block_counts

    def recognize_with_sphinx(self):
        audio = self.cut_file(0, 60)
        self._save_audio_to_wav(audio)
        r = sr.Recognizer()
        with sr.AudioFile(self.wav_file_name) as source:
            audio = r.record(source)
            print("rec...")
            time1 = datetime.datetime.now()
            recognized_text = r.recognize_sphinx(audio)
            time2 = datetime.datetime.now()
            print("Time: " + str(time2 - time1))
        return recognized_text
