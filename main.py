import os
import shutil
import threading
import time
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb


class FileOrderingWindow:
    """
    Класс для отображения окна для упорядочивания файлов
    """
    Y_SOURCE_PATH = 25
    Y_TARGET_PATH = 100
    Y_FILE_COUNT_LABEL = 180
    Y_INFORMATION_LABEL = 200
    Y_ERROR_MESSAGE = 220

    def __init__(self):
        self.root = Tk()
        self.root.title("Упорядочиватель файлов")
        self.root.minsize(width=800, height=600)

        self.label_source_folder = Label(self.root, text='Укажите папку откуда нужно взять файлы')
        self.label_source_folder.place(x=50, y=5)
        self.entry_source_folder = Entry(self.root, width=80)
        self.entry_source_folder.place(x=40, y=self.Y_SOURCE_PATH)
        self.label_source_folder_error = Label(self.root, fg='red')
        self.label_source_folder_error.place(x=50, y=self.Y_SOURCE_PATH + 20)

        self.button_choice_source_folder = Button(self.root, text='Выбрать исходную папку', command=self.choice_source_folder)
        self.button_choice_source_folder.place(x=550, y=self.Y_SOURCE_PATH - 5)

        self.label_target_folder = Label(self.root, text='Укажите папку куда положить упорядоченные файлы')
        self.label_target_folder.place(x=50, y=self.Y_TARGET_PATH - 25)
        self.entry_target_folder = Entry(self.root, width=80)
        self.entry_target_folder.place(x=40, y=self.Y_TARGET_PATH)
        self.label_target_folder_error = Label(self.root, fg='red')
        self.label_target_folder_error.place(x=50, y=self.Y_TARGET_PATH + 20)

        self.button_choice_source_folder = Button(self.root, text='Выбрать целевую папку', command=self.choice_target_folder)
        self.button_choice_source_folder.place(x=550, y=self.Y_TARGET_PATH - 5)

        self.button_start = Button(self.root, text="Упорядочить", command=self.preparatory_actions)
        self.button_start.place(x=50, y=self.Y_TARGET_PATH + 50)

        self.label_source_file_count = Label(self.root)
        self.label_source_file_count.place(x=60, y=self.Y_FILE_COUNT_LABEL)

        self.label_information_text = Label(self.root)
        self.label_information_text.place(x=60, y=self.Y_INFORMATION_LABEL)

        self.label_error_message = Label(self.root, fg='red')
        self.label_error_message.place(x=60, y=self.Y_ERROR_MESSAGE)

        self.files_processed_number = 0

        self.root.mainloop()

    def file_ordering(self, in_folder, out_folder):
        """
        Метод упорядочивания файлов. Берёт файлы из in_folder и перекладывает их out_folder в подпапку Год/Месяц/день
        :param in_folder: Папка откуда надо взять файлы
        :param out_folder: Папка куда нужно переложить файлы и упорядочить по годам/ месяцам/ датам
        :return:
        """
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
        """Метод для подсчёта количества файлов в папке. Отображает количество файлов в self.label_source_file_count"""
        count_files = 0
        self.label_source_file_count['text'] = 'Идёт подсчёт количества файлов'
        for dirpath, dirnames, filenames in os.walk(path):
            for file_name in filenames:
                count_files += 1

        self.label_source_file_count['text'] = f'В этой папке {count_files} файлов'

    def choice_source_folder(self):
        """Метод для выбора исходной папки с файлами через кнопку выбора исходной папки """
        source_path = fd.askdirectory(title='Выбрать исходную папку')
        if source_path:
            self.entry_source_folder.delete(0, "end")  # очистка поля для ввода исходной папки
            source_path = os.path.normpath(source_path)
            self.entry_source_folder.insert(0, source_path)  # вставка выбраного пути
            self.label_source_folder_error['text'] = ''

    def choice_target_folder(self):
        """Метод для выбора целевой папки с файлами через кнопку выбора целевой папки"""
        target_path = fd.askdirectory(title='Выбрать целевую папку')
        if target_path:
            target_path = os.path.normpath(target_path)
            self.entry_target_folder.delete(0, "end")  # очистка поля для ввода конечной папки
            self.entry_target_folder.insert(0, target_path)
            self.label_target_folder_error['text'] = ''

    def arrange_files(self, source_folder, target_folder):
        """Главный метод для вызова упорядочивания файлов, также засекает время начало работы"""
        self.started_at = time.time()

        file_ordering_thread = threading.Thread(target=self.file_ordering, args=(source_folder, target_folder))
        file_ordering_thread.start()
        self.check_file_ordering_thread(file_ordering_thread)

    def check_file_ordering_thread(self, thread):
        """Метод, проверяет работает ли поток по упорядочиванию файлов и обновляет счётчик обработанных файлов.
        По окончанию работы потока, выводится информация в self.label_information_text и потребовавшееся время"""
        if thread.is_alive():
            self.label_information_text['text'] = f'Упорядочивание файлов в процессе, обработанно {self.files_processed_number} файлов'
            self.label_information_text.after(100, lambda: self.check_file_ordering_thread(thread))

        else:
            self.ended_at = time.time()
            elapsed = round(self.ended_at - self.started_at, 4)
            self.label_information_text['text'] = f'Упорядочивание файлов выполнено. Заняло {elapsed} секунд'

    def preparatory_actions(self):
        """Метод для проверки корректности введёных путей"""
        self.label_error_message['text'] = ''
        source_folder = self.entry_source_folder.get()
        flag_start_opportunity = True
        if not os.path.exists(source_folder):
            self.label_source_folder_error['text'] = 'Исходной папки не существует! Проверьте правильность ввода.'
            flag_start_opportunity = False

        target_folder = self.entry_target_folder.get()
        if not os.path.exists(target_folder) or target_folder == '':
            answer = mb.askyesno(title="Создать целевую папку?", message="Целевой папки нет, создать?")
            if answer:
                try:
                    os.makedirs(name=target_folder)
                except Exception as e:
                    self.label_target_folder_error['text'] += f' Ошибка при создание целевой папки! {e.args} '
            else:
                self.label_target_folder_error['text'] = 'Целевой папки не существует!'
                flag_start_opportunity = False

        if flag_start_opportunity:
            self.clear_information_label_text()
            self.count_file_number(source_folder)
            self.arrange_files(source_folder=source_folder, target_folder=target_folder)
        else:
            self.label_error_message['text'] += 'Укажите корректные пути!'

    def clear_information_label_text(self):
        self.label_source_folder_error['text'] = ''
        self.label_target_folder_error['text'] = ''
        self.label_error_message['text'] = ''
        self.label_information_text['text'] = ''


def main():
    file_ordering_window = FileOrderingWindow()


if __name__ == '__main__':
    main()
