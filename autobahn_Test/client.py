from os import system
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory, WebSocketServerFactory, \
    WebSocketServerProtocol
from logic_server import server_side
import sys
from time import sleep
from twisted.python import log
from twisted.internet import reactor


class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        pass

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        self.factory.reactor.stop()

if __name__ == '__main__':

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory(u"ws://127.0.0.1:9000", debug=False)
    factory.protocol = MyClientProtocol

    reactor.connectTCP("127.0.0.1", 9000, factory)
    reactor.run()
    system('python logic_server.py')
