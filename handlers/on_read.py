from utils import time_now_rfc_1123, data_decode, c_type
from .on_file import on_file


def on_read_handler(sel, sock, addr, root):
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

    # prevents server down when browser asks for favicon.ico
    if file == "favicon.ico":
        sock.send(bytes("HTTP/1.1 200 OK\r\n", "utf-8"))
        return False
    response, fp, file_size, file_exists = on_file(root, file)
    content_type = c_type(fp)

    with open(fp, "rb") as f:
        try:
            if method == "GET":
                sock.send(bytes(response, "utf-8"))
                sock.send(bytes(f"Date: {now}\r\n", "utf-8"))
                sock.send(bytes("Server: socket/1.0\r\n", "utf-8"))
                sock.send(bytes(f"Content-Length: {file_size}\r\n", "utf-8"))
                sock.send(bytes(f"Content-Type: {content_type}\r\n", "utf-8"))
                sock.send(bytes("Connection: close\r\n\r\n", "utf-8"))
                sock.send(bytes(f.read()))
            elif method == "HEAD" and file_exists:
                sock.send(bytes("HTTP/1.1 204 OK\r\n", "utf-8"))
                sock.send(bytes(f"Content-Length: {file_size}\r\n\r\n", "utf-8"))
            elif method == "HEAD" and not file_exists:
                sock.send(bytes(response, "utf-8"))
                sock.send(bytes(f"Content-Length: {file_size}\r\n\r\n", "utf-8"))
            else:
                sock.send(bytes("HTTP/1.1 405 Not Allowed\r\n", "utf-8"))
                sock.send(bytes("Content-Type: text/html\r\n\r\n", "utf-8"))
        except ConnectionError:
            print("Client suddenly closed, cannot send")
            return False
        finally:
            sock.close()
            sel.unregister(sock)
        return True
