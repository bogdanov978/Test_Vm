# encoding: utf-8
from lxml import etree
import errno
import os
from shutil import copy
import sys


def copy_files(cnf_file):
    if not os.path.exists(cnf_file):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), cnf_file
        )

    with open(cnf_file) as f:
        xml = f.read()

    try:
        root = etree.fromstring(xml)
    except etree.XMLSyntaxError as e:
        print("cant parse xml file:", e)
        return

    paths = {}  # словарь используется для хранения путей для очередного файла
    for cur_file in root.getchildren():  # проход по файлам
        for attr in cur_file.items():  # получения списка из 3-х аттрибутов, представленных кортежами (имя, значение)
            paths[attr[0]] = attr[1]

        path_to_file = os.path.join(paths['source_path'], paths['file_name'])  # конструирует путь в зависимости от ОС
        if os.path.exists(path_to_file):
            try:
                copy(path_to_file, paths["destination_path"])
                print("file", path_to_file, "was copied to", paths["destination_path"])
            except PermissionError as e:
                print("cant copy file:", e)
        else:
            print("file", path_to_file, "not found!")


if __name__ == "__main__":
    cfg_filepath = os.path.join(os.getcwd(), "config_file.xml")  # по-умолчанию используется файл из папки с task1.py
    if len(sys.argv) > 1:
        cfg_filepath = sys.argv[1]

    copy_files(cfg_filepath)
