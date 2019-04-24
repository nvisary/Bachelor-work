import sublime
import sublime_plugin
import os


class TestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view_name = self.view.file_name()
        r = sublime.Region(0, self.view.size())
        alltext = self.view.substr(r)
        alltext = alltext.split()
        sel_begin = self.view.sel()[0].begin()
        count_letters = 0
        selected_word = 1
        for word in alltext:
            count_letters += len(word)
            count_letters += 1
            if count_letters >= sel_begin:
                break
            selected_word += 1
        print("selected word: {}".format(selected_word))
        path = os.path.dirname(view_name)
        print("python " + path + "\\main.py --reverse-sync " + path + "/res/book1.mp3 " + path + "/res/book1.fb2 {}".format(
                selected_word))
        os.system("python " + path + "/main.py --reverse-sync " + path + "/res/book1.mp3 " + path + "/res/book1.fb2 {}".format(
                selected_word))
