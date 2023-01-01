from control import config

TEMP_RANGE = 0.5


def setup_heating(rooms):
    for room in rooms:
        setup_pin(config.room_control_pin(room))
        config.set_room_target_reached(room, False)


def setup_pin(pin):
    print(f"Pin {pin} set up")


def cleanup():
    print("Pin cleanup")


def control_heating(rooms, room_heating_requests):
    for room in rooms:
        if config.room_tag(room) in room_heating_requests:
            control_room(room)
        else:
            disable_pin(config.room_control_pin(room))


def control_room(room):
    current_temp = config.room_current_temp(room)
    if current_temp is None:
        disable_pin(config.room_control_pin(room))
        return
    target_temp = config.room_target_temp(room)
    if current_temp >= target_temp:
        config.set_room_target_reached(room, True)
    if current_temp < (target_temp - TEMP_RANGE):
        config.set_room_target_reached(room, False)
    if not config.room_target_reached(room) and current_temp < target_temp:
        enable_pin(config.room_control_pin(room))
    else:
        disable_pin(config.room_control_pin(room))


def enable_pin(pin):
    print(f"Pin {pin} enabled")


def disable_pin(pin):
    print(f"Pin {pin} disabled")
