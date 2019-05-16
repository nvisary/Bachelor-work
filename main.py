import sys
import preprocessor as pr
import sync
import argparse
import sound_utils.Player as sound_utils
import os

PREPROCESSOR_PATH = os.path.dirname(__file__) + "/res/sync_db-big.txt"


def initial_sync(mp3_path, book_path, db_path, debug):
    preprocessor = pr.Preprocessor(mp3_path, book_path, db_path, debug)
    preprocessor.preprocess()


def play(mp3_path, second, duration):
    player = sound_utils.Player(mp3_path)
    player.play_from(int(second), int(duration))


def preprocessor(argv):
    mp3_path = argv[2]
    book_path = argv[3]
    print("You run preprocessor.")
    print("Path to mp3: " + mp3_path)
    print("Path to book: " + book_path)
    preprocessor = pr.Preprocessor(mp3_path, book_path, PREPROCESSOR_PATH)
    preprocessor.preprocess()


def syncronize(argv):
    mp3_path = argv[0]
    book_path = argv[1]
    second = int(argv[2])
    print("You run sync.")
    print("Path to mp3: " + mp3_path)
    print("Path to book: " + book_path)
    print("Run from sec: " + str(second))
    synchronizer = sync.Sync(PREPROCESSOR_PATH, mp3_path, book_path)
    synchronizer.sync_from_audio(second)


def reverse_sync(argv):
    mp3_path = argv[0]
    book_path = argv[1]
    word = int(argv[2])
    print("You run reverse-sync.")
    print("Path to mp3: " + mp3_path)
    print("Path to book: " + book_path)
    print("Run from word: " + str(word))
    synchronizer = sync.Sync(PREPROCESSOR_PATH, mp3_path, book_path)
    synchronizer.sync_from_text(word)


def compare_test(argv):
    book = "book"
    max_books = 4
    for i in range(3, max_books + 1):
        path_to_audio = argv[0] + "/" + book + str(i) + ".mp3"
        path_to_fb2 = argv[0] + "/" + book + str(i) + ".fb2"
        recognized = argv[0] + "/recognized{}.txt".format(i)
        book_txt = argv[0] + "/book{}.txt".format(i)
        result = argv[0] + "/res{}.txt".format(i)

        #preprocessor = pr.Preprocessor(path_to_audio, path_to_fb2, argv[0] + "/sync_db{}.txt".format(i), False,
        #                               recognized_path=recognized, book_txt_path=book_txt)
        #preprocessor.preprocess()

        recognized_file = open(recognized, "r")
        book_file = open(book_txt, "r")
        result_file = open(result, "w")

        recognized_text = recognized_file.read()
        book_text = book_file.read()

        recognized_text = recognized_text.split()
        book_text = book_text.split()
        result_text = ""
        block_size = 20
        i = 0
        while i < len(recognized_text):
            result_text += "r:" + str(recognized_text[i:i + block_size]) + "\n" + "b:" + str(
                book_text[i:i + block_size]) + "\n\r"
            i += block_size

        result_file.write(result_text)

        recognized_file.close()
        book_file.close()
        result_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize audio book and fb2 book.")
    parser.add_argument('--initial-sync', dest="initial_sync", action="store", nargs=3,
                        help="Initial sync")
    parser.add_argument('--sync', dest="sync", action="store", nargs=3, help="Sync mp3 and fb2 on seconds range")
    parser.add_argument("--reverse-sync", dest="reverse_sync", action="store", nargs=3, help="Sync mp3 and fb2 on word")
    parser.add_argument('--play', dest="play", action="store", nargs=3, help="Play mp3 starts from n second")
    parser.add_argument('--self-test', dest="self_test_db", action="store", nargs=1,
                        help="Self test. Use early writen db")
    parser.add_argument('--debug', dest="debug", action="store", default=False, type=bool)

    parser.add_argument('--compare-test', dest="compare_test", action="store", nargs=1,
                        help="Run compare test arg is folder where books and audios stored")

    args = parser.parse_args()

    if args.initial_sync:
        initial_sync(args.initial_sync[0], args.initial_sync[1], args.initial_sync[2], args.debug)
    if args.play:
        play(args.play[0], args.play[1], args.play[2])
    if args.self_test_db:
        print("self")
    if args.sync:
        syncronize(args.sync)
    if args.reverse_sync:
        reverse_sync(args.reverse_sync)
    if args.compare_test:
        compare_test(args.compare_test)
