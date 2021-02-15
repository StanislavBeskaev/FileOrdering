# -*- coding: utf-8 -*-

import os
import shutil
import time


class FileOrdering:

    def __init__(self, in_folder, out_folder):
        self.in_folder = in_folder
        self.out_folder = out_folder

    def run(self):
        count = 0
        for dirpath, dirnames, filenames in os.walk(self.in_folder):
            for file_name in filenames:
                count += 1
                print(file_name)
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

        print(f'Скопировано {count} файлов')


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()

        result = func(*args, **kwargs)

        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'Функция работала {elapsed} секунд(ы)')
        return result
    return surrogate


@time_track
def main():
    source_foto_path = 'C:\\Users\\Станислав\\Desktop\\FileOrdering_test\\source'  # путь откуда взять фото
    source_foto_path = os.path.normpath(source_foto_path)

    target_foto_path = 'C:\\Users\\Станислав\\Desktop\\FileOrdering_test\\target'  # путь куда скопировать фото
    target_foto_path = os.path.normpath(target_foto_path)

    file_ordering = FileOrdering(in_folder=source_foto_path, out_folder=target_foto_path)
    file_ordering.run()


if __name__ == '__main__':
    main()
