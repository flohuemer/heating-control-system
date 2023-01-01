import requests
from ics import Calendar
from os.path import exists
from datetime import timedelta
from control import config


def read_cache(path):
    if not exists(path):
        return None
    with open(path, "r") as f:
        return f.read()


def write_cache(path, calendar):
    with open(path, "w+") as f:
        f.write(calendar)


def extract_rooms(calendar, rooms):
    room_requests = set()
    for event in calendar.events:
        current_time = event.begin.now()
        end = event.end
        location = event.location
        for room in rooms:
            room_tag = config.room_tag(room)
            if not location or room_tag in location:
                start = event.begin - \
                    timedelta(minutes=config.room_preheating_mins(room))
                if current_time.is_between(start, end):
                    room_requests.add(room_tag)
        if len(rooms) == len(room_requests):
            break
    return room_requests


def room_heating_requests(url, cache_path, rooms):
    calendar_data = None
    try:
        calendar_data = requests.get(url).text
    except requests.exceptions.RequestException:
        calendar_data = read_cache(cache_path)
    if calendar_data is None:
        return []
    write_cache(cache_path, calendar_data)
    calendar = Calendar(calendar_data)
    return extract_rooms(calendar, rooms)
