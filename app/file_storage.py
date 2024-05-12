import json
from typing import List

class EventFileManager:
    FILE_PATH = "events.json"

    @classmethod
    def read_events_from_file(cls) -> List[dict]:
        try:
            with open(cls.FILE_PATH, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @classmethod
    def write_events_to_file(cls, events: List[dict]):
        with open(cls.FILE_PATH, 'w') as file:
            json.dump(events, file, indent=4)

