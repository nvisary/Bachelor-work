import sound_utils.SoundRecognizer as sr
import text_utils.book as book

DIVIDER = '\n'
MIN_BLOCK_SIZE = 15
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
        recognized_text = sound_recognizer.recognize()
        block_counts = sound_recognizer.get_block_counts()

        # open book and get book text
        book_worker = book.BookWorker(self.book_path)
        book_text = book_worker.get_book_text()

        # save recognize text to file
        recognized_file = open(RECOGNIZED_FILE_PATH, "w")
        recognized_file.write(recognized_text)
        recognized_file.close()

        # save book text to file
        book_file = open(BOOK_FILE_PATH, "w")
        book_file.write(book_text)

        # write data to preprocessor file
        preprocessor_file = open(self.preprocessor_path, "w")

        preprocessor_file.write(str(MIN_BLOCK_SIZE) + DIVIDER)  # min block size of recognize audio (seconds)

        for block_count in block_counts:
            preprocessor_file.write(str(block_count) + DIVIDER)

        preprocessor_file.close()
        book_file.close()
        recognized_file.close()
