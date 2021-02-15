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
            count = 0
            for dirpath, dirnames, filenames in os.walk(folder_path):
                for file_name in filenames:
                    count += 1
                    label_information_message['text'] = f'В этой папке {count} файлов'


        else:
            label_information_message['text'] = ''
            label_error_message['text'] = 'Такого пути не сущесвует'

    except EXCEPTION as e:
        print(f'Произошла ошибка: {e}')


def choice_source_folder():
    """Метод для выбора исходной папки с файлами через кнопку выбора"""
    source_path = fd.askdirectory()
    if source_path:
        entry_source_folder.delete(0, "end")  # очистка поля для ввода исходной папки
        entry_source_folder.insert(0, source_path)  # вставка выбраного пути


def choice_target_folder():
    """Метод для выбора целевой папки с файлами через кнопку выбора"""
    target_path = fd.askdirectory()
    if target_path:
        entry_target_folder.delete(0, "end")  # очистка поля для ввода конечной папки
        entry_target_folder.insert(0, target_path)



root = Tk()
root.title("Упорядочиватель файлов")
root.minsize(width=800, height=600)

label_source_folder = Label(root, text='Укажите папку с файлами')
label_source_folder.place(x=50, y=5)

entry_source_folder = Entry(root, width=80)
entry_source_folder.place(x=40, y=25)

button_choice_source_folder = Button(text='Выбрать папку', command=choice_source_folder)
button_choice_source_folder.place(x=550, y=20)

label_target_folder = Label(root, text='Укажите папку куда положить упорядоченные файлы')
label_target_folder.place(x=50, y=55)

entry_target_folder = Entry(root, width=80)
entry_target_folder.place(x=40, y=80)

button_count_files_number = Button(text="Посчитать количество файлов", command=count_file_number)
button_count_files_number.place(x=60, y=110)

label_information_message = Label(root)
label_information_message.place(x=60, y=150)

label_error_message = Label(root)
label_error_message.place(x=60, y=190)

root.mainloop()
