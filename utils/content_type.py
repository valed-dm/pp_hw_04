"""Content type checker"""


from .file_extension import f_ext


def c_type(path):
    """Provides proper content type"""

    ct = "text/html"

    ext = f_ext(path)

    if ext == ".css":
        ct = "text/css"
    elif ext == ".js":
        ct = "text/javascript"
    elif ext in [".jpg", ".jpeg"]:
        ct = "image/jpeg"
    elif ext == ".png":
        ct = "image/png"
    elif ext == ".gif":
        ct = "image/gif"
    elif ext == ".swf":
        ct = "application/x-shockwave-flash"

    return ct
