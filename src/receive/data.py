from modules.config import ConfigEntry, read_config_file

class ReceiveUnitConfig(ConfigEntry):
    port: int = 0
    log_file: str = None

    def parse(self, config) -> None:
        self.port = self._read_int(config, "port")
        self.log_file = self._read_string(config, "log_file")

    def from_file(file_path:str):
        c = ReceiveUnitConfig()
        read_config_file(file_path, c)
        return c