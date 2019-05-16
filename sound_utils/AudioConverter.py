from pydub import AudioSegment

audio = AudioSegment.from_mp3("../res/harry/harry-big.mp3")
audio.export("../res/harry/harry-big.wav", format="wav")