import kivy

from kivy.app import App
from kivy.config import Config
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
import os

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '200')

# audio = AudioSegment.from_mp3('../res/cutted.mp3')
# audio.export("../res/cutted.wav", format="wav")

sound = SoundLoader.load('res/cutted.wav')

location = 0


def play_btn_click(instance):
    global location
    if sound.state == "play":
        location = sound.get_pos()
        sound.stop()
        instance.text = "Play"
    else:
        sound.play()
        sound.seek(location)
        instance.text = "Pause"


def reset_btn_click(instance):
    global location
    location = 0
    sound.stop()


class AudioPlayer(App):
    btn_left = Button(text="Play",
                      on_press=play_btn_click,
                      background_color=[.06, .31, .55, 1],
                      background_normal="",
                      font_size=25,
                      size_hint=(.5, .25),
                      pos=(0, 0))

    btn_right = Button(text="Reset",
                       on_press=reset_btn_click,
                       background_color=[.06, .31, .55, 1],
                       background_normal="",
                       font_size=25,
                       size_hint=(.5, .25),
                       pos=(100, 0))
    lbl_time = Label(text="00:00",
                     font_size=25,
                     pos=(0, 50))
    layout = FloatLayout(size=(200, 200))

    def build(self):
        Clock.schedule_interval(self.on_tick, 1)
        self.layout.add_widget(self.btn_right)
        self.layout.add_widget(self.btn_left)
        self.layout.add_widget(self.lbl_time)
        return self.layout

    def on_tick(self, dt):
        self.lbl_time.text = str(location)



player = AudioPlayer()
player.run()
