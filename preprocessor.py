import sound_utils.SoundRecognizer as sr
import text_utils.book as book
from text_utils.TextCipher import TextCipher
import text_utils.text_analyzer as text_analyzer

DIVIDER = '\n'
MIN_BLOCK_SIZE = 20
RECOGNIZED_FILE_PATH = "recognized.txt"
BOOK_FILE_PATH = "book.txt"
ENCRYPTION = False
ENCRYPTION_KEY = "Hello world"
BLOCK_PADDING_SIZE = 20


class Preprocessor:
    def __init__(self, path_to_mp3, path_to_book, preprocessor_path, debug=False, recognized_path=RECOGNIZED_FILE_PATH,
                 book_txt_path=BOOK_FILE_PATH):
        self.mp3_path = path_to_mp3
        self.book_path = path_to_book
        self.preprocessor_path = preprocessor_path
        self.debug = debug
        self.recognized_path = recognized_path
        self.book_txt_path = book_txt_path

    def preprocess(self):
        # recognize mp3 file and get text
        sound_recognizer = sr.SoundRecognizer(self.mp3_path, MIN_BLOCK_SIZE, padding=BLOCK_PADDING_SIZE,
                                              book_path=self.book_path)
        recognized_text = ""
        if not self.debug:
            recognized_text = sound_recognizer.recognize(show_steps=True)

        block_counts = sound_recognizer.get_block_counts()

        # open book and get book text
        book_worker = book.BookWorker(self.book_path)
        book_text = book_worker.get_book_text_from_tree()

        # save recognize text to file
        if not self.debug:
            recognized_file = open(self.recognized_path, "w")
            recognized_file.write(recognized_text)
        else:
            recognized_file = open(self.recognized_path, "r")
            recognized_text = recognized_file.read()

        # save book text to file

        book_file = open(self.book_txt_path, "w")
        book_file.write(book_text)

        # write data to preprocessor file
        preprocessor_file = open(self.preprocessor_path, "wb")
        db_data = str(MIN_BLOCK_SIZE) + DIVIDER  # min block size of recognize audio (seconds)
        db_data += str(BLOCK_PADDING_SIZE) + DIVIDER

        for block_count in block_counts:
            db_data += str(block_count) + DIVIDER

        text_cipher = TextCipher(ENCRYPTION_KEY)
        if ENCRYPTION:
            db_data = text_cipher.encrypt(db_data)
        else:
            db_data = db_data.encode("UTF-8")
        preprocessor_file.write(db_data)
        preprocessor_file.close()
        book_file.close()
        recognized_file.close()

