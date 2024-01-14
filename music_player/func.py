import tkinter
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog

from PIL import Image, ImageTk
from pygame import mixer


import os


dirname = os.path.dirname(__file__)

mixer.init() # Инициализация объекта mixer(звуки)

def about_us():
    tkinter.messagebox.showinfo('О проигрывателе', 'Это музыкательный проигрыватель разработан korsany тг: @semyonkors')


def brows_file():
    global filename
    filename = filedialog.askopenfilename()
    print(filename)

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