from json import load, dump
from os import system
from time import sleep
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

def save_users_ips(file_name, users_ips):
    curr_fle = None
    with open(file_name, 'r') as settings:
        curr_fle = load(settings)
        curr_fle['users_ips'] = users_ips
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
    
    current_users = factory.protocol.USERS 
    save_users_ips('settings.json', current_users)
    sleep(10)
    curr_user = 0
    to_be_called = 'python logic_client.py {}'
    while True:
        fin_to_be_called = to_be_called.format(curr_user)
        system(fin_to_be_called)
        curr_user = (curr_user + 1) % len(current_users)

