

class Event:

    def __init__(self, event_dict):
        self.id = event_dict["id"]
        self.objects = event_dict["objects"]
        self.step = event_dict["step"]
        self.type = event_dict["type"]