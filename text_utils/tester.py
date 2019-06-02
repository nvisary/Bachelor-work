from text_utils.book import BookWorker
from sound_utils.SoundRecognizer import SoundRecognizer
import time
import Levenshtein
import numpy as np
import random

start = time.time()
book_path = "../res/harry.fb2"
audio_path = "../res/harry/harry-big.mp3"
audio_block = 20


def get_levenshtein(text1, text2):
    if len(text1) == len(text2):
        ratios = []
        for i in range(len(text1)):
            ratios.append(Levenshtein.ratio(text1[i], text2[i]))
        return np.mean(ratios)
    return None

'''
print("Open audio")
sound_rec = SoundRecognizer(audio_path, audio_block)
audio_length = sound_rec.get_audio_length()
f = open("text.txt", "w")
f.write(sound_rec.recognize(show_steps=True))

first = sound_rec.recognize_on_time(10, 70)
second = sound_rec.recognize_on_time(int(audio_length / 2), int(audio_length / 2) + 60)
speech_speed = int((len(first.split()) + len(second.split())) / 2)

print("Скорость говорящего: ", speech_speed)

f = open("text.txt", "r")
book_worker = BookWorker(book_path)
book_text = book_worker.get_book_text_from_tree()
rec_text = f.read()
rec_text = rec_text.split()
book_text = book_text.split()

log = open("log.txt", "w")
border = random.randint(0, len(rec_text))
print(rec_text[border:border + 3])
for i in range(len(rec_text)):
    log.write(str(rec_text[border:border + 3]))
    log.write(str(book_text[i:i + 3]) + str(" "))
    lev = get_levenshtein(rec_text[border:border + 3], book_text[i:i + 3])
    if lev > 0.8:
        print("Found: [{}]".format(i))
        print(book_text[i - 3: i + 10])

    log.write(str(lev))
    log.write("\n")
'''
f = open("text.txt", "r")
rec_text = f.read()
rec_text = rec_text.split()
print(len(rec_text))

book_worker = BookWorker(book_path)
book_text = book_worker.get_book_text_from_tree().split()
print(book_text[1720:1740])

end = time.time()
print("Время выполнения: {} секунд".format(int(end - start)))


