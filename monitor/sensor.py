import random


def setup(pin):
    print(f"Pin {pin} set up")


def cleanup():
    print("Pin cleanup")


def get_temp(pin):
    return random.uniform(19, 21.2)
