import sound_utils.SoundRecognizer as sr
import text_utils.book as book
from text_utils.TextCipher import TextCipher
import text_utils.text_analyzer as text_analyzer

DIVIDER = '\n'
MIN_BLOCK_SIZE = 20
RECOGNIZED_FILE_PATH = "recognized.txt"
BOOK_FILE_PATH = "book.txt"
COMPARE_LIMIT = 0.5
ENCRYPTION = True


class Preprocessor:
    def __init__(self, path_to_mp3, path_to_book, preprocessor_path, debug):
        self.mp3_path = path_to_mp3
        self.book_path = path_to_book
        self.preprocessor_path = preprocessor_path
        self.debug = debug

    def preprocess(self):
        # recognize mp3 file and get text
        sound_recognizer = sr.SoundRecognizer(self.mp3_path, MIN_BLOCK_SIZE)
        recognized_text = ""
        if not self.debug:
            recognized_text = sound_recognizer.recognize(show_steps=True, book_path=self.book_path)

        block_counts = sound_recognizer.get_block_counts()

        # open book and get book text
        book_worker = book.BookWorker(self.book_path)
        book_text = book_worker.get_book_text_from_tree()

        # save recognize text to file
        if not self.debug:
            recognized_file = open(RECOGNIZED_FILE_PATH, "w")
            recognized_file.write(recognized_text)
        else:
            recognized_file = open(RECOGNIZED_FILE_PATH, "r")
            recognized_text = recognized_file.read()
            self.find_padding(book_text, recognized_text)

        # save book text to file

        book_file = open(BOOK_FILE_PATH, "w")
        book_file.write(book_text)

        # write data to preprocessor file
        preprocessor_file = open(self.preprocessor_path, "wb")
        db_data = str(MIN_BLOCK_SIZE) + DIVIDER  # min block size of recognize audio (seconds)

        for block_count in block_counts:
            db_data += str(block_count) + DIVIDER

        text_cipher = TextCipher("Hello world")
        if ENCRYPTION:
            db_data = text_cipher.encrypt(db_data)
        else:
            db_data = db_data.encode("UTF-8")
        preprocessor_file.write(db_data)
        preprocessor_file.close()
        book_file.close()
        recognized_file.close()

    def find_padding(self, book_text, recognized_text):
        book_text = book_text.split()
        recognized_text = recognized_text.split()
        log = open("debug_out.txt", "w")
        print(book_text[:30])
        print(recognized_text[:30])
        block = 3
        i = 0
        j = 0
        accepted = []
        stop_position = 25
        counts = [0] * 10
        while j < len(recognized_text):
            if j + block >= len(recognized_text):
                log.write(str(accepted))
                log.write(str(counts))
                return
            print(str(j) + "/" + str(stop_position))
            while i < len(book_text):
                if i + block >= 2000:
                    break
                rec_block = recognized_text[j:j + block]
                text_block = book_text[i:i + block]
                log.write(str(rec_block))
                log.write(str(text_block))
                lev = text_analyzer.compare(rec_block, text_block)
                counts[int((lev * 10) % 10)] += 1
                log.write("result: " + str(lev) + "\n")

                if lev >= COMPARE_LIMIT:
                    accepted.append({"levenstein": lev, "rec": rec_block, "text": text_block})

                i += block
            j += block
            i = 0
            if j >= stop_position:
                break
        log.write(str(accepted))
        log.write(str(counts))