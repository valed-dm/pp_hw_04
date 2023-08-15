import os

from .find_path_to_file import find_path


def file_path(root, file):
    """Defines file path"""

    if file.endswith("/"):
        print("file.endswith =>", file)
        res = root + "/" + file + "index.html"
        print("res => ", res)
        if os.path.exists(res):
            return res
        return False

    fp = find_path(root, file)
    # print("fp =>", fp)
    if fp:
        res = fp
    else:
        res = root + "/" + file

    # print("path =>", res)
    print("res =>", res)
    return res
