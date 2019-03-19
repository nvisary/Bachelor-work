from pydub import AudioSegment
import speech_recognition as sr
import os
import datetime
import text_utils.book as book
import text_utils.text_analyzer as analyzer


class SoundRecognizer:
    """Class recognize speech from audio mp3"""

    def __init__(self, path_to_mp3, min_block_size):
        """"""
        self.block_counts = []
        self.AUDIO_IN = path_to_mp3
        self.WAV_FOLDER = "tmp/"
        self.audio_mp3 = AudioSegment.from_mp3(self.AUDIO_IN)
        self.MIN_BLOCK_SIZE = min_block_size  # seconds

    def recognize_on_time(self, time1, time2):
        cutted_audio = self.cut_file(time1, time2)
        self._save_audio_to_wav(cutted_audio)
        r = sr.Recognizer()
        with sr.AudioFile(self.wav_file_name) as source:
            audio = r.record(source)
            recognized_text = r.recognize_google(audio, language="ru_RU")

        return recognized_text

    def recognize(self, show_steps=False, book_path="res/harry.fb2"):
        audio_length = self.get_audio_length()
        recognized_text = ""
        count_blocks = int(audio_length / self.MIN_BLOCK_SIZE)
        book_worker = book.BookWorker(book_path)
        book_text = book_worker.get_book_text()
        book_text = book_text.split()

        last = 0
        last_block = ""
        if show_steps:
            print("Recognition file " + self.AUDIO_IN)
        for i in range(count_blocks):
            time1 = i * self.MIN_BLOCK_SIZE
            time2 = time1 + self.MIN_BLOCK_SIZE
            recognized_block = self.recognize_on_time(time1, time2)
            if show_steps:
                print("Block: " + str(i + 1) + "/" + str(count_blocks))
            count_words = len(recognized_block.split())
            book_block = book_text[last: last + count_words]
            print(book_block)
            print(recognized_block.split())
            print("Compare: " + str(analyzer.text_compare(recognized_block.split(), book_block)))
            last += count_words

            self.block_counts.append(count_words)
            recognized_text += " " + recognized_block

        return recognized_text

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
