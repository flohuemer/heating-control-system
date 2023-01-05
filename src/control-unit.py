from time import sleep
from control.data import ControlUnitConfig
from modules import monitor, heating, calendar, io
from modules.logger import Logger
import sys

logger: Logger = None


def run(config: ControlUnitConfig):
    logger.log("Start control unit...")
    heating.setup_heating(config.rooms, logger)
    url = config.calendar.url
    cache_file = config.calendar.cache_file
    rooms = config.rooms
    logger.log(f"Communicating with calendar url {url}.")
    logger.log(f"Managing {len(rooms)} rooms.")
    while True:
        try:
            room_hr = calendar.room_heating_requests(
                url, cache_file, rooms, logger)
            direct_hr = monitor.get_requests(rooms, logger)
            requests = room_hr.union(direct_hr)
            monitor.update_temp(rooms, logger)
            heating.control_heating(rooms, requests, logger)
            sleep(config.calendar.update_interval)
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
    config = ControlUnitConfig.from_file(argv[1])
    logger = Logger(config.log_file)
    run(config)


if __name__ == "__main__":
    main(sys.argv)
