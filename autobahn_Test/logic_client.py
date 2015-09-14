from json import load, dump
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketClientFactory
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketClientProtocol
# or: from autobahn.asyncio.websocket import WebSocketServerProtocol

class GetUsers(WebSocketServerProtocol):
    USERS = []
    TIMER = None
    USERS_NUMBER = 0

    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))
        if request.peer not in GetUsers.USERS:
            GetUsers.USERS.append(request.peer)

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        pass

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))
        if len(GetUsers.USERS) == GetUsers.USERS_NUMBER:
            def edit_user_ip(user_ips):
                return [user.split(':')[-2] for user in user_ips]
            GetUsers.USERS = edit_user_ip(GetUsers.USERS)
            self.factory.reactor.stop()


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
    with open('settings.json') as settings:
        loaded_file = load(settings)
        fact.USERS_NUMBER = loaded_file['users_count']

def save_users_count(file_name, users_count):
    curr_fle = None
    with open(file_name, 'r') as settings:
        curr_fle = load(settings)
        curr_fle['users_count'] = users_count
    with open(file_name, 'w') as settings:
        dump(curr_fle, settings)




if __name__ == '__main__':
    factory = WebSocketServerFactory()
    factory.protocol = GetUsers
    users_cnt = int(input("Please insert number of users: "))
    save_users_count('settings.json', users_cnt)
    get_users_count(factory.protocol)
    reactor.listenTCP(9000, factory)
    reactor.run()
    
    #current_users = factory.protocol.USERS 
    #curr_user = 0
    #while True:
        #connect to the current user
        #factory = WebSocketClientFactory(u"ws://" + current_users[curr_user]+ ":9002", debug = False)
        #factory.protocol = ClientConnector
        #reactor.connectTCP(current_users[curr_user], 9002, factory)
        #reactor.run()
        #curr_user = (curr_user + 1) % len(current_users)

