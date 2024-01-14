import tkinter
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog

from PIL import Image, ImageTk
from pygame import mixer

import os


dirname = os.path.dirname(__file__)

def about_us():
    tkinter.messagebox.showinfo('О проигрывателе', 'Это музыкательный проигрыватель разработан korsany тг: @semyonkors')


def brows_file():
    global filename
    filename = filedialog.askopenfilename()

def play_music():
    #music_file = os.path.join(dirname, 'journey.wav')
    try:
        mixer.music.load(filename)
        mixer.music.play()
    except:
        tkinter.messagebox.showerror('Файл не найден', 'Музыкальный проигрыватель не может найти файл, пожалуйста проверьте правильность пути до файла!')


# Пауза
def pause_music():
    global pause
    pause = TRUE
    mixer.music.pause()
    statusbar['text'] = 'Воспроизведение приостановленно!'


def stop_music():
    mixer.music.stop()


def set_vol(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)