from os.path import exists
import json
from shared.configcheck import check_float, check_int, check_list, check_string


def read_config_file(path):
    if not exists(path):
        raise Exception(f"Config file {path} not found")
    with open(path, "r") as f:
        config = json.load(f)
        try:
            check_string(calendar_url(config))
            check_string(calendar_cache_path(config))
            check_list(calendar_rooms(config))
            for room in calendar_rooms(config):
                check_string(room_tag(room))
                check_float(room_target_temp(room))
                check_int(room_preheating_mins(room))
                check_int(room_control_pin(room))
            return config
        except KeyError:
            raise Exception("Invalid config file")


def calendar_url(config):
    return config["calendar"]["url"]


def calendar_cache_path(config):
    return config["calendar"]["cache_path"]


def calendar_rooms(config):
    return config["rooms"]


def room_tag(room):
    return room["tag"]


def room_target_temp(room):
    return room["target_temp"]


def room_preheating_mins(room):
    return room["preheating_mins"]


def room_control_pin(room):
    return room["control_pin"]


def room_current_temp(room):
    return room["current_temp"]


def set_room_current_temp(room, value):
    room["current_temp"] = value


def room_target_reached(room):
    return room["target_reached"]


def set_room_target_reached(room, value):
    room["target_reached"] = value
