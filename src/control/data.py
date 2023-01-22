from modules.config import ConfigEntry, read_config_file
from modules.heating import HeatingRoom
from modules.calendar import CalendarRoom
from modules.monitor import MonitorRoom

class Calendar(ConfigEntry):
    url: str = None
    cache_file: str = None
    update_interval: int = 0

    def parse(self, config):
        self.url = self._read_string(config, "url")
        self.cache_file = self._read_string(config, "cache_file")
        self.update_interval = self._read_int(config, "update_interval")

class Room(ConfigEntry, HeatingRoom, CalendarRoom, MonitorRoom):
    tag: str = None
    target_temp: float = 0.0
    setback_temp: float = 0.0
    preheating_mins: int = 0
    control_pin: int = 0

    current_temp: float = 0.0
    target_temp_reached: bool = False

    def parse(self, config) -> None:
        self.tag = self._read_string(config, "tag")
        self.target_temp = self._read_float(config, "target_temp")
        self.setback_temp = self._read_float(config, "setback_temp")
        self.preheating_mins = self._read_int(config, "preheating_mins")
        self.control_pin = self._read_int(config, "control_pin")

    def get_tag(self) -> str:
        return self.tag

    def get_preheating_mins(self) -> int:
        return self.preheating_mins

    def get_control_pin(self) -> int:
        return self.control_pin

    def get_current_temp(self) -> float:
        return self.current_temp
    
    def set_current_temp(self, value) -> None:
        self.current_temp = value

    def get_target_temp(self) -> float:
        return self.target_temp

    def get_setback_temp(self) -> float:
        return self.setback_temp
    
    def get_target_temp_reached(self) -> bool:
        return self.target_temp_reached

    def set_target_temp_reached(self, value: bool) -> None:
        self.target_temp_reached = value

class Rooms(list[Room] ,ConfigEntry):
    def parse(self, config):
        for entry in config:
            r = Room()
            r.parse(entry)
            self.append(r)

class ControlUnitConfig(ConfigEntry):
    calendar = Calendar()
    rooms = Rooms()
    log_file: str = None

    def parse(self, config) -> None:
        self.calendar.parse(self._read_dict(config, "calendar"))
        self.rooms.parse(self._read_list(config, "rooms"))
        self.log_file = self._read_string(config, "log_file")

    def from_file(file_path:str):
        c = ControlUnitConfig()
        read_config_file(file_path, c)
        return c