from enum import Enum


class Event:
    class Type(Enum):
        START = "Start"
        END = "End"
        COLLISION = "Collision"
        START_TOUCHING = "StartTouching"
        END_TOUCHING = "EndTouching"

    KEY_ID = "id"
    KEY_OBJECTS = "objects"
    KEY_STEP = "step"
    KEY_TYPE = "type"

    def __init__(self, event_dict):
        self.id = event_dict[Event.KEY_ID]
        self.objects = event_dict[Event.KEY_OBJECTS]
        self.step = event_dict[Event.KEY_STEP]
        self.type = Event.Type(event_dict[Event.KEY_TYPE])

    def __hash__(self):
        return self.id

    def __str__(self):
        return str(self.id)