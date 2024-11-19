import os
import sys
import shutil


def create():

    path: str = os.path.split(sys.argv[0])[0]
    path_file: str = f'{path}/data_file'
    name_folder: list[str] = ['uriczor']

    for folder in name_folder:

        path_folders: str = f'{path}/{folder}'

        for root, dirs, files in os.walk(path_file):
            for file in files:
                if os.path.exists(path_folders):
                    if os.path.exists(f'{path_folders}/{file}'):
                        print('Файлы существуют')
                    shutil.copy(f'{root}/{file}', f'{path_folders}/')

                else:
                    os.mkdir(path_folders)
                    shutil.copy(f'{root}/{file}', f'{path_folders}/')


if __name__ == '__main__':
    create()

