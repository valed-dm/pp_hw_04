"""Decodes HTTP request data"""


from urllib.parse import unquote

from .fn_replace import fn_replace
from .smart_rstrip import smart_rstrip


def data_decode(data):
    """Decodes HTTP request data"""

    d = data.decode().split(" ")
    if d:
        method = d[0] if d[0] in ["GET", "HEAD"] else None
        try:
            file = d[1].lstrip("/?=")
            file = smart_rstrip(file, char="?")

            if "%" in file:
                file_split = file.split("/")
                percent_encoded = file_split[-1]
                print("percent_encoded =>", percent_encoded)

                if "." in percent_encoded:
                    space_inserted = percent_encoded.replace("%20", " ")
                    file = fn_replace(
                        fplist=file_split, fn_old=percent_encoded, fn_new=space_inserted
                    )
                    return method, file

                try:
                    decoded = unquote(percent_encoded)
                    file = fn_replace(
                        fplist=file_split, fn_old=percent_encoded, fn_new=decoded
                    )
                    return method, file
                except ValueError:
                    file = None

        except IndexError:
            file = None

        return method, file
