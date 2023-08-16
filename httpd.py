import argparse
import selectors
import socket
import threading

from handlers import on_connect, on_disconnect, on_read_handler
from utils import ports, user_input


class SocketServ:
    """Socket server with callbacks"""

    def __init__(self, port, root):
        self.port = port
        self.host = socket.gethostname()
        self.root = root
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
        if not self.on_read or not self.on_read(sel, sock, addr, root=self.root):
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


def create_workers(port, qty, root):
    workers_ports = ports(port, qty)
    print("ports in use: ", workers_ports)
    print("root document dir: ", root)
    servers = [SocketServ(port=port, root=root) for port in workers_ports]
    threads = [threading.Thread(target=serv.start_server) for serv in servers]
    for th in threads:
        th.start()
        print(f"threads {th} started")


start_port = 12121

if __name__ == "__main__":
    wks, rtd = user_input()

    parser = argparse.ArgumentParser(description="workers qty, assets root dir path")
    parser.add_argument("-w", "--wqty", action="store", type=int, default=1)
    parser.add_argument("-r", "--root", action="store", default="DOCUMENT_ROOT")
    args = parser.parse_args()

    create_workers(port=start_port, qty=wks or args.wqty, root=rtd or args.root)
