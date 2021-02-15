import os
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb

from file_ordering import FileOrdering


def clear_text():
    answer = mb.askyesno(title="Вопрос", message="Очистить текстовое поле?")
    if answer == True:
        text.delete(1.0, END)


def insertText():
    try:
        file_name = fd.askopenfilename()
        f = open(file_name)
        s = f.read()
        text.insert(1.0, s)
        f.close()
    except FileNotFoundError:
        mb.showwarning('Ошибка', 'Не указан файл для открытия')


def extractText():
    try:
        file_name = fd.asksaveasfilename(filetypes=(("TXT files", "*.txt"),
                                                    ("HTML files", "*.html;*.htm"),
                                                    ("All files", "*.*")))
        f = open(file_name, 'w')
        s = text.get(1.0, END)
        f.write(s)
        f.close()
    except FileNotFoundError:
        mb.showwarning('Ошибка', 'Не указан файл для сохранения. Данные не сохранены')


def load_folder():
    try:
        folder_path = fd.askopenfilename()


    except FileNotFoundError:
        mb.showwarning('Ошибка', 'Не указан файл для открытия')


def count_file_number():
    try:
        folder_path = entry_source_folder.get()
        folder_path = os.path.normpath(folder_path)
        if os.path.exists(folder_path) and folder_path != '.':
            label_error_message['text'] = 'Такой путь сущестует'
        else:
            label_error_message['text'] = 'Такого пути не сущесвует'

    except EXCEPTION as e:
        print(f'Произошла ошибка: {e}')


root = Tk()
root.title("Упорядочиватель файлов")
root.minsize(width=800, height=600)

label_source_folder = Label(root, text='Укажите папку с файлами')
label_source_folder.place(x=50, y=5)

entry_source_folder = Entry(root, width=80)
entry_source_folder.place(x=40, y=25)

label_target_folder = Label(root, text='Укажите папку куда положить упорядоченные файлы')
label_target_folder.place(x=50, y=55)

entry_target_folder = Entry(root, width=80)
entry_target_folder.place(x=40, y=80)

button_count_files_number = Button(text="Посчитать количество файлов", command=count_file_number)
button_count_files_number.place(x=60, y=100)

label_error_message = Label(root)
label_error_message.place(x=60, y=150)
root.mainloop()
