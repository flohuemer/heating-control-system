from datetime import datetime
from modules import files


class Logger():
    def __init__(self, file) -> None:
        self.file = file

    def __write(self, level: str, msg: str):
        timestamp = datetime.now()
        data = f"{timestamp} {level}: {msg}"
        print(data)
        files.append_runtime_file(self.file, data + "\n")

    def log(self, msg: str):
        self.__write("LOG", msg)

    def warn(self, msg: str):
        self.__write("WARN", msg)

    def error(self, msg: str):
        self.__write("ERROR", msg)
