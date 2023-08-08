import selectors
import socket


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
        print("Client suddenly closed while receiving")
        return False
    if not data:
        print("Disconnected by", addr)
        return False

    method = data.decode().split(" ")[0]
    print("method ===>", method)

    try:
        if method == "GET":
            sock.send(bytes("HTTP/1.1 200 OK\r\n", "utf-8"))
            sock.send(bytes("Content-Type: text/html\r\n\r\n", "utf-8"))
            sock.send(bytes(f"Content-Length: {len(data)}\r\n\r\n", "utf-8"))
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


class SocketServ:
    """Socket server with callbacks"""

    def __init__(self, port):
        self.port = port
        self.host = socket.gethostname()
        self.on_conn = on_connect
        self.on_read = on_read_handler
        self.on_disconn = on_disconnect

    def on_accept_ready(self, sel, serv_sock, mask):
        sock, addr = serv_sock.accept()  # Should be ready
        # sock.setblocking(False)
        sel.register(sock, selectors.EVENT_READ, self.on_read_ready)
        if self.on_conn:
            self.on_conn(sock, addr)

    def on_read_ready(self, sel, sock, mask):
        # try:
        addr = sock.getpeername()
        if not self.on_read or not self.on_read(sel, sock, addr):
            if self.on_disconn:
                self.on_disconn(sock, addr)
            sel.unregister(sock)
            sock.close()

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
            serv_sock.bind((self.host, self.port))
            serv_sock.listen(1)
            # sock.setblocking(False)
            sel = selectors.DefaultSelector()
            sel.register(serv_sock, selectors.EVENT_READ, self.on_accept_ready)
            while True:
                # print(f"Waiting for connections or data on port {self.port}")
                events = sel.select()
                for key, mask in events:
                    callback = key.data
                    callback(sel, key.fileobj, mask)
