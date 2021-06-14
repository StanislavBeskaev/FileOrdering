import os
import datetime
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
    Y_FILTER_DATE = 170
    Y_BUTTON_START = 220
    Y_FILE_COUNT_LABEL = 270
    Y_INFORMATION_LABEL = 300
    Y_ERROR_MESSAGE = 330
    DATE_FORMAT = '%d.%m.%Y'

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

        self.button_choice_source_folder = Button(self.root, text='Выбрать исходную папку',
                                                  command=self.choice_source_folder)
        self.button_choice_source_folder.place(x=550, y=self.Y_SOURCE_PATH - 5)

        self.label_target_folder = Label(self.root, text='Укажите папку куда положить упорядоченные файлы')
        self.label_target_folder.place(x=50, y=self.Y_TARGET_PATH - 25)
        self.entry_target_folder = Entry(self.root, width=80)
        self.entry_target_folder.place(x=40, y=self.Y_TARGET_PATH)
        self.label_target_folder_error = Label(self.root, fg='red')
        self.label_target_folder_error.place(x=50, y=self.Y_TARGET_PATH + 20)

        self.button_choice_source_folder = Button(self.root, text='Выбрать целевую папку',
                                                  command=self.choice_target_folder)
        self.button_choice_source_folder.place(x=550, y=self.Y_TARGET_PATH - 5)

        self.label_date_filter = Label(self.root, text='Дата, с которой брать файлы для упорядочивания. В формате '
                                                       'дд.мм.гггг ; необязательный фильтр')
        self.label_date_filter.place(x=50, y=self.Y_FILTER_DATE - 25)
        self.entry_filter_date = Entry(self.root, width=80)
        self.entry_filter_date.place(x=40, y=self.Y_FILTER_DATE)
        self.label_date_filter_error = Label(self.root, fg='red')
        self.label_date_filter_error.place(x=50, y=self.Y_FILTER_DATE + 20)

        self.button_start = Button(self.root, text="Упорядочить", command=self.preparatory_actions)
        self.button_start.place(x=50, y=self.Y_BUTTON_START)

        self.button_stop = Button(self.root, text="Остановить", command=self.stop_ordering, fg='red')

        self.label_source_file_count = Label(self.root)
        self.label_source_file_count.place(x=60, y=self.Y_FILE_COUNT_LABEL)

        self.label_information_text = Label(self.root)
        self.label_information_text.place(x=60, y=self.Y_INFORMATION_LABEL)

        self.label_error_message = Label(self.root, fg='red')
        self.label_error_message.place(x=60, y=self.Y_ERROR_MESSAGE)

        self.files_processed_number = 0

        self.user_ordering_break = False  # принудительная остановка упорядочивания файлов

        self.root.mainloop()

    def stop_ordering(self):
        """Метод для остановки упорядочивания файлов"""
        self.user_ordering_break = True

    def file_ordering(self, in_folder, out_folder, filter_date=None):
        """
        Метод упорядочивания файлов. Берёт файлы из in_folder и перекладывает их out_folder в подпапку Год/Месяц/день
        :param in_folder: Папка откуда надо взять файлы
        :param out_folder: Папка куда нужно переложить файлы и упорядочить по годам/ месяцам/ датам
        :param filter_date: Дата, с которой отбираются файлы для сортировки( по дате изменения файла).
        По умолчанию None
        :return:
        """
        self.files_processed_number = 0
        for dirpath, dirnames, filenames in os.walk(in_folder):
            for file_name in filenames:
                if self.user_ordering_break:  # если была нажата кнопка "Остановить", то прекращаем выполнение потока
                    return
                file_path = os.path.join(dirpath, file_name)
                file_modify_time = time.gmtime(os.path.getmtime(file_path))
                file_modify_date = datetime.datetime.fromtimestamp(time.mktime(file_modify_time))
                if filter_date and file_modify_date < filter_date:
                    continue

                file_modify_year = str(file_modify_time.tm_year)
                if file_modify_time.tm_mon < 10:
                    file_modify_month = '0' + str(file_modify_time.tm_mon)
                else:
                    file_modify_month = str(file_modify_time.tm_mon)
                file_modify_day = str(file_modify_time.tm_mday)

                file_year_month_target_path = os.path.join(out_folder, file_modify_year, file_modify_month,
                                                           file_modify_day)

                if os.path.exists(file_year_month_target_path):
                    directory_to_copy = file_year_month_target_path
                    shutil.copy2(src=file_path, dst=directory_to_copy)
                else:
                    new_directory = file_year_month_target_path
                    os.makedirs(name=new_directory, exist_ok=True)
                    shutil.copy2(src=file_path, dst=new_directory)
                self.files_processed_number += 1

    def count_file_number(self, path, filter_date):
        """Метод для подсчёта количества файлов в папке. Отображает количество файлов в self.label_source_file_count"""
        count_files = 0
        self.label_source_file_count['text'] = 'Идёт подсчёт количества файлов'
        for dirpath, dirnames, filenames in os.walk(path):
            for file_name in filenames:
                file_path = os.path.join(dirpath, file_name)
                file_modify_time = time.gmtime(os.path.getmtime(file_path))
                file_modify_date = datetime.datetime.fromtimestamp(time.mktime(file_modify_time))
                if filter_date and file_modify_date < filter_date:
                    continue
                count_files += 1

        self.label_source_file_count['text'] = f'{count_files} файлов для упорядочивания'
        filter_date = self.entry_filter_date.get()
        if self.entry_filter_date.get():
            self.label_source_file_count['text'] += f', с даты {filter_date}'

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

    def start_arrange_files(self, source_folder, target_folder, filter_date):
        """Главный метод для вызова упорядочивания файлов, также засекает время начало работы"""
        self.started_at = time.time()

        # упорядочивание файлов запускается в отдельном потоке, что бы не блокировать окно программы
        file_ordering_thread = threading.Thread(target=self.file_ordering, args=(source_folder, target_folder,
                                                                                 filter_date))
        file_ordering_thread.start()
        self.check_file_ordering_thread(file_ordering_thread)

    def check_file_ordering_thread(self, thread):
        """Метод, проверяет работает ли поток по упорядочиванию файлов и обновляет счётчик обработанных файлов.
        По окончанию работы потока, выводится информация в self.label_information_text и потребовавшееся время"""
        if thread.is_alive():
            current_ordering_duration = round(time.time() - self.started_at, 2)
            self.label_information_text[
                'text'] = f'Упорядочивание файлов в процессе, прошло {current_ordering_duration} сек,' \
                          f' обработано {self.files_processed_number} файлов'
            self.label_information_text.after(100, lambda: self.check_file_ordering_thread(thread))
        elif not thread.is_alive() and self.user_ordering_break:
            self.ended_at = time.time()
            elapsed = round(self.ended_at - self.started_at, 2)
            self.label_information_text['text'] = f'Прервано. упорядочивание работало {elapsed} секунд,' \
                                                  f' упорядочило {self.files_processed_number} файлов'
            self.label_error_message['text'] = 'Прервано пользователем'
            self.button_stop.place_forget()
        else:
            self.ended_at = time.time()
            elapsed = round(self.ended_at - self.started_at, 4)
            self.label_information_text['text'] = f'Упорядочивание файлов выполнено. Заняло {elapsed} секунд'
            self.button_stop.place_forget()

    def check_source_target_paths(self) -> bool:
        """
        Метод проверяет корректность введённых путей
        :return: Корректность введённых путей(True/False)
        """
        self.label_error_message['text'] = ''
        is_correct_paths = True
        source_folder = self.entry_source_folder.get()
        is_correct_paths = True
        if not os.path.exists(source_folder):
            self.label_source_folder_error['text'] = 'Исходной папки не существует! Проверьте правильность ввода.'
            is_correct_paths = False

        target_folder = self.entry_target_folder.get()

        # Если указан не абсолютный путь к целевой папке, то это некорректный путь
        if os.path.normpath(target_folder) != os.path.abspath(target_folder):
            is_correct_paths = False
            self.label_target_folder_error['text'] = 'Неккоретный путь!'

        if not os.path.exists(target_folder) and is_correct_paths:
            answer = mb.askyesno(title="Создать целевую папку?", message="Целевой папки нет, создать?")
            if answer:
                try:
                    os.makedirs(name=target_folder)
                except Exception as e:
                    is_correct_paths = False
                    self.label_target_folder_error['text'] = f' Ошибка при создание целевой папки! {e.args} '
            else:
                self.label_target_folder_error['text'] = 'Целевой папки не существует!'
                is_correct_paths = False
        return is_correct_paths

    def preparatory_actions(self):
        """Метод проверяет готовность к запуску, и запускает упорядочивание файлов если проверки выполнены"""
        is_correct_paths = self.check_source_target_paths()
        is_correct_filter_date = self.check_filter_date()
        if is_correct_paths and is_correct_filter_date:
            source_folder = self.entry_source_folder.get()
            target_folder = self.entry_target_folder.get()
            filter_date = self.entry_filter_date.get()
            if filter_date:
                filter_date = datetime.datetime.strptime(filter_date, self.DATE_FORMAT)
            self.clear_information_label_text()
            self.user_ordering_break = False
            self.button_stop.place(x=200, y=self.Y_BUTTON_START)
            self.count_file_number(source_folder, filter_date)
            self.start_arrange_files(source_folder=source_folder, target_folder=target_folder,
                                     filter_date=filter_date)
        else:
            self.label_error_message['text'] += 'Исправьте ошибки'

    def check_filter_date(self) -> bool:
        """Функция для проверки корректности заполненности фильтрующей даты"""
        filter_date = self.entry_filter_date.get()
        if not filter_date:
            return True

        try:
            datetime_filter_date = datetime.datetime.strptime(filter_date, self.DATE_FORMAT)
            return True
        except ValueError:
            self.label_date_filter_error['text'] = f'Дата не в формате {self.DATE_FORMAT}'
            return False

    def clear_information_label_text(self):
        """
        Метод очистки информационных сообщений и сообщений об ошибках
        :return:
        """
        self.label_source_folder_error['text'] = ''
        self.label_target_folder_error['text'] = ''
        self.label_error_message['text'] = ''
        self.label_information_text['text'] = ''
        self.label_date_filter_error['text'] = ''


def main():
    file_ordering_window = FileOrderingWindow()


if __name__ == '__main__':
    main()
