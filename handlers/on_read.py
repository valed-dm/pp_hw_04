from utils import time_now_rfc_1123, data_decode


def on_read_handler(sel, sock, addr):
    try:
        data = sock.recv(1024)  # Should be ready
    except ConnectionError:
        print("Client suddenly closed while receiving")
        return False
    if not data:
        print("Disconnected by", addr)
        return False

    now = time_now_rfc_1123()
    method, file = data_decode(data)
    print("method ===>", method, "file ===>", file)

    try:
        if method == "GET":
            sock.send(bytes("HTTP/1.1 200 OK\r\n", "utf-8"))
            sock.send(bytes(f"Date: {now}\r\n", "utf-8"))
            sock.send(bytes("Server: socket/1.0\r\n\r\n", "utf-8"))
            sock.send(bytes(f"Content-Length: {len(data)}\r\n", "utf-8"))
            sock.send(bytes("Content-Type: text/html\r\n\r\n", "utf-8"))
            sock.send(bytes("Connection: close\r\n\r\n", "utf-8"))
            sock.send(data)
        elif method == "HEAD":
            sock.send(bytes("HTTP/1.1 204 OK\r\n", "utf-8"))
            sock.send(bytes(f"Content-Length: {len(data)}\r\n\r\n", "utf-8"))
        else:
            sock.send(bytes("HTTP/1.1 405 Not Allowed\r\n", "utf-8"))
            sock.send(bytes("Content-Type: text/html\r\n\r\n", "utf-8"))

    except ConnectionError:
        print("Client suddenly closed, cannot send")
        sock.close()
        sel.unregister(sock)
        return False

    sock.close()
    sel.unregister(sock)
    return True
