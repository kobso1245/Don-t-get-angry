import logging
import asyncio
from time import sleep
import websockets
def input_loop():
    name = input("Please select name: ")

@asyncio.coroutine
def get_pl_id(websocket, path):
    pl_id = "da"
    info = yield from websocket.recv()
    if 'pl_id' in info:
        #make_player
        pl_id = int(info.split(':')[1])

    print(info)


logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

ser = websockets.server.serve(get_pl_id, 'localhost', 8100)
ev_loop = asyncio.get_event_loop()
ev_loop.run_until_complete(ser)
ev_loop.run_forever()

def main():
    #get player id
    pass
