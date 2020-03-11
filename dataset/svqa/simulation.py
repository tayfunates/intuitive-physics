from object import Object

class Simulation:
    def __init__(self, initial_scene_dict, end_scene_dict, causal_graph_dict ):
        self.objects = []
        for object_state_at_init, object_state_at_end in zip(initial_scene_dict, end_scene_dict):
            assert object_state_at_init[Object.KEY_UNIQUE_ID] != object_state_at_end[Object.KEY_UNIQUE_ID]
            self.objects.append(Object(object_state_at_init, object_state_at_end))

        self.causal_graph = causal_graph_dict
