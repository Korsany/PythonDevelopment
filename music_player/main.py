import tkinter
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog

from PIL import Image, ImageTk
from pygame import mixer

import os

'''from func import(
    about_us, play_music, pause_music, stop_music, set_vol, brows_file,
)'''


def about_us():
    tkinter.messagebox.showinfo('О проигрывателе', 'Это музыкательный проигрыватель разработан korsany тг: @semyonkors')


def brows_file():
    global filename
    filename = filedialog.askopenfilename()
    print(filename)


dirname = os.path.dirname(__file__) # Путь до каталога музыкального проигрывателя
mixer.init() # Инициализация объекта mixer(звуки)

# Созданик окна
root = Tk()


# Меню
menubar = Menu(root)
root.config(menu=menubar)

# Под меню "Файл"
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Файл', menu=subMenu)
subMenu.add_command(label='Открыть', command=brows_file)
subMenu.add_command(label='Выход')

# Под меню "Файл"Помощь
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Помощь', menu=subMenu)
subMenu.add_command(label='О программе', command=about_us)
subMenu.add_command(label='*_Пасхалка_*')


# Настройка окна
root.geometry('600x600')
root.title('Music player')

# Создание иконки
icon_filename = os.path.join(dirname, 'images/melody.ico')
im = Image.open(icon_filename)
photo = ImageTk.PhotoImage(im)
root.wm_iconphoto(True, photo)


# Создаём надпись
text = Label(root, text='Амогус')
text.pack() # Выводим в окно


def play_music():
    # Проверяем, инициализированна ли переменая "paused"
    try:
        paused
    except NameError:
    #music_file = os.path.join(dirname, 'journey.wav')
        try:
            print("one")
            mixer.music.load(filename)
            mixer.music.play()
            statusbar['text'] = "Воспроизведодится" + ' - ' + filename
        except:
            tkinter.messagebox.showerror('Файл не найден', 'Музыкальный проигрыватель не может найти файл, пожалуйста проверьте правильность пути до файла!')
    else:
        mixer.music.unpause()
        statusbar['text'] = "Воспроизведение возобновленно"


# Пауза
def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = 'Воспроизведение приостановленно!'


def stop_music():
    mixer.music.stop()


def set_vol(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)


# Создаём картинку - play
photo_icon_file = os.path.join(dirname, 'images/play.png')
im = Image.open(photo_icon_file)
photo = ImageTk.PhotoImage(im)
play_btn = Button(root, image=photo, command=play_music)
play_btn.pack()


# Регулятор громкости
scale = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)
scale.pack()


# Создаём картинку - stop
stop_icon_filename = os.path.join(dirname, 'images/stop.png')
im = Image.open(stop_icon_filename)
stop_photo = ImageTk.PhotoImage(im)
stop_btn = Button(root, image=stop_photo, command=stop_music)
stop_btn.pack()


# Создаём картинку - pause
pause_icon_filename = os.path.join(dirname, 'images/pause.png')
im = Image.open(pause_icon_filename)
pause_photo = ImageTk.PhotoImage(im)
pause_btn = Button(root, image=pause_photo, command=pause_music)
pause_btn.pack()


# Статусная строка
statusbar = Label(root, text='Добро подаловать в проигрыватель от Korsany', relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)








# Вывод окна
root.mainloop()