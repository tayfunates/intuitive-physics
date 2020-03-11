import json

from src.event import Event

if __name__ == "__main__":
    event_dict = json.loads("""{
      "id": 4382325240,
      "objects": [2,3],
      "step": 500,
      "type": "End"
    }""")
    eventA = Event(event_dict)
    print(eventA)