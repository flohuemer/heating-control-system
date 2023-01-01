def check_int(val):
    if type(val) is not int:
        raise Exception("Invalid config value")


def check_float(val):
    if type(val) is not float:
        raise Exception("Invalid config value")


def check_string(val):
    if type(val) is not str:
        raise Exception("Invalid config value")


def check_list(val):
    if type(val) is not list:
        raise Exception("Invalid config value")
