import os

from .find_path_to_file import find_path


def file_path(root, file):
    """Defines file path"""

    if file.endswith("/"):
        res = os.path.join(root + file + "index.html")
        if os.path.exists(res):
            return res
        return False

    fp = find_path(root, file)
    # print("fp =>", fp)
    if fp:
        res = fp
    else:
        res = os.path.join(root + file)

    # print("path =>", res)
    return res
