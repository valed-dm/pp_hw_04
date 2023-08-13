import os

from utils import file_path


def on_file(root, file):
    response = "HTTP/1.1 200 OK\r\n"
    file_exists = True

    fp = file_path(root, file)
    
    if os.path.exists(fp):
        print("os.path.exists(fp) =>", os.path.exists(fp))
        file_size = os.path.getsize(fp)
    else:
        response = "HTTP/1.1 404 Not Found\r\n"
        fp = os.path.join("DOCUMENT_ROOT", "404.html")
        file_size = os.path.getsize(fp)
        file_exists = False

    return response, fp, file_size, file_exists
