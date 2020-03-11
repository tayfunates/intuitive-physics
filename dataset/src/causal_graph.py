from src.event import Event


class CausalGraph:

    def __init__(self, graph_dict):
        # TODO: Can be optimized, I guess.

        self.__id_to_event = {}  # Mapping integer event IDs to Event objects.
        self.__from_id_to_ids = {}  # Mapping integer event IDs to connected event IDs. Represents edges.
        for event_dict in graph_dict["nodes"]:
            self.__id_to_event[event_dict["id"]] = Event(event_dict)
        for edge_dict in graph_dict["edges"]:
            self.__from_id_to_ids[edge_dict["from"]] = edge_dict["to"]

        self.__graph = {}

        for event in self.__id_to_event.values():
            self.__graph[event] = [self.__id_to_event[event_id] for event_id in self.__from_id_to_ids[event.id]]
