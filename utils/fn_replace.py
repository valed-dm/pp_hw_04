"""Converts urlencoded filepath to string"""


def fn_replace(fplist, fn_old, fn_new):
    """Helps convert urlencoded filepath to string"""

    fplist.remove(fn_old)
    fplist.append(fn_new)
    file = "/".join(fplist)

    return file
