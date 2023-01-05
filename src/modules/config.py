from os.path import exists, join
import json
from abc import abstractmethod

class ConfigFileException(Exception):
    pass

class ConfigEntry():
    @abstractmethod
    def parse(self, config) -> None: pass

    def __read_type(self, config, name, expected_type):
        try:
            value = config[name]
            if type(value) is not expected_type:
                raise ConfigFileException(f"Value type of {name} in config file is not {expected_type}.")
            return value
        except KeyError:
            raise ConfigFileException(f"Key {name} not found in config file entry.")

    def _read_int(self, config, name):
        return self.__read_type(config, name, int)


    def _read_float(self, config, name):
        return self.__read_type(config, name, float)


    def _read_string(self, config, name):
        return self.__read_type(config, name, str)


    def _read_list(self, config, name):
        return self.__read_type(config, name, list)

    def _read_dict(self, config, name):
        return self.__read_type(config, name, dict)


def read_config_file(config_path: str, config: ConfigEntry):
    if not exists(config_path):
        raise ConfigFileException(
            f"Config file at {config_path} does not exsist.")
    with open(config_path, "r") as f:
        config_data = json.load(f)
        config.parse(config_data)