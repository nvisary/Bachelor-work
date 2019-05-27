from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from pydub import AudioSegment
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
import os
import sys
sys.path.append(os.path.join(sys.path[0], "../"))

import math
import text_utils.book as book
import sync
import os.path

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '600')
Builder.load_file("GuiApp.kv")
Builder.load_file("load_dialog.kv")
PAGE_LENGTH = 1800  # symbols in page
PATH = os.path.abspath(os.path.join(__file__, "../"))


class MainScreen(Screen):
    # mp3 = AudioSegment.from_mp3("res/harry.mp3")
    mp3 = AudioSegment.from_mp3("res/harry/harry-big.mp3")
    audio_length = int(len(mp3) / 1000)
    mp3.export("res/harry/harry-big.wav", format="wav")
    audio = SoundLoader.load('res/harry/harry-big.wav')

    synchronizer = sync.Sync(PATH + "../res/sync_db-big.txt", PATH + "../res/harry.mp3", PATH + "../res/harry.fb2")
    current_second = 0
    current_page = 1
    current_selected_word = -1
    book_worker = book.BookWorker(PATH + "../res/harry.fb2")
    book_text = book_worker.get_book_text_from_tree()
    spliced_book = book_text.split()
    pages = int(len(book_text) / PAGE_LENGTH) + 1
    seek_size = 30

    def __init__(self, **kw):
        super().__init__(**kw)
        self.lbl_pages.text = str(self.current_page) + "/" + str(self.pages)
        self.txt_input.text = self.book_text[(self.current_page - 1) * PAGE_LENGTH:
                                             (self.current_page - 1) * PAGE_LENGTH + PAGE_LENGTH]
        Clock.schedule_interval(self.timer, 1)

    def update_page(self):
        self.txt_input.text = self.book_text[(self.current_page - 1) * PAGE_LENGTH:
                                             self.current_page * PAGE_LENGTH]
        self.lbl_pages.text = str(self.current_page) + "/" + str(self.pages)

    def play_audio(self):
        if self.audio.state != "play":
            self.btn_play.source = "pause.png"
            self.audio.play()
            self.audio.seek(self.current_second)

    def stop_audio(self):
        if self.audio.state == "play":
            self.btn_play.source = "play.png"
            self.current_second = self.audio.get_pos()
            self.audio.stop()

    def play_click(self, instance):
        if self.audio.state == "play":
            self.stop_audio()
        else:
            self.play_audio()

    def timer(self, dt):
        if self.audio.state == "play":
            self.current_second += 1
            self.update_time()
            self.time_slider.value = int(self.current_second * 100 / self.audio_length)

            sync_word = self.synchronizer.sync_from_audio(self.current_second, False)

            if sync_word != self.current_selected_word:
                self.current_selected_word = sync_word

                count_words = sync_word
                count_symbols = 0
                while count_words != 0:
                    count_symbols += len(self.spliced_book[count_words - 1])
                    count_words -= 1
                pages = math.ceil(count_symbols / PAGE_LENGTH)
                self.current_page = pages
                self.update_page()

                while count_symbols > PAGE_LENGTH:
                    count_symbols -= PAGE_LENGTH
                    print("Count symbols: ", count_symbols)
                self.txt_input.select_text(count_symbols, count_symbols + 100)

    def audio_seek(self, direction):
        if self.audio.state == "play":
            if direction == "Back":
                if self.current_second - self.seek_size > 0:
                    self.current_second -= self.seek_size
                else:
                    self.current_second = 0
            elif direction == "Forward":
                if self.current_second + self.seek_size > self.audio_length:
                    self.current_second = self.audio_length - 10
                else:
                    self.current_second += self.seek_size
            self.audio.seek(self.current_second)

    def time_slider_touch_up(self, touch):
        touch_x = touch.pos[0]
        touch_y = touch.pos[1]
        if 320 < touch_x < 570 and 18 < touch_y < 53:
            self.play_audio()
            # if self.audio.state == "play":
            # self.audio.seek(self.current_second)

    def time_slider_moved(self, touch):
        touch_x, touch_y = touch.pos[0], touch.pos[1]

        if 320 < touch_x < 570 and 18 < touch_y < 53:
            self.stop_audio()
            self.current_second = int(self.audio_length * self.time_slider.value / 100)
            self.update_time()

            # self.play_audio_from_current_sec()

    def play_audio_from_current_sec(self):
        if self.audio.state == "play":
            self.audio.stop()
        self.audio.play()
        self.audio.seek(self.current_second)

    def update_time(self):
        hours = 0
        minutes = 0
        seconds = int(self.current_second)
        while seconds > 59:
            minutes += 1
            seconds -= 59

        while minutes > 59:
            hours += 1
            minutes -= 59

        if hours < 10:
            hours = "0" + str(hours)

        if minutes < 10:
            minutes = "0" + str(minutes)
        if seconds < 10:
            seconds = "0" + str(seconds)
        self.lbl_time.text = "{}:{}:{}".format(hours, minutes, seconds)
        self.time_slider.value = int(self.current_second * 100 / self.audio_length)

    def text_input_touched(self, touch):
        touch_position = touch.pos
        touch_x = touch_position[0]
        touch_y = touch_position[1]
        if 550 >= touch_y >= 65:
            if touch_x < 300:
                if self.current_page > 1:
                    self.current_page -= 1
                    self.update_page()
            else:
                if self.current_page <= self.pages:
                    self.current_page += 1
                    self.update_page()
            count_symbols = PAGE_LENGTH * self.current_page
            count_words = 0
            while count_symbols > 0:
                count_symbols -= len(self.spliced_book[count_words])
                count_words += 1
            if self.current_page == 1:
                self.current_second = 0
            else:
                self.current_second = self.synchronizer.sync_from_text(count_words, False)
            self.update_page()
            self.update_time()
        # Добавить обновление секунд и если включено аудио перемотка (при переключении страницы)


class LibraryScreen(Screen):
    def dismiss_popup(self):
        self._popup.dismiss()


    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()

        self.dismiss_popup()

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)




class ImageButton(ButtonBehavior, Image):
    pass


sm = ScreenManager()
sm.add_widget(MainScreen())
sm.add_widget(LibraryScreen())


class GuiApp(App):

    def build(self):
        return sm


GuiApp().run()

'''Button:
                size_hint: .15, .85
                text: "Back"
                on_press:
                    root.manager.transition.direction = "left"
                    root.manager.current = "main"'''
