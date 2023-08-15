import os

set_once = False
new_root = ""


def set_root(root, file):
    """Sets new root dir for wikipedia_russia.html"""

    global set_once
    global new_root

    if set_once:
        file_path_split = file.split("/")
        file_name = file_path_split[-1]
        return new_root, file_name

    file_path_split = file.split("/")
    file_name = file_path_split[-1]
    if file_name == "wikipedia_russia.html":
        file_dir_ends_at = len(file_path_split) - 1
        file_dir = file_path_split[:file_dir_ends_at]
        file_dir = "/".join(file_dir)
        new_root = os.path.join(root, file_dir)
        set_once = True
        print("new root =>", new_root)
    else:
        new_root = root

    return new_root, file_name
