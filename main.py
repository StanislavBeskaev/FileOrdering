import os
import shutil
import time
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
                count += 1
                label_information_text['text'] = f'Обработано {count} файлов'


def count_file_number(path):
    count_files = 0
    label_source_file_count['text'] = 'Идёт подсчёт количества файлов'
    for dirpath, dirnames, filenames in os.walk(path):
        for file_name in filenames:
            count_files += 1

    label_source_file_count['text'] = f'В этой папке {count_files} файлов'


def choice_source_folder():
    """Метод для выбора исходной папки с файлами через кнопку выбора"""
    source_path = fd.askdirectory(title='Выбрать исходную папку')
    if source_path:
        entry_source_folder.delete(0, "end")  # очистка поля для ввода исходной папки
        source_path = os.path.normpath(source_path)
        entry_source_folder.insert(0, source_path)  # вставка выбраного пути


def choice_target_folder():
    """Метод для выбора целевой папки с файлами через кнопку выбора"""
    target_path = fd.askdirectory(title='Выбрать целевую папку')
    if target_path:
        target_path = os.path.normpath(target_path)
        entry_target_folder.delete(0, "end")  # очистка поля для ввода конечной папки
        entry_target_folder.insert(0, target_path)


def arrange_files(source_folder, target_folder):
    """Главная функция для вызова упорядочивания файлов"""
    started_at = time.time()

    file_ordering = FileOrdering(in_folder=source_folder, out_folder=target_folder)
    file_ordering.run()

    ended_at = time.time()
    elapsed = round(ended_at - started_at, 4)
    label_information_text['text'] += f'. Упорядочивание файлов выполнено. Заняло {elapsed} секунд'


def preparatory_actions():
    """Метод для проверки корректности введёных путей"""
    label_error_message['text'] = ''
    source_folder = entry_source_folder.get()
    flag_start_opportunity = True
    if not os.path.exists(source_folder):
        label_error_message['text'] += 'Исходной папки не существует! Проверьте правильность ввода.'
        flag_start_opportunity = False

    target_folder = entry_target_folder.get()
    if not os.path.exists(target_folder):
        answer = mb.askyesno(title="Создать целевую папку?", message="Целевой папки нет, создать?")
        if answer:
            try:
                os.makedirs(name=target_folder)
            except Exception as e:
                label_error_message['text'] += f' Ошибка при создание целевой папки! {e.args} '
        else:
            label_error_message['text'] += ' Целевой папки не существует!'
            flag_start_opportunity = False

    if flag_start_opportunity:
        count_file_number(source_folder)
        arrange_files(source_folder=source_folder, target_folder=target_folder)
        # TODO при работе FileOrdering зависает окно, подумать что бы окно не зависало



# TODO обернуть всё в main, после окончания разработки
# def main():

root = Tk()
root.title("Упорядочиватель файлов")
root.minsize(width=800, height=600)

label_source_folder = Label(root, text='Укажите папку с файлами')
label_source_folder.place(x=50, y=5)

entry_source_folder = Entry(root, width=80)
entry_source_folder.place(x=40, y=25)

button_choice_source_folder = Button(text='Выбрать исходную папку', command=choice_source_folder)
button_choice_source_folder.place(x=550, y=20)

label_target_folder = Label(root, text='Укажите папку куда положить упорядоченные файлы')
label_target_folder.place(x=50, y=55)

entry_target_folder = Entry(root, width=80)
entry_target_folder.place(x=40, y=80)

button_choice_source_folder = Button(text='Выбрать целевую папку', command=choice_target_folder)
button_choice_source_folder.place(x=550, y=75)

button_start = Button(text="Упорядочить", command=preparatory_actions)
button_start.place(x=50, y=115)

label_source_file_count = Label(root)
label_source_file_count.place(x=60, y=160)

label_information_text = Label(root)
label_information_text.place(x=60, y=180)

label_error_message = Label(root)
label_error_message.place(x=60, y=200)

root.mainloop()


# Вызывать в main
# if __name__ == '__main__':
#     main()