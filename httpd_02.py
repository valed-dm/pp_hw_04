import select
import socket

HOST, PORT = "", 12121


def handle(sock, addr):
    try:
        data = sock.recv(1024).decode()  # Should be ready
        print(f"Received {data[:5]}from: {addr}")
    except ConnectionError:
        print(f"Client suddenly closed while receiving")
        return False
    if not data:
        print("Disconnected by", addr)
        return False
    data = data.upper()
    try:
        sock.send(bytes(data, "utf-8"))  # Hope it won't block
        print(f"Send: {data[:5]}to: {addr}")
    except ConnectionError:
        print(f"Client suddenly closed, cannot send")
        return False
    return True


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.bind((HOST, PORT))
        serv_sock.listen(1)
        # serv_sock.setblocking(False)
        inputs = [serv_sock]
        outputs = []
        while True:
            print("Waiting for connections or data...")
            readable, writeable, exceptional = select.select(inputs, outputs, inputs)
            for sock in readable:
                if sock == serv_sock:
                    sock, addr = serv_sock.accept()  # Should be ready
                    print("Connected by", addr)
                    # sock.setblocking(False)
                    inputs.append(sock)
                # else:
                #     addr = sock.getpeername()

                if not handle(sock, addr):
                    # Disconnected
                    inputs.remove(sock)
                    if sock in outputs:
                        outputs.remove(sock)
                    sock.close()
                    continue
