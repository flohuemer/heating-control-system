from os.path import join, exists
from os import mkdir

RUNTIME_DIR = join(".", "runtime")

TEMPERATURE_EXT = ".temp"
REQUEST_EXT = ".req"

def __get_runtime_file_path(file_name: str) -> str:
    if not exists(RUNTIME_DIR):
        mkdir(RUNTIME_DIR)
    return join(RUNTIME_DIR, file_name)


def append_runtime_file(file_name:str, data: str) -> None:
    path = __get_runtime_file_path(file_name)
    with open(path, "a+") as f:
        f.write(str(data))

def write_runtime_file(file_name: str, data: str) -> None:
    path = __get_runtime_file_path(file_name)
    with open(path, "w+") as f:
        f.write(str(data))

def read_runtime_file(file_name:str) -> str:
    path = __get_runtime_file_path(file_name)
    if not exists(path):
        return None
    with open(path, "r") as f:
        return f.read()