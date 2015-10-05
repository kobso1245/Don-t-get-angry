
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory, WebSocketServerFactory, \
    WebSocketServerProtocol
from time import sleep
import sys
from time import sleep
from twisted.python import log
from twisted.internet import reactor


class UserServer(WebSocketServerProtocol):

    def onConnect(self, request):
        pass

    def onOpen(self):
        pass

    def onMessage(self, payload, isBinary):
        print(payload)
        # logic goes here
        sleep(5)
        self.sendMessage("Done")

    def onClose(self, wasClean, code, reason):
        pass


def server_side():
    factory = WebSocketServerFactory()
    factory.protocol = UserServer
    reactor.listenTCP(9002, factory)
    reactor.run()

if __name__ == '__main__':
    server_side()
