import os
import shutil
from datetime import time
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb


class FileOrdering:

    def __init__(self, in_folder, out_folder):
        self.in_folder = in_folder
        self.out_folder = out_folder

    def run(self):
        count = 0
        for dirpath, dirnames, filenames in os.walk(self.in_folder):
            for file_name in filenames:
                count += 1
                print(file_name)  # TODO выводить в label
                file_path = os.path.join(dirpath, file_name)
                file_modify_time = time.gmtime(os.path.getmtime(file_path))

                file_modify_year = str(file_modify_time.tm_year)
                if file_modify_time.tm_mon < 10:
                    file_modify_month = '0' + str(file_modify_time.tm_mon)
                else:
                    file_modify_month = str(file_modify_time.tm_mon)
                file_modify_day = str(file_modify_time.tm_mday)

                file_year_month_target_path = os.path.join(self.out_folder, file_modify_year, file_modify_month, file_modify_day)

                if os.path.exists(file_year_month_target_path):
                    directory_to_copy = file_year_month_target_path
                    shutil.copy2(src=file_path, dst=directory_to_copy)
                else:
                    new_directory = file_year_month_target_path
                    os.makedirs(name=new_directory, exist_ok=True)
                    shutil.copy2(src=file_path, dst=new_directory)


def clear_text():
    answer = mb.askyesno(title="Вопрос", message="Очистить текстовое поле?")
    if answer == True:
        text.delete(1.0, END)


def count_file_number():
    try:
        folder_path = entry_source_folder.get()
        folder_path = os.path.normpath(folder_path)
        if os.path.exists(folder_path) and folder_path != '.':
            label_error_message['text'] = 'Такой путь сущестует'  # TODO Удалить после отладки
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


def arrange_files():
    """Главная функция для вызова упорядочивания файлов"""
    started_at = time.time()

    # TODO здесь вызов упорядочивания файлов

    ended_at = time.time()
    elapsed = round(ended_at - started_at, 4)  # TODO вывести время выполнения в Label


# TODO обернуть всё в main, после окончания разработки
# def main():

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


# Вызывать в main
# if __name__ == '__main__':
#     main()