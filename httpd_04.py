import selectors
import socket


HOST, PORT = "", 12121


def handle(sock, addr):
    try:
        data = sock.recv(1024)  # Should be ready
    except ConnectionError:
        print(f"Client suddenly closed while receiving")
        return False
    print(f"Received {data} from: {addr}")
    if not data:
        print("Disconnected by", addr)
        return False
    data = data.upper()
    # print(f"Send: {data} to: {addr}")
    try:
        sock.send(bytes("HTTP/1.0 200 OK\r\n", "utf-8"))
        sock.send(bytes("Content-Type: text/html\r\n\r\n", "utf-8"))
        # sock.send(data)  # Hope it won't block
    except ConnectionError:
        print(f"Client suddenly closed, cannot send")
        return False
    return True

# def handle(sock, addr):
#     """This is on_read func"""
#
#     try:
#         data = sock.recv(1024)  # Should be ready
#     except ConnectionError:
#         print(f"Client suddenly closed while receiving")
#         return False
#     # print(f"Received {data} from: {addr}")
#     if not data:
#         print("Disconnected by", addr)
#         return False
#     data.decode()
#     # print(f"Send: {data} to: {addr}")
#     try:
#         sock.send(bytes("HTTP/1.0 200 OK\r\n", "utf-8"))
#         sock.send(bytes("Content-Type: text/html\r\n\r\n", "utf-8"))
#         sock.send(bytes(f"Content-Length: {len(data)}\r\n\r\n", "utf-8"))
#         sock.send(bytes(data))  # Hope it won't block
#         sock.close()
#         # print(f"Send: {data} to: {addr}")
#     except ConnectionError:
#         print(f"Client suddenly closed, cannot send")
#         return False
#     return True


def on_accept_ready(sel, serv_sock, mask):
    sock, addr = serv_sock.accept()  # Should be ready
    # print("Connected by", addr)
    # sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ, on_read_ready)


def on_read_ready(sel, sock, mask):
    addr = sock.getpeername()
    if not handle(sock, addr):
        sel.unregister(sock)
        sock.close()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.bind((HOST, PORT))
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
