import threading

from httpd import SocketServ


def ports(port, qty):
    """Creates ports sequence"""

    ports_seq = [i for i in range(port, port + qty)]
    return ports_seq


def create_workers(port, qty):
    workers_ports = ports(port, qty)
    print(workers_ports)
    servers = [SocketServ(port) for port in workers_ports]
    threads = [threading.Thread(target=serv.start_server) for serv in servers]
    for th in threads:
        th.start()
        print(f"threads {th} started")


if __name__ == "__main__":
    start_port = 12121
    workers_qty = 1
    create_workers(port=start_port, qty=workers_qty)
