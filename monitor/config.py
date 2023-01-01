from shared.configcheck import check_string, check_int
from os.path import exists
import json


def read_config_file(path):
    if not exists(path):
        raise Exception(f"Config file {path} not found")
    with open(path, "r") as f:
        config = json.load(f)
        try:
            check_string(server_hostname(config))
            check_int(server_port(config))
            check_int(sensor_pin(config))
            check_int(button_pin(config))
            check_string(tag(config))
        except KeyError:
            raise Exception("Invalid config file")
        return config


def server_hostname(config):
    return config["server"]["hostname"]


def server_port(config):
    return config["server"]["port"]


def sensor_pin(config):
    return config["sensor"]["pin"]


def button_pin(config):
    return config["button"]["pin"]


def tag(config):
    return config["tag"]
