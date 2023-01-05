from os.path import exists, join
from datetime import datetime
from abc import abstractmethod
from modules.logger import Logger
from modules import files


class MonitorRoom():
    @abstractmethod
    def get_tag(self) -> str: pass

    @abstractmethod
    def set_current_temp(self, value) -> None: pass


def update_temp(rooms: list[MonitorRoom], logger: Logger):
    for room in rooms:
        room_tag = room.get_tag()
        logger.log(f"Monitor: Reading temperature data for room {room_tag}")
        current_temp = files.read_runtime_file(
            room_tag + files.TEMPERATURE_EXT)
        if current_temp is None:
            logger.log("Monitor: No temperature data found")
        else:
            try:
                current_temp = float(current_temp)
            except ValueError:
                logger.warn("Monitor: Unable to parse temperature data")
                pass
        logger.log(f"Monitor: Current temperature: {current_temp}")
        room.set_current_temp(current_temp)
        logger.log("Monitor:")


def get_requests(rooms: list[MonitorRoom], logger: Logger):
    room_requests = set()
    for room in rooms:
        room_tag = room.get_tag()
        logger.log(f"Monitor: Reading requests for room {room_tag}")
        end_time = files.read_runtime_file(room_tag + files.REQUEST_EXT)
        if end_time is None:
            logger.log("Monitor: No requests found")
            continue
        try:
            end_time = float(end_time)
        except ValueError:
            logger.warn("Monitor: Unable to parse request data")
            continue
        end_time = datetime.fromtimestamp(end_time)
        if datetime.now() < end_time:
            logger.log(f"Monitor: Request will end at: {end_time}")
            room_requests.add(room_tag)
    return room_requests
