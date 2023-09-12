"""Gets file extension"""


import os


def f_ext(path):
    """Gets file extension"""

    file, ext = os.path.splitext(path)
    return ext
