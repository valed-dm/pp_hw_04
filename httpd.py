import selectors
import socket

HOST = socket.gethostname()
PORT = 12121


def on_connect(sock, addr):
    # print("Connected by", addr)
    pass


def on_disconnect(sock, addr):
    # print("Disconnected by", addr)
    pass


def on_read_handler(sel, sock, addr):
    try:
        data = sock.recv(1024)  # Should be ready
    except ConnectionError:
        print(f"Client suddenly closed while receiving")
        return False
    if not data:
        print("Disconnected by", addr)
        return False
    try:
        sock.send(bytes("HTTP/1.0 200 OK\r\n", "utf-8"))
        sock.send(bytes("Content-Type: text/html\r\n\r\n", "utf-8"))
        sock.send(bytes(f"Content-Length: {len(data)}\r\n\r\n", "utf-8"))
        sock.send(data)  # Hope it won't block
        sock.close()
        sel.unregister(sock)
        # print(f"Send: {data} to: {addr}")
    except ConnectionError:
        print(f"Client suddenly closed, cannot send")
        return False
    return True


def run_server(host, port, on_conn, on_read, on_disconn):
    def on_accept_ready(sel, serv_sock, mask):
        sock, addr = serv_sock.accept()  # Should be ready
        # sock.setblocking(False)
        sel.register(sock, selectors.EVENT_READ, on_read_ready)
        if on_conn:
            on_conn(sock, addr)

    def on_read_ready(sel, sock, mask):
        # try:
        addr = sock.getpeername()
        # except OSError:
        #     addr = None
        if not on_read or not on_read(sel, sock, addr):
            if on_disconn:
                on_disconn(sock, addr)
            sel.unregister(sock)
            sock.close()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.bind((host, port))
        serv_sock.listen(1)
        # sock.setblocking(False)
        sel = selectors.DefaultSelector()
        sel.register(serv_sock, selectors.EVENT_READ, on_accept_ready)
        while True:
            # print("Waiting for connections or data...")
            events = sel.select()
            for key, mask in events:
                callback = key.data
                callback(sel, key.fileobj, mask)


if __name__ == "__main__":
    run_server(HOST, PORT, on_connect, on_read_handler, on_disconnect)
