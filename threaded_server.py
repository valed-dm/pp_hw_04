import json
import logging
import socket
import threading

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname).1s %(message)s",
    datefmt="%Y.%m.%d %H:%M:%S",
)


class ThreadedServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        logging.info("server listens on port %d", port_num)
        while True:
            client, address = self.sock.accept()
            # print("client, address ===>", client, address)
            client.settimeout(60)
            t = threading.Thread(target=self.listenToClient, args=(client, address))
            t.start()

    @staticmethod
    def listenToClient(client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the received data
                    d = data.decode().split(" ")
                    print(d)
                    response = json.dumps(d)
                    print(len(response))
                    if d[0] == "GET":
                        client.send(bytes("HTTP/1.0 200 OK\r\n", "utf-8"))
                        client.send(bytes("Content-Type: text/html\r\n\r\n", "utf-8"))
                        client.send(bytes(f"Content-Length: {len(response)}\r\n\r\n", "utf-8"))
                        client.send(bytes(response, "utf-8"))
                        client.close()
                    elif d[0] == "HEAD":
                        client.send(bytes("HTTP/1.0 200 OK\r\n", "utf-8"))
                        client.send(bytes(f"Content-Length: {len(response)}\r\n\r\n", "utf-8"))
                        client.close()
                    else:
                        client.send(bytes("HTTP/1.0 405 Method Not Allowed\r\n\r\n", "utf-8"))
                        client.close()
                else:
                    raise TimeoutError("Client disconnected")

            except (OSError, TimeoutError):
                client.close()
                return False


if __name__ == "__main__":
    host_name = socket.gethostname()
    port_num = 12121

    try:
        logging.info(f"host={host_name}, port={port_num}")
        ThreadedServer(host_name, port_num).listen()
    except socket.error as e:
        logging.error("socket.error", exc_info=e)
