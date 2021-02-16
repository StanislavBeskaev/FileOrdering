import os
import shutil
import threading
import time
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb


class FileOrderingWindow:
    def __init__(self):
        self.root = Tk()
        self.root.title("Упорядочиватель файлов")
        self.root.minsize(width=800, height=600)

        self.label_source_folder = Label(self.root, text='Укажите папку с файлами')
        self.label_source_folder.place(x=50, y=5)

        self.entry_source_folder = Entry(self.root, width=80)
        self.entry_source_folder.place(x=40, y=25)

        self.button_choice_source_folder = Button(self.root, text='Выбрать исходную папку', command=self.choice_source_folder)
        self.button_choice_source_folder.place(x=550, y=20)

        self.label_target_folder = Label(self.root, text='Укажите папку куда положить упорядоченные файлы')
        self.label_target_folder.place(x=50, y=55)

        self.entry_target_folder = Entry(self.root, width=80)
        self.entry_target_folder.place(x=40, y=80)

        self.button_choice_source_folder = Button(self.root, text='Выбрать целевую папку', command=self.choice_target_folder)
        self.button_choice_source_folder.place(x=550, y=75)

        self.button_start = Button(self.root, text="Упорядочить", command=self.preparatory_actions)
        self.button_start.place(x=50, y=115)

        self.label_source_file_count = Label(self.root)
        self.label_source_file_count.place(x=60, y=160)

        self.label_information_text = Label(self.root)
        self.label_information_text.place(x=60, y=180)

        self.label_error_message = Label(self.root)
        self.label_error_message.place(x=60, y=200)

        self.files_processed_number = 0

        self.root.mainloop()

    def file_ordering(self, in_folder, out_folder):
        self.files_processed_number = 0
        for dirpath, dirnames, filenames in os.walk(in_folder):
            for file_name in filenames:
                file_path = os.path.join(dirpath, file_name)
                file_modify_time = time.gmtime(os.path.getmtime(file_path))

                file_modify_year = str(file_modify_time.tm_year)
                if file_modify_time.tm_mon < 10:
                    file_modify_month = '0' + str(file_modify_time.tm_mon)
                else:
                    file_modify_month = str(file_modify_time.tm_mon)
                file_modify_day = str(file_modify_time.tm_mday)

                file_year_month_target_path = os.path.join(out_folder, file_modify_year, file_modify_month, file_modify_day)

                if os.path.exists(file_year_month_target_path):
                    directory_to_copy = file_year_month_target_path
                    shutil.copy2(src=file_path, dst=directory_to_copy)
                else:
                    new_directory = file_year_month_target_path
                    os.makedirs(name=new_directory, exist_ok=True)
                    shutil.copy2(src=file_path, dst=new_directory)
                self.files_processed_number += 1

    def count_file_number(self, path):
        count_files = 0
        self.label_source_file_count['text'] = 'Идёт подсчёт количества файлов'
        for dirpath, dirnames, filenames in os.walk(path):
            for file_name in filenames:
                count_files += 1

        self.label_source_file_count['text'] = f'В этой папке {count_files} файлов'

    def choice_source_folder(self):
        """Метод для выбора исходной папки с файлами через кнопку выбора"""
        source_path = fd.askdirectory(title='Выбрать исходную папку')
        if source_path:
            self.entry_source_folder.delete(0, "end")  # очистка поля для ввода исходной папки
            source_path = os.path.normpath(source_path)
            self.entry_source_folder.insert(0, source_path)  # вставка выбраного пути

    def choice_target_folder(self):
        """Метод для выбора целевой папки с файлами через кнопку выбора"""
        target_path = fd.askdirectory(title='Выбрать целевую папку')
        if target_path:
            target_path = os.path.normpath(target_path)
            self.entry_target_folder.delete(0, "end")  # очистка поля для ввода конечной папки
            self.entry_target_folder.insert(0, target_path)

    def arrange_files(self, source_folder, target_folder):
        """Главная функция для вызова упорядочивания файлов"""
        started_at = time.time()

        self.file_ordering(in_folder=source_folder, out_folder=target_folder)

        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        self.label_information_text['text'] += f'. Упорядочивание файлов выполнено. Заняло {elapsed} секунд'

    def preparatory_actions(self):
        """Метод для проверки корректности введёных путей"""
        self.label_error_message['text'] = ''
        source_folder = self.entry_source_folder.get()
        flag_start_opportunity = True
        if not os.path.exists(source_folder):
            self.label_error_message['text'] += 'Исходной папки не существует! Проверьте правильность ввода.'
            flag_start_opportunity = False

        target_folder = self.entry_target_folder.get()
        if not os.path.exists(target_folder):
            answer = mb.askyesno(title="Создать целевую папку?", message="Целевой папки нет, создать?")
            if answer:
                try:
                    os.makedirs(name=target_folder)
                except Exception as e:
                    self.label_error_message['text'] += f' Ошибка при создание целевой папки! {e.args} '
            else:
                self.label_error_message['text'] += ' Целевой папки не существует!'
                flag_start_opportunity = False

        if flag_start_opportunity:
            self.count_file_number(source_folder)
            self.label_information_text['text'] = ''
            self.arrange_files(source_folder=source_folder, target_folder=target_folder)
            # TODO при работе FileOrdering зависает окно, подумать что бы окно не зависало


def main():
    file_ordering_window = FileOrderingWindow()


if __name__ == '__main__':
    main()
