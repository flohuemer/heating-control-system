from monitor import sensor, button, config
import requests
from shared import constants
from time import sleep
from os.path import join


def setup(c):
    sensor.setup(config.sensor_pin(c))
    button.setup(config.button_pin(c))


def loop(c):
    url = "http://" + config.server_hostname(c) + ":" + str(config.server_port(c)) + "?" + constants.TAG_PARAM + \
        "=" + config.tag(c) + "&" + constants.TEMP_PARAM + \
        "={0}&" + constants.REQUEST_PARAM + "={1}"
    i = 0
    while True:
        try:
            request = button.is_pressed(config.button_pin(c))
            if request or i == 0:
                temp = sensor.get_temp(config.sensor_pin(c))
                requests.get(url.format(temp, request))
                i = 400
            sleep(0.05)
            i -= 1
        except requests.exceptions.RequestException:
            sleep(30)
        except KeyboardInterrupt:
            break


def teardown(c):
    sensor.cleanup()


if __name__ == "__main__":
    c = config.read_config_file(
        join(".", constants.CONFIG_DIR, "monitor-unit-config.json"))
    setup(c)
    loop(c)
    teardown(c)
