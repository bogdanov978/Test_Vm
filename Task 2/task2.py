# encoding: utf-8
import hashlib
import errno
import os
import sys


def check_sums(path, h_type, h_sum):
    if not os.path.exists(path):
        return "file not found!"

    with open(path) as f:
        content = f.read()

    if h_type == "md5":
        real_sum = hashlib.md5(content.encode('utf-8')).hexdigest()
    elif h_type == "sha1":
        real_sum = hashlib.sha1(content.encode('utf-8')).hexdigest()
    elif h_type == "sha256":
        real_sum = hashlib.sha256(content.encode('utf-8')).hexdigest()
    else:
        return "unknown hash sum type: " + h_type

    return "OK" if real_sum == h_sum else "FAIL"


if __name__ == "__main__":
    workdir = os.getcwd()
    input_file = os.path.join(workdir, "input_file.txt")  # пути по-умолчанию
    files_dir = os.path.join(workdir, "files")
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    if len(sys.argv) > 2:
        files_dir = sys.argv[2]

    if not os.path.exists(input_file):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), input_file
        )

    if not os.path.isdir(files_dir):
        raise NotADirectoryError(
            errno.ENOTDIR, os.strerror(errno.ENOTDIR), files_dir
        )

    with open(input_file) as inp_f:
        lines = inp_f.readlines()

    for line in lines:
        file, hash_type, hash_sum = line.split()
        f_path = os.path.join(files_dir, file)
        print(file, check_sums(f_path, hash_type, hash_sum))
