from socketserver import StreamRequestHandler, TCPServer
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


def client():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('localhost', 20002))
    s.send(b'Hello')


class EchoHandler(StreamRequestHandler):
    def handle(self):
        print("Get connection from", self.client_address)
        msg = self.request.recv(8192)
        print(msg)
        self.request.send(b'Banana')
        self.finish()


def server():
    serv = TCPServer(('',20002), EchoHandler)
    serv.serve_forever()


if __name__ == '__main__':
    serv = TCPServer(('',20002), EchoHandler)
    ser = Thread(target=serv.serve_forever)
    ser.start()
    client()
    serv.shutdown()
    ser.join()
