from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk


# Функция изменения темы оформления
def change_theme(theme):
    text_field['bg'] = view_colors[theme]['text_bg']
    text_field['fg'] = view_colors[theme]['text_fg']
    text_field['insertbackground'] = view_colors[theme]['cursor']
    text_field['selectbackground'] = view_colors[theme]['select_bg']


# Функиция изменения шрифтового оформления
def change_fonts(font_name):
    text_field['font'] = fonts[font_name]['font']


# Функция команды "Закрыть" меню "Файл"
def notepad_exit():
    answer = messagebox.askokcancel('Выход', 'Вы точно хотите выйти?')
    if answer:  # Если ответ положителен
        root.destroy()


# Функция команды "Открыть" меню "Файл"
def open_file():
    file_path = filedialog.askopenfilename(title='Выбор файла', filetypes=(('Текстовые документы(*.txt)', '*.txt'), ('Все файлы', '*.*')))
    if file_path:
        text_field.delete('1.0', END)
        text_field.insert('1.0', open(file_path, encoding='utf-8').read())


# Создание основного объекта Tkinter(окна)
root = Tk()


# Заголовок окна текстового редактора
root.title("Текстовый редактор")

# Разрешение окна текстового редактора
root.geometry('640x480')


# Создание меню
main_menu = Menu(root)


# Раздел меню "Файл"
# tearoff=0 - запрет на отображение меню в отдельном окне
file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label='Открыть', command=open_file)
file_menu.add_command(label='Сохранить')


# добавление полосы-разделителя пунктов меню
file_menu.add_separator()
file_menu.add_command(label='Закрыть', command=notepad_exit)
root.config(menu=file_menu)


# Раздел меню "Вид"
view_menu = Menu(main_menu, tearoff=0)

# подменю "Вид"
view_menu_sub = Menu(view_menu, tearoff=0)
font_menu_sub = Menu(view_menu, tearoff=0)

# подменю "Вид" --> "Тема"
view_menu_sub.add_command(label='Тёмная', command=lambda: change_theme('dark'))
view_menu_sub.add_command(label='Светлая', command=lambda: change_theme('light'))
view_menu.add_cascade(label='Тема', menu=view_menu_sub)

# подменю "Вид" --> "Шрифт..."
font_menu_sub.add_command(label='Arial', command=lambda: change_fonts('Arial'))
font_menu_sub.add_command(label='Comic Sans MS', command=lambda: change_fonts('CSMS'))
font_menu_sub.add_command(label='Times New Roman', command=lambda: change_fonts('TNR'))
view_menu.add_cascade(label='Шрифт...', menu=font_menu_sub)
root.config(menu=view_menu)


# добавление списков меню
main_menu.add_cascade(label='Файл', menu=file_menu)
main_menu.add_cascade(label='Вид', menu=view_menu)
root.config(menu=main_menu)


# область набора и редактирования текста
f_text = Frame(root)

# "растягиваем" область по размеру окна
f_text.pack(fill=BOTH, expand=1)


# Стили оформления текстового редактора
# Словарь тем оформления
view_colors = {
    'dark': {
        'text_bg': 'black',
        'text_fg': 'lime',
        'curs': 'brown',
        'select_bg': '#8D917A'
    },
    'light': {
        'text_bg': 'white',
        'text_fg': 'black',
        'curs': '#A5A5A5',
        'select_bg': '#FAEEDD'
    }
}


# Сдловарь шрифтов
fonts = {
    'Arial': {
        'font': 'Arial 14 bold'
    },
    'CSMS': {
        'font': ('Comic Sans MS', 14, 'bold')
    },
    'TNR': {
        'font': ('Times New Roman', 14, 'bold')
    }
}


# виджет "поле для набора текста"
text_field = Text(f_text,
                    bg='black',
                    fg='lime',
                    # отступы от края экрана
                    padx=10,
                    pady=10,
                    # Перенос текста по словам
                    wrap=WORD,
                    # показываем курсор
                    insertbackground='brown',
                    # выделение текста
                    selectbackground="#8D917A",
                    # отступы между абзацами
                    spacing3=10
                    )


# выводим виджет набора текста в область окна
text_field.pack(expand=1, fill=BOTH, side=LEFT)


# добавление виджета полосы прокрутки
scroll = Scrollbar(f_text, command=text_field.yview)
scroll
