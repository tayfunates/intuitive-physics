from svqa.event import Event


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

    @property
    def events(self):
        return self.__graph.keys()

    def events_after(self, step_count):
        return [event for event in self.events if event.step > step_count]

    def events_before(self, step_count):
        return [event for event in self.events if event.step < step_count]

    def immediate_outcome_events(self, event: Event):
        return self.__graph[event]

    def immediate_cause_events(self, event: Event):
        causes = []
        for e in self.events:
            if event in self.immediate_outcome_events(e):
                causes.append(e)
        return causes

    def outcome_events(self, cause: Event):
        all_outcomes = []
        outcomes = self.immediate_outcome_events(cause)
        all_outcomes.extend(outcomes)
        for event in outcomes:
            all_outcomes.append(self.outcome_events(event))
        return all_outcomes

    def cause_events(self, outcome: Event):
        all_causes = []
        causes = self.immediate_cause_events(outcome)
        all_causes.extend(causes)
        for outcome in causes:
            all_causes.append(self.outcome_events(outcome))
        return all_causes