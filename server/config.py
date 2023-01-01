from shared.configcheck import check_int
from os.path import exists
import json

def read_config_file(path):
    if not exists(path):
        raise Exception(f"Config file {path} not found")
    with open(path, "r") as f:
        config  = json.load(f)
        try:
            check_int(port(config))
        except KeyError:
            raise Exception("Invalid config file")
        return config


def port(config):
    return config["port"]