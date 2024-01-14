import tkinter
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog

from PIL import Image, ImageTk
from pygame import mixer

import os

from func import(
    about_us, play_music, stop_music, set_vol, brows_file
)


# Путь до каталога музыкального проигрывателя
dirname = os.path.dirname(__file__)

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


mixer.init() # Инициализация объекта mixer(звуки)

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


# Создаём картинку - play
photo_icon_file = os.path.join(dirname, 'images/play.png')
im = Image.open(photo_icon_file)
photo = ImageTk.PhotoImage(im)
play_btn = Button(root, image=photo, command=play_music)
play_btn.pack()

# Создаём картинку - stop
stop_icon_filename = os.path.join(dirname, 'images/stop.png')
im = Image.open(stop_icon_filename)
stop_photo = ImageTk.PhotoImage(im)
stop_btn = Button(root, image=stop_photo, command=stop_music)
stop_btn.pack()

scale = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)
scale.pack()

statusbar = Label(root, text='Добро подаловать в проигрыватель от Korsany', relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)



# Вывод окна
root.mainloop()