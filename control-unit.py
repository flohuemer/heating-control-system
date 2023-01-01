from datetime import timedelta
from control import calendar, config, heating, monitor
from time import sleep
from os.path import join, exists
from shared import constants
from os import mkdir


def setup(c):
    runtime_dir = join(".", constants.RUNTIME_DIR)
    if not exists(runtime_dir):
        mkdir(runtime_dir)
    heating.setup_heating(config.calendar_rooms(c))


def loop(c):
    while True:
        try:
            rooms = config.calendar_rooms(c)
            room_heating_requests = calendar.room_heating_requests(
                config.calendar_url(c), join(".", constants.RUNTIME_DIR, config.calendar_cache_path(c)), rooms)
            direct_heating_requests = monitor.get_requests(rooms)
            requests = room_heating_requests.union(direct_heating_requests)
            monitor.update_temp(rooms)
            heating.control_heating(rooms, requests)
            sleep(60)
        except KeyboardInterrupt:
            break


def teardown(c):
    heating.cleanup()


if __name__ == "__main__":
    c = config.read_config_file(
        join(".", constants.CONFIG_DIR, "control-unit-config.json"))
    setup(c)
    loop(c)
    teardown(c)
