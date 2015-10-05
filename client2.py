import asyncio
import websockets


def input_loop():
    name = input("Please select name: ")


@asyncio.coroutine
def get_pl_id(websocket, path):
    pl_id = yield from websocket.recv()
    print(pl_id)

start_Server = websockets.serve(get_pl_id, 'localhost', 8101)
ev_loop = asyncio.get_event_loop()
ev_loop.run_until_complete(start_Server)
ev_loop.run_forever()


def main():
    # get player id
    pass
