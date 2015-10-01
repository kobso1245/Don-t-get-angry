from socketserver import StreamRequestHandler, TCPServer
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from time import sleep
import sys
from itertools import cycle
#members_count = 1
connected_users = []


def client(ip):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((ip, 9000))
    s.send(b'Hello')
    result = s.recv(8192)
    while not result:
        sleep(1)
        result = s.recv(8192v)
    return result


class EchoHandler(StreamRequestHandler):
    connected = []

    def handle(self):
        global connected_users
        global members_count
        print("Get connection from", self.client_address)
        connected_users.append(self.client_address)
        EchoHandler.connected.append(self.client_address)
        members_count -= 1
        msg = self.request.recv(8192)
        print(msg)
        self.request.send(bytes(str(len(EchoHandler.connected) - 1), 'utf-8'))
        self.finish()


class MainServer(StreamRequestHandler):
    done = False

    def handle(self):
        MainServer.done = True


def serve_forever__(serv):
    serv.serve_forever()


def server():
    serv = TCPServer(('', 20002), EchoHandler)
    serv.serve_forever()


def start_server_for_ips():
    serv = TCPServer(('', 20007), EchoHandler)
    ser = Thread(target=serv.serve_forever)
    ser.start()
    global members_count
    members_count = 2
    while members_count:
        sleep(1)
    serv.shutdown()


def send_updates(ip):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(ip, 9000)
    s.send(b'Update')

if __name__ == '__main__':
    done = False
    start_server_for_ips()
    for user in cycle(connected_users):
        # make a connection to the user
        changes = client(user[0])
        # let all the clients know about the new changes
        for other_user in connected_users:
            send_updates(other_user[0])
