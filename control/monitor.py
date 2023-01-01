from control import config
from os.path import exists, join
from shared import constants
from datetime import datetime


def update_temp(rooms):
    for room in rooms:
        file_name = join(".", constants.RUNTIME_DIR,
                         config.room_tag(room) + constants.TEMP_EXT)
        current_temp = None
        if exists(file_name):
            with open(file_name, "r") as f:
                current_temp = f.read()
                try:
                    current_temp = float(current_temp)
                except ValueError:
                    pass
        config.set_room_current_temp(room, current_temp)


def get_requests(rooms):
    room_requests = set()
    for room in rooms:
        room_tag = config.room_tag(room)
        file_name = join(".", constants.RUNTIME_DIR,
                         room_tag + constants.REQUEST_EXT)
        if exists(file_name):
            with open(file_name, "r") as f:
                end_time = f.read()
                try:
                    end_time = float(end_time)
                except ValueError:
                    continue
                end_time = datetime.fromtimestamp(end_time)
                if datetime.now() < end_time:
                    room_requests.add(room_tag)
    return room_requests
