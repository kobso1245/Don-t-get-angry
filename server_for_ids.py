from time import sleep
import json
import asyncio
import websockets
def get_ips():
    host_ips = []
    with open('settings.json') as settings_file:
        host_ips = json.load(settings_file)['IPs']
    return host_ips

@asyncio.coroutine
def send_pl_id(conns):
    pl_id = 0
    for conn in conns:
        websocket = yield from websockets.connect('ws://' + conn + '/')
        yield from websocket.send("pl_id:"+str(pl_id))
        yield from websocket.close()
        pl_id += 1

conns = get_ips()
asyncio.get_event_loop().run_until_complete(send_pl_id(conns))
