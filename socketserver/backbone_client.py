from socketserver import StreamRequestHandler, TCPServer
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from time import sleep
members_count = 1
connected_users = []


def getting_row_number():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('localhost', 20007))
    s.send(b'Hello')
    return int(s.recv(8192))


class EchoHandler(StreamRequestHandler):

    def handle(self):
        global connected_users
        global members_count
        print("Get connection from", self.client_address)
        connected_users.append(self.client_addres)
        members_count -= 1
        msg = self.request.recv(8192)
        print(msg)
        self.request.send(b'Banana')
        self.finish()


def server():
    serv = TCPServer(('', 9000), EchoHandler)
    serv.serve_forever()


if __name__ == '__main__':
    row = getting_row_number()
    serv = TCPServer(('', 9000), EchoHandler)
    serv_th = Thread(target=serv.serve_forever)
    serv_th.start()
