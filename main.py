from SoundRecognizer import SoundRecognizer

AUDIO_IN = "res/garry.mp3"
SoundRecognizer = SoundRecognizer(AUDIO_IN)
while True:
    t1 = int(input("time1:"))
    t2 = int(input("time2:"))
    print(SoundRecognizer.recognize_on_time(t1, t2))

