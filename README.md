# Bachelor-work
University bachelor work

Libs:
pip install SpeechRecognition pydub PyAudio pocketsphinx
pip install pycryptodome
    
Установка плагина. 
1. Установить все зависимости библиотеки Kivy

    sudo add-apt-repository ppa:kivy-team/kivy
    
    sudo apt-get update
    sudo apt-get install python3-kivy
   
    sudo apt-get install -y \
    libgstreamer1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good
    
    Установить только отсутствующие зависимости: 
    sudo apt-get install -y \
    python-pip \
    build-essential \
    git \
    python \
    python-dev \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev
    
    подробная информация по установке: Bachelor-work/gui/Installation on Linux.pdf
2. Поместить файл Bachelor-work/sublime_plugin/plugin.py 
в директорию где находятся конфиги Sublime
    Обычно это: ~/.config/sublime-text-3/Packages
3. В файле plugin.py настроить путь к python
   Если при вызове из консоли третьего python используется python3 main.py (а не python main.py)
   тогда исправить строку 25 на 
   os.system("python3 " + path + "/main.py --reverse-sync " + path + "/res/book1.mp3 " + path + "/res/book1.fb2 {}".format(
                selected_word))
   Если при вызове третьего python используется python main.py 
   Тогда исправлять не нужно
4. В sublime открыть Preferences -> Key Bindings
    и вставить данный шорткей:
    [
	    { "keys": ["ctrl+shift+p"], "command": "test" }
    ]
5. В sublime открыть файл Bachelor-work/book.txt (открывать только те файлы, которые находятся в корне проекта)
   Выделить нужное слово и нажать ctrl+shift+p
   Должен открыться терминал, а затем запуститься UI
