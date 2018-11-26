import sound_utils.SoundRecognizer as sr

sound_recognizer = sr.SoundRecognizer("res/harry_en.mp3", 15)
text = sound_recognizer.recognize_with_sphinx()
print(text)
