import sound_utils.SoundRecognizer as sr
import text_utils.book as book
from text_utils.TextCipher import TextCipher

DIVIDER = '\n'
MIN_BLOCK_SIZE = 20
RECOGNIZED_FILE_PATH = "recognized.txt"
BOOK_FILE_PATH = "book.txt"


class Preprocessor:
    def __init__(self, path_to_mp3, path_to_book, preprocessor_path):
        self.mp3_path = path_to_mp3
        self.book_path = path_to_book
        self.preprocessor_path = preprocessor_path

    def preprocess(self):
        # recognize mp3 file and get text
        sound_recognizer = sr.SoundRecognizer(self.mp3_path, MIN_BLOCK_SIZE)

        recognized_text = sound_recognizer.recognize(show_steps=True, book_path=self.book_path)
        block_counts = sound_recognizer.get_block_counts()

        # open book and get book text
        book_worker = book.BookWorker(self.book_path)
        book_text = book_worker.get_book_text_from_tree()

        # save recognize text to file
        recognized_file = open(RECOGNIZED_FILE_PATH, "w")
        recognized_file.write(recognized_text)

        # save book text to file
        book_file = open(BOOK_FILE_PATH, "w")
        book_file.write(book_text)

        # write data to preprocessor file
        preprocessor_file = open(self.preprocessor_path, "wb")
        db_data = str(MIN_BLOCK_SIZE) + DIVIDER  # min block size of recognize audio (seconds)

        for block_count in block_counts:
            db_data += str(block_count) + DIVIDER

        text_cipher = TextCipher("Hello world")
        encrypted_data = text_cipher.encrypt(db_data)
        preprocessor_file.write(encrypted_data)
        preprocessor_file.close()
        book_file.close()
        recognized_file.close()

    def find_padding(self, book_text, recognized_text):
        pass