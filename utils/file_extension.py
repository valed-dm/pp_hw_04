import os


def f_ext(path):
    file, ext = os.path.splitext(path)
    return ext
