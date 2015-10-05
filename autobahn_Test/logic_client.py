from json import load, dump
import sys
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketClientFactory
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketClientProtocol
# or: from autobahn.asyncio.websocket import WebSocketServerProtocol
SETTINGS_FILE = 'settings.json'


class ClientConnector(WebSocketClientProtocol):

    def onConnect(self, response):
        pass

    def onOpen(self):
        self.sendMessage(u"Hello world!".encode('utf8'))

    def onMessage(self, payload, isBinary):
        self.sendClose()

    def onClose(self, wasClean, code, reason):
        self.factory.reactor.stop()


def get_users_count(fact):
    with open(SETTINGS_FILE) as settings:
        loaded_file = load(settings)
        fact.USERS_NUMBER = loaded_file['users_count']


def save_users_count(file_name, users_count):
    curr_fle = None
    with open(file_name, 'r') as settings:
        curr_fle = load(settings)
        curr_fle['users_count'] = users_count
    with open(file_name, 'w') as settings:
        dump(curr_fle, settings)


def get_users():
    with open(SETTINGS_FILE) as settings:
        return load(settings)['users_ips']


if __name__ == '__main__':
    args = sys.argv
    curr_user = int(args[1])
    current_users = get_users()
    # connect to the current user
    factory = WebSocketClientFactory(
        u"ws://" +
        current_users[curr_user] +
        ":{}".format(
            9002 +
            curr_user),
        debug=False)
    factory.protocol = ClientConnector
    reactor.connectTCP(current_users[curr_user], 9002 + curr_user, factory)
    reactor.run()
