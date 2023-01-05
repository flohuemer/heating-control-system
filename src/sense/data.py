from modules.config import ConfigEntry, read_config_file


class SenseUnitConfig(ConfigEntry):
    uri: str = None
    sensor_pin: int = 0
    button_pin: int = 0
    tag: str = None
    update_interval: int = 20
    log_file: str = None

    def parse(self, config) -> None:
        server = self._read_dict(config, "server")
        hostname = self._read_string(server, "hostname")
        port = self._read_int(server, "port")
        self.uri = f"ws://{hostname}:{port}"
        self.update_interval = self._read_int(server, "update_interval")
        self.sensor_pin = self._read_int(config, "sensor_pin")
        self.button_pin = self._read_int(config, "button_pin")
        self.tag = self._read_string(config, "tag")
        self.log_file = self._read_string(config, "log_file")

    def from_file(file_path: str):
        c = SenseUnitConfig()
        read_config_file(file_path, c)
        return c
