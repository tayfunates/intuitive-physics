import json
from svqa.simulation import Simulation
from svqa.causal_graph import CausalGraph
from svqa.event import Event

def test__event_class():
    event_dict = json.loads("""{
         "id": 4382325240,
         "objects": [2,3],
         "step": 500,
         "type": "End"
       }""")
    event_a = Event(event_dict)
    return event_a.id == 4382325240


def test__causal_graph():
    with open("../../simulation/2d/SVQA-Box2D/Testbed/graph.json") as graph_file:
        string = graph_file.read()
        causal_graph = CausalGraph(json.loads(string))

def test__json_read():
    initial_scene_path = "../../simulation/2d/SVQA-Box2D/Testbed/scene.json"
    end_scene_path = "../../simulation/2d/SVQA-Box2D/Testbed/scene.json"
    causal_graph_path = "../../simulation/2d/SVQA-Box2D/Testbed/graph.json"

    with open(initial_scene_path) as json_file:
        initial_scene = json.load(json_file)

    with open(end_scene_path) as json_file:
        end_scene = json.load(json_file)

    with open(causal_graph_path) as json_file:
        causal_graph = json.load(json_file)

    sim = Simulation(initial_scene, end_scene, causal_graph)


if __name__ == "__main__":
    assert test__event_class()
    test__causal_graph()

    test__json_read()
