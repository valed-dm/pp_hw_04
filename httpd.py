import selectors
import socket
import threading

from handlers import on_connect, on_disconnect, on_read_handler
from utils import ports


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


def create_workers(port, qty):
    workers_ports = ports(port, qty)
    print(workers_ports)
    servers = [SocketServ(port) for port in workers_ports]
    threads = [threading.Thread(target=serv.start_server) for serv in servers]
    for th in threads:
        th.start()
        print(f"threads {th} started")


start_port = 12121
workers_qty = 1

if __name__ == "__main__":
    create_workers(port=start_port, qty=workers_qty)
