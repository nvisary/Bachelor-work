import sys
import preprocessor as pr
import sync
PREPROCESSOR_PATH = "prep.txt"


def preprocessor(argv):
    mp3_path = argv[2]
    book_path = argv[3]
    print("You run preprocessor.")
    print("Path to mp3: " + mp3_path)
    print("Path to book: " + book_path)
    preprocessor = pr.Preprocessor(mp3_path, book_path, PREPROCESSOR_PATH)
    preprocessor.preprocess()


def syncronize(argv):
    mp3_path = argv[2]
    book_path = argv[3]
    second = int(argv[4])
    print("You run sync.")
    print("Path to mp3: " + mp3_path)
    print("Path to book: " + book_path)
    print("Run from sec: " + str(second))
    synchronizer = sync.Sync(PREPROCESSOR_PATH, mp3_path, book_path)
    synchronizer.sync_from(second)


if __name__ == "__main__":
    '''Use --preprocessor <audio_path.mp3> <book_path.fb2>
       Use sync after preprocessor(!)
       Use --sync <audio_path.mp3> <book_path.fb2> <seconds count>
    '''
    argv = sys.argv
    if len(argv) < 4:
        exit(1)
    if argv[1] == "--preprocessor":
        preprocessor(argv)
    if argv[1] == "--sync":
        syncronize(argv)
