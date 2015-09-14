from os import system
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory, WebSocketServerFactory, \
    WebSocketServerProtocol
from logic_server import server_side

class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")

        def hello():
            self.sendMessage(u"Hello, world!".encode('utf8'))
            self.sendMessage(b"\x00\x01\x03\x04", isBinary=True)
            self.factory.reactor.callLater(1, hello)
        self.sendClose()

        # start sending messages every second ..
        #hello()

    def onMessage(self, payload, isBinary):
        pass

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        self.factory.reactor.stop()

from time import sleep
if __name__ == '__main__':

    import sys
    from time import sleep
    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory(u"ws://127.0.0.1:9000", debug=False)
    factory.protocol = MyClientProtocol

    reactor.connectTCP("127.0.0.1", 9000, factory)
    reactor.run()
    system('python logic_server2.py')

