import socketserver
from http.server import BaseHTTPRequestHandler


def some_function():
    print("some_function got called")


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/captureImage":
            # Insert your code here
            some_function()

        self.send_response(200)


httpd = socketserver.TCPServer(("", 8080), MyHandler)

if __name__ == "__main__":
    httpd.serve_forever()
    print("server started at localhost:8080")
