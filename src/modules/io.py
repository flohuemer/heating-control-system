import RPi.GPIO as GPIO
import Adafruit_DHT


def cleanup():
    GPIO.cleanup()


def setup():
    GPIO.setmode(GPIO.BCM)


def setup_output_pin(pin: int):
    GPIO.setup(pin, GPIO.OUT)


def setup_input_pin(pin: int):
    GPIO.setup(pin, GPIO.IN)


def setup_pull_up_pin(pin: int):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def setup_pull_down_pin(pin: int):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def set_high(pin: int):
    GPIO.output(pin, GPIO.HIGH)


def set_low(pin: int):
    GPIO.output(pin, GPIO.LOW)


def is_high(pin: int):
    return GPIO.input(pin) == GPIO.HIGH


def is_low(pin: int):
    return GPIO.input(pin) == GPIO.LOW


def get_DHT22_temp(pin: int):
    _, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pin)
    return temp
