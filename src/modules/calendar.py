import requests
from ics import Calendar
from os.path import exists
from datetime import timedelta
from abc import abstractmethod
from modules import files
from modules.logger import Logger


class CalendarRoom():
    @abstractmethod
    def get_tag(self) -> str: pass

    @abstractmethod
    def get_preheating_mins(self) -> int: pass


def __extract_rooms(calendar: Calendar, rooms: list[CalendarRoom], logger: Logger):
    room_requests = set()
    logger.log(f"Calendar: Found {len(calendar.events)} events.")
    for event in calendar.events:
        current_time = event.begin.now()
        end = event.end
        location = event.location
        for room in rooms:
            room_tag = room.get_tag()
            if not location or room_tag in location:
                start = event.begin - \
                    timedelta(minutes=room.get_preheating_mins())
                if current_time.is_between(start, end):
                    room_requests.add(room_tag)
        if len(rooms) == len(room_requests):
            break
    logger.log(f"Calendar: Extracted {len(room_requests)} heating requests.")
    return room_requests


def room_heating_requests(url: str, cache_file: str, rooms: list[CalendarRoom], logger: Logger):
    calendar_data = None
    try:
        calendar_data = requests.get(url).text
    except requests.exceptions.RequestException:
        calendar_data = files.read_runtime_file(cache_file)
    if calendar_data is None:
        return []
    files.write_runtime_file(cache_file, calendar_data)
    calendar = Calendar(calendar_data)
    return __extract_rooms(calendar, rooms, logger)
