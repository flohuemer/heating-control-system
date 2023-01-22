from time import sleep
import websockets
import asyncio
from modules import communication

TEMPS = [(14.0, False), (14.2, False), (14.4, False), (14.6, False), (14.8, False),
         (15.0, False), (14.8, False), (14.6, False), (14.4, False), (14.6, False),
         (14.8, True), (15.0, False), (16.0, False), (17.0, False), (18.0, False),
         (19.0, False), (20.0, False), (19.6, False), (19.4, False), (19.6, False),
         (19.8, False), (20.0, False)]


async def send(uri: str, data: str):
    async with websockets.connect(uri) as websocket:
        await websocket.send(data)

def run():
    for t in TEMPS:
        temp = t[0]
        request = t[1]
        data = communication.encode_data("tag", temp, request)
        asyncio.run(send("address", data))
        sleep(10)

if __name__ == "__main__":
    run()