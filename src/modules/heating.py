from abc import abstractmethod
from modules.logger import Logger
from modules import io

TEMP_RANGE = 0.5


class HeatingRoom():
    @abstractmethod
    def get_tag(self) -> str: pass

    @abstractmethod
    def get_control_pin(self) -> int: pass

    @abstractmethod
    def get_current_temp(self) -> float: pass

    @abstractmethod
    def get_target_temp(self) -> float: pass

    @abstractmethod
    def get_setback_temp(self) -> float: pass

    @abstractmethod
    def get_target_temp_reached(self) -> bool: pass

    @abstractmethod
    def set_target_temp_reached(self, value: bool) -> None: pass


def setup_heating(rooms: list[HeatingRoom], logger: Logger):
    logger.log(f"Heating: IO pin setup for {len(rooms)} rooms...")
    io.setup()
    for room in rooms:
        pin = room.get_control_pin()
        logger.log(
            f"Heating: Output pin {pin} set for tag {room.get_tag()}")
        io.setup_output_pin(pin)
        io.set_high(pin)
        room.set_target_temp_reached(False)

def cleanup(logger: Logger):
    logger.log(f"Heating: Clean up IO pins")
    io.cleanup()

def control_heating(rooms: list[HeatingRoom], room_heating_requests: set[str], logger: Logger):
    for room in rooms:
        logger.log(f"Heating: Controlling room {room.get_tag()}")
        if room.get_tag() in room_heating_requests:
            control_room(room, room.get_target_temp(), logger)
        else:
            control_room(room, room.get_setback_temp(), logger)
        logger.log("Heating: ")


def control_room(room: HeatingRoom, target_temp: float, logger: Logger):
    current_temp = room.get_current_temp()
    pin = room.get_control_pin()
    if current_temp is None:
        logger.warn(f"Heating: Undefined current temperature")
        disable_pin(pin)
        return
    logger.log(f"Heating: temp:{current_temp}°C, target:{target_temp}°C")
    if current_temp >= target_temp:
        room.set_target_temp_reached(True)
    if current_temp < (target_temp - TEMP_RANGE):
        room.set_target_temp_reached(False)
    if not room.get_target_temp_reached() and current_temp < target_temp:
        logger.log("Heating: Heating enabled")
        enable_pin(pin)
    else:
        logger.log("Heating: Heating disabled")
        disable_pin(pin)


def enable_pin(pin: int):
    io.set_low(pin)


def disable_pin(pin: int):
    io.set_high(pin)
