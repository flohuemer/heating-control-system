from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from datetime import datetime, timedelta
from shared import constants
from server import config
from os.path import join, exists
from os import mkdir


class ControlServer(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        parameters = parse_qs(query)
        status = 400
        if constants.TAG_PARAM not in parameters:
            self.send_response(400)
            self.end_headers()
            return
        if constants.TEMP_PARAM in parameters:
            self.write_temp(parameters[constants.TAG_PARAM]
                            [0], parameters[constants.TEMP_PARAM][0])
            status = 200
        if constants.REQUEST_PARAM in parameters:
            try:
                if parameters[constants.REQUEST_PARAM][0] == "True":
                    self.write_request(parameters[constants.TAG_PARAM][0])
                status = 200
            except ValueError:
                pass
        self.send_response(status)
        self.end_headers()

    def write_temp(self, tag, value):
        file_name = join(".", constants.RUNTIME_DIR, tag + constants.TEMP_EXT)
        with open(file_name, "w+") as f:
            f.write(str(value))

    def write_request(self, tag):
        file_name = join(".", constants.RUNTIME_DIR,
                         tag + constants.REQUEST_EXT)
        with open(file_name, "w+") as f:
            end = datetime.now() + timedelta(hours=4)
            f.write(str(end.timestamp()))


if __name__ == "__main__":
    c = config.read_config_file(
        join(".", constants.CONFIG_DIR, "server-config.json"))
    runtime_dir = join(".", constants.RUNTIME_DIR)
    if not exists(runtime_dir):
        mkdir(runtime_dir)

    webServer = HTTPServer(("localhost", config.port(c)), ControlServer)

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
