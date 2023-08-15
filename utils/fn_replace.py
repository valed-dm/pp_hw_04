def fn_replace(fplist, fn_old, fn_new):
    fplist.remove(fn_old)
    fplist.append(fn_new)
    file = "/".join(fplist)

    return file
