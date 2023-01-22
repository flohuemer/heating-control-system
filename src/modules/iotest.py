import random


def cleanup():
    print("Clean up pins")


def setup():
    pass


def setup_output_pin(pin: int):
    print(f"Set pin {pin} to output")


def setup_input_pin(pin: int):
    print(f"Set pin {pin} to input")


def setup_pull_up_pin(pin: int):
    print(f"Set pin {pin} to pull up input")


def setup_pull_down_pin(pin: int):
    print(f"Set pin {pin} to pull down input")


def set_high(pin: int):
    print(f"Set pin {pin} to high")


def set_low(pin: int):
    print(f"Set pin {pin} to low")


def is_high(pin: int):
    return not is_low(pin)


def is_low(pin: int):
    return random.random() == 0.0


def get_DHT22_temp(pin: int):
    return random.uniform(12, 21.2)
