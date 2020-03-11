

class Event:

    KEY_ID = "id"
    KEY_OBJECTS = "objects"
    KEY_STEP = "step"
    KEY_TYPE = "type"

    def __init__(self, event_dict):
        self.id = event_dict[Event.KEY_ID]
        self.objects = event_dict[Event.KEY_OBJECTS]
        self.step = event_dict[Event.KEY_STEP]
        self.type = event_dict[Event.KEY_TYPE]

