from socket import socket, AF_INET,SOCK_STREAM
s = socket(AF_INET,SOCK_STREAM)
s.connect(('localhost', 20002))
s.send(b'Hello')
print(s.recv(8192))
