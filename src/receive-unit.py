from receive.data import ReceiveUnitConfig
from modules import communication, files
from modules.logger import Logger
import websockets
import asyncio
from datetime import datetime, timedelta
import sys

logger: Logger = None

async def run(websocket):
    async for message in websocket:
        tag, temp, request = communication.decode_data(message)
        logger.log(f"Received data for tag {tag}")
        logger.log(f"Temp: {temp}")
        logger.log(f"Request: {request}")
        logger.log(f"Updating temperature file...")
        files.write_runtime_file(tag + files.TEMPERATURE_EXT, temp)
        if request:
            end = datetime.now() + timedelta(hours=4)
            logger.log(f"Updating request file...")
            logger.log(f"Request will end at: {end}")
            files.write_runtime_file(tag + files.REQUEST_EXT, end.timestamp())
        logger.log("")


async def main(argv):
    global logger
    if len(argv) != 2:
        print("Expected config file path as argument")
        exit(1)
    config = ReceiveUnitConfig.from_file(argv[1])
    logger = Logger(config.log_file)
    logger.log(f"Start listening to websocket port {config.port}")
    logger.log("")
    async with websockets.serve(run, "localhost", config.port):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main(sys.argv))
