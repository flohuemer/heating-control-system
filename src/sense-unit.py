from time import sleep
from sense.data import SenseUnitConfig
from modules import io, communication
from modules.logger import Logger
import websockets
import asyncio
import sys

SLEEP_TIME = 0.05
TIMEOUT_SLEEP_TIME = 30

logger: Logger = None

async def send(uri: str, data: str):
    async with websockets.connect(uri) as websocket:
        await websocket.send(data)


def run(config: SenseUnitConfig):
    logger.log("Start sense unit...")
    logger.log("IO pin setup...")
    io.setup()
    logger.log(f"Input pin {config.sensor_pin} configured for sensor")
    io.setup_intput_pin(config.sensor_pin)
    logger.log(f"Input pin {config.button_pin} configured for button")
    io.setup_intput_pin(config.button_pin)
    logger.log(f"Update interval set to {config.update_interval} seconds")
    interval_steps = config.update_interval // SLEEP_TIME
    i = 0
    logger.log("")
    while True:
        try:
            request = io.is_high(config.button_pin)
            if request or i == 0:
                logger.log("Update requested")
                temp = io.get_DHT22_data(config.sensor_pin)
                logger.log(f"Button state is: {request} and temp is: {temp}")
                logger.log(f"Sending data to {config.uri} for tag {config.tag}")
                data = communication.encode_data(config.tag, temp, request)
                asyncio.run(send(config.uri, data))
                i = interval_steps
                logger.log("")
            sleep(SLEEP_TIME)
            i -= 1
        except ConnectionError:
            logger.warn(
                f"Connection timed out. Will retry after {TIMEOUT_SLEEP_TIME} seconds")
            sleep(TIMEOUT_SLEEP_TIME)
        except KeyboardInterrupt:
            logger.warn("User interrupted system")
            break
    logger.log("Clean up system")
    io.cleanup()


def main(argv):
    global logger
    if len(argv) != 2:
        print("Expected config file path as argument")
        exit(1)
    config = SenseUnitConfig.from_file(argv[1])
    logger = Logger(config.log_file)
    run(config)


if __name__ == "__main__":
    main(sys.argv)
