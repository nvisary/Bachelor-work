import sys
import preprocessor as pr
import sync
import argparse
import sound_utils.Player as sound_utils


PREPROCESSOR_PATH = "res/sync_bd.txt"


def initial_sync(mp3_path, book_path, db_path):
    preprocessor = pr.Preprocessor(mp3_path, book_path, db_path)
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
    synchronizer.sync_from(second)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize audio book and fb2 book.")
    parser.add_argument('--initial-sync', dest="initial_sync", action="store", nargs=3,
                        help="Initial sync")
    parser.add_argument('--sync', dest="sync", action="store", nargs=3, help="Sync mp3 and fb2 on seconds range")
    parser.add_argument('--play', dest="play", action="store", nargs=3, help="Play mp3 starts from n second")
    parser.add_argument('--self-test', dest="self_test_db", action="store", nargs=1,
                        help="Self test. Use early writen db")

    args = parser.parse_args()

    if args.initial_sync:
        initial_sync(args.initial_sync[0], args.initial_sync[1], args.initial_sync[2])
    if args.play:
        play(args.play[0], args.play[1], args.play[2])
    if args.self_test_db:
        print("self")
    if args.sync:
        syncronize(args.sync)



