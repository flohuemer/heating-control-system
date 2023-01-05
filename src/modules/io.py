import random


def cleanup():
    print("Clean up pins")


def setup():
    pass


def setup_output_pin(pin: int):
    print(f"Set pin {pin} to output")


def setup_intput_pin(pin: int):
    print(f"Set pin {pin} to input")


def is_high(pin: int):
    return random.random() == 0.0


def is_low(pin: int):
    return not is_high(pin)

def get_DHT22_data(pin: int):
    return random.uniform(19, 21.2)