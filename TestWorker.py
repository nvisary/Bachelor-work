import preprocessor
import sound_utils.SoundRecognizer as sr
import matplotlib.pyplot as plt
import os
import numpy as np
import datetime
import time


class TestWorker:
    def __init__(self, mp3_path, book_path):
        self.mp3_path = mp3_path
        self.book_path = book_path

    def test1(self):
        """Зависимость блока распознавания от времени  и качества (сколько удачных точек синхронизации) работы алгоритма
            Тестируем блоки разной длины, начиная от 5 секунд, заканчивая 40"""
        min_block_sizes = [5, 10, 20, 30, 40, 60]
        success = [0] * 6
        fail = [0] * 6
        percents_success = [0] * 6
        rec_times = [0] * 6

        i = 0
        for block_size in min_block_sizes:
            sound_recognizer = sr.SoundRecognizer(self.mp3_path, min_block_size=block_size, padding=20,
                                                  book_path=self.book_path,
                                                  count_words_search=3)
            start = time.time()
            sound_recognizer.recognize(show_steps=True)
            end = time.time()
            data = sound_recognizer.get_data()
            print("Success: ", data['success'])
            print("Fail: ", data['fail'])
            print("Count: ", data['searches'])
            success[i] = data['success']
            fail[i] = data['fail']
            percents_success[i] = data['success'] / data['searches']
            rec_times[i] = int(end - start)
            i += 1

        percents_success = np.array(percents_success)
        plt.plot(min_block_sizes, percents_success * 100)
        plt.title("Размер блока / качество распознавания")
        plt.xlabel("Размер блока распознавания [секунды]")
        plt.ylabel("% Положительных результатов")
        plt.show()
        self.save_results("test1", {"min_blocks_sizes": min_block_sizes,
                                    "percent_success": percents_success * 100,
                                    "success": success,
                                    "fail": fail,
                                    "recognition_times": rec_times})

    def test2(self):
        """Зависимость размера блока распознавания от времени работы алгоритма"""
        times = [96, 123, 161, 192, 213, 223]
        min_block_sizes = [5, 10, 20, 30, 40, 60]
        plt.plot(min_block_sizes, times)
        plt.title("Размер блока / времени распознавания аудио 25 минут")
        plt.xlabel("Размер блока распознавания [секунды]")
        plt.ylabel("Время распознавания 25 минут книги")
        plt.show()

    def test3(self):
        min_block_sizes = [10, 30]
        search_blocks = [2, 3, 4, 5, 6]

        success = [0] * len(min_block_sizes) * len(search_blocks)
        fail = [0] * len(min_block_sizes) * len(search_blocks)
        percents_success = [0] * len(min_block_sizes) * len(search_blocks)
        i = 0
        for min_block in min_block_sizes:
            for search_block in search_blocks:
                sound_recognizer = sr.SoundRecognizer(self.mp3_path, min_block_size=min_block, padding=20,
                                                      book_path=self.book_path,
                                                      count_words_search=search_block)
                sound_recognizer.recognize(show_steps=True)

                data = sound_recognizer.get_data()
                print("Success: ", data['success'])
                print("Fail: ", data['fail'])
                print("Count: ", data['searches'])
                success[i] = data['success']
                fail[i] = data['fail']
                percents_success[i] = data['success'] / data['searches']
                i += 1

        percents_success = np.array(percents_success)
        percents_success = percents_success * 100
        plt.plot(search_blocks, percents_success[:5], label="Блок распознавания {} секунд".format(min_block_sizes[0]))
        plt.plot(search_blocks, percents_success[5:], label="Блок распознавания {} секунд".format(min_block_sizes[1]))
        plt.legend()
        plt.title("Размер блока поиска / качество распознавания")
        plt.xlabel("Размер блока поиска [слов]")
        plt.ylabel("% Положительных результатов")
        plt.show()
        self.save_results("test3", {"min_blocks_sizes": min_block_sizes,
                                    "percent_success": percents_success,
                                    "success": success,
                                    "fail": fail})

    def save_results(self, file_name, results):
        path = "tests/" + file_name
        if not os.path.exists(path):
            os.mkdir(path)
        now = datetime.datetime.now()

        for key in results:
            file = "/" + str(key) + "_" + str(now.strftime("%d-%H_%M_%S")) + ".txt"
            f = open(path + file, "w")
            f.write(str(results[key]))
            f.close()


test = TestWorker("res/harry/harry-big.mp3", "res/harry.fb2")
test.test3()
