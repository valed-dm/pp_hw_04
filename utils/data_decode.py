def data_decode(data):
    d = data.decode().split(" ")
    method = d[0]
    file = d[1].lstrip("/?=")
    return method, file
