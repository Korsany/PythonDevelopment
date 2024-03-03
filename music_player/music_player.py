import os
import threading
import time

import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from ttkthemes import themed_tk as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pygame import mixer
from mutagen.mp3 import MP3

# путь до текущего каталога музыкального проигрывателя
dirname = os.path.dirname(__file__)

window = tk.ThemedTk(theme="radiance")

def about_us():
    tkinter.messagebox.showinfo('О проигрывателе', 'Этот музыкальный проигрыватель разработан \n'
                                'на основе библиотеки Tkinter и языка Python')

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

# добавление в список воспроизведения
def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index,filename)
    playlist.insert(index,filename_path)
    index += 1                                    

# Меню
menubar = Menu(window)
window.config(menu=menubar)

# список воспроизведения
playlist = []

# Подменю "Файл"
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Файл", menu=subMenu)
subMenu.add_command(label="Открыть", command=browse_file)
subMenu.add_command(label="Выход", command=window.destroy)
# Подменю "Помощь"
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Помощь", menu=subMenu)
subMenu.add_command(label="О программе", command=about_us)
mixer.init()  # инициализация объекта mixer
window.geometry('600x600')
window.title("Музыкальный проигрыватель Мелодия")
# иконка окна проигрывателя
icon_filename = os.path.join(dirname, "images/melody.ico")
im = Image.open(icon_filename)
photo = ImageTk.PhotoImage(im)
window.wm_iconphoto(True, photo)

# Window - статусная строка(StatusBar), левый фрейм(left_frame)
#           правый фрейм(right_frame)
# Левый фрейм (left_frame) - список listbox (playlist)
# Правый фрейм (right_frame) - верхний фрейм(top_frame),
# Центральный фрейм(middleframe) и нижний фрейм(bottom_frame)

# создание фрейма слева
left_frame = ttk.Frame(window)
left_frame.pack(side=LEFT, padx=30)

# добавление виждета списка вопроизведения
playlistbox = Listbox(left_frame)
playlistbox.pack()

# кнопка добавить в список воспроизведения
addbtn = ttk.Button(left_frame, text="+ Добавить", command=browse_file)
addbtn.pack(side=LEFT)

# Функция удаления песни из исписка
def del_song():
    selected_song = playlistbox.curselection()
    try:    
        selected_song = int(selected_song[0])
        if not mixer.music.get_busy():
            playlistbox.delete(selected_song)
            playlist.pop(selected_song)
        else:
            stop_music()
            playlistbox.delete(selected_song)
            playlist.pop(selected_song)
    except IndexError:
        tkinter.messagebox.showerror("Песня не найдена", "Выбирите музыку из списка, для удаления")

# кнопка удалить из списка воспроизведения
delbtn = ttk.Button(left_frame, text="- Удалить", command=del_song)
delbtn.pack(side=LEFT)

right_frame = ttk.Frame(window)
right_frame.pack()

top_frame = ttk.Frame(right_frame)
top_frame.pack()

lengthlabel = ttk.Label(top_frame, text="Продолжительность : --:--")
lengthlabel.pack(pady=5)

currenttimelabel = ttk.Label(top_frame, text='Прошло : --:--', relief=GROOVE)
currenttimelabel.pack()

# Показ дополнительной информации о воспроизводимой мелодии
def show_details(play_song):
    file_data = os.path.splitext(play_song)
    # анализ расширения воспроизводимого файла
    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:    
        a = mixer.Sound(play_song)
        total_length = a.get_length()
    # div - total_length / 60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Продолжительность" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()

# Функция подсчёта текущего времени воспроизведения
def start_count(t):
    global paused
    # mixer.music.get_busy(): 
    # Возвращает FALSE, когда нажата кнопка "Стоп"
    # (воспроизведение было остановлено)
    # Continue - игнорирует все операторы ниже этой команды.
    # Проверяем: приостановлено ли воспроизведение или нет.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Прошло: " + timeformat
            time.sleep(1)
            current_time = current_time + 1  # x += 1


def play_music():
    # music_file = os.path.join(dirname, "journey.wav")
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Воспроизведение возобновлено"
        paused = FALSE
    else:    
        try:
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Воспроизводится" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
           tkinter.messagebox.showerror('Файл не найден', 'Музыкальный проигрыватель не может найти файл. Пожалуйста проверьте правильность пути до файла.')
           print('Ошибка')            

def stop_music():
    mixer.music.stop()
    lengthlabel['text'] = 'Продолжительность: --:--'
    currenttimelabel['text'] = 'Прошло: --:-'
    statusbar['text'] = "Воспроизведение остановлено"

paused = FALSE    

# Функция "Паузы"
def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Воспроизведение приостановлено"

# Функция перемотки воспроизведения
def rewind_music():
    play_music()
    statusbar['text'] = "Перемотка назад"        

def set_vol(val):
    # функция set_volume() объекта mixer принимает на вход
    # значения от 0 до 1. Например: 0, 0.1, 0.55, 0.99, 1.
    volume = int(val) / 100
    mixer.music.set_volume(volume)

muted = FALSE  # флаг установки беззвучного режима (FALSE - не установлен, TRUE - установлен)

# Функция установки беззвучного режима
def mute_music():
    global muted
    if muted:
        # выход из беззвучного режима
        mixer.music.set_volume(0.7)
        volume_btn.configure(image=volume_photo)
        scale.set(70)
        muted = FALSE
    else:
        # включение беззвучного режима
        mixer.music.set_volume(0)
        volume_btn.configure(image=mute_photo)
        scale.set(0)
        muted = TRUE    

middleframe = Frame(right_frame)
middleframe.pack(pady=30, padx=30)      

play_icon_filename = os.path.join(dirname, 'images/play.png')
im = Image.open(play_icon_filename)
photo = ImageTk.PhotoImage(im)
play_btn = ttk.Button(middleframe, image=photo, command=play_music)
#play_btn.pack(side=LEFT, padx=10)
play_btn.grid(row=0, column=0, padx=10)

bottomframe = Frame(right_frame)
bottomframe.pack()

rewind_icon_filename = os.path.join(dirname, 'images/rewind.png')
im = Image.open(rewind_icon_filename)
rewind_photo = ImageTk.PhotoImage(im)
rewind_btn = ttk.Button(bottomframe, image=rewind_photo, command=rewind_music)
rewind_btn.grid(row=0, column=0)

mute_icon_filename = os.path.join(dirname, 'images/mute.png')
volume_icon_filename = os.path.join(dirname, 'images/volume.png')
mute_im = Image.open(mute_icon_filename)
volume_im = Image.open(volume_icon_filename)
mute_photo = ImageTk.PhotoImage(mute_im)
volume_photo = ImageTk.PhotoImage(volume_im)
volume_btn = ttk.Button(bottomframe, image=volume_photo, command=mute_music)
volume_btn.grid(row=0, column=1)

stop_icon_filename = os.path.join(dirname, 'images/stop.png')
im = Image.open(stop_icon_filename)
stop_photo = ImageTk.PhotoImage(im)
stop_btn = ttk.Button(middleframe, image=stop_photo, command=stop_music)
#stop_btn.pack(side=LEFT, padx=10)
stop_btn.grid(row=0, column=1, padx=10)

pause_icon_filename = os.path.join(dirname, 'images/pause.png')
im = Image.open(pause_icon_filename)
pause_photo = ImageTk.PhotoImage(im)
pause_btn = ttk.Button(middleframe, image=pause_photo, command=pause_music)
#pause_btn.pack(side=LEFT, padx=10)
pause_btn.grid(row=0, column=2, padx=10)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)
#scale.pack(pady=15)
scale.grid(row=0, column=2, pady=15, padx=30)

# Статусная строка
statusbar = ttk.Label(window, text="Добро пожаловать в проигрыватель 'Мелодия'", relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

# При закрытии окна проигрывателя
def on_closing():
    stop_music()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()