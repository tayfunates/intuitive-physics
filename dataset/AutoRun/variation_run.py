
# Takes 1 input that is the output of the simulation.
# Produces variations of it (number of object + 1)

import sys
import argparse
import json
import subprocess
import os
import glob
import copy
from AutoRun.generate_dataset import run_simulation
from svqa.causal_graph import CausalGraph


def new_output_json(output: json, i: int):
    ret = copy.deepcopy(output)
    del ret["scene_states"][0]["scene"]["objects"][i]
    del ret["causal_graph"]
    for i in range(len(ret["scene_states"])):
        if ret["scene_states"][i]["step"] != 0:
            del ret["scene_states"][i]
    return ret


def create_variations(path: str, controller: json, output: json) -> list:
    start_scene_state = output["scene_states"][0] #best to check step count
    objects = start_scene_state["scene"]["objects"]
    variations = [(objects[i]["uniqueID"], new_output_json(output, i)) for i in range(len(objects)) if objects[i]["bodyType"] != 0] #0 for static objects
    controller_paths = []
    for i in range(len(variations)):
        output = variations[i]
        name = f"{os.path.splitext(path)[0]}_var_{output[0]}"
        json.dump(output[1], open(f"{name}.json", "w"))
        controller_paths.append((output[0], create_controller_variations(controller, name)))

    return controller_paths


def create_controller_variations(controller: json, name: str) -> str:
    controller = copy.deepcopy(controller)
    controller["outputVideoPath"] = f"{name}_out.mpg"
    controller["outputJSONPath"] = f"{name}_out.json"
    controller["inputScenePath"] = f"{name}.json"

    name = f"{name}_controller.json"
    json.dump(controller, open(name, "w"))
    return name


def get_variation_output(controller: str):
    with open(controller) as controller_json_file:
        controller_data = json.load(controller_json_file)
        with open(controller_data["outputJSONPath"]) as output_json_file:
            output_data = json.load(output_json_file)

    return output_data


def is_equal_without_step(event1, event2):
    return (set(event1["objects"]) == set(event2["objects"]) and event1["type"] == event2["type"])


def get_different_event_list(causal_graph_src: CausalGraph, causal_graph_compare: CausalGraph, object_props: dict, discarded_object_id: int):
    src_events = causal_graph_src.events
    compare_events = causal_graph_compare.events

    discarded_shapes = ['platform']
    objects_ids_discarded = [object['uniqueID'] for object in object_props if object['shape'] in discarded_shapes]

    res = []
    for src_event in src_events:
        objects_of_event = src_event['objects']
        #discard events including object to be discarded
        if discarded_object_id in objects_of_event:
            continue
        found_discarded_shape = False
        for object_of_event in objects_of_event:
            if object_of_event in objects_ids_discarded:
                found_discarded_shape = True
                break
        if found_discarded_shape:
            continue

        found_equal = False
        for compare_event in compare_events:
            if is_equal_without_step(src_event, compare_event):
                found_equal = True
                break
        if not found_equal :
            res.append(src_event["id"])

    return res


def write_enables_prevents(output_dict: dict):
    original_causal_graph = CausalGraph(output_dict["original_video_output"]["causal_graph"])
    variation_outputs = output_dict["variations_outputs"]

    output_dict_enables = []
    output_dict_prevents = []
    for removed_object_key in variation_outputs:
        removed_object_id = int(removed_object_key)
        variation_causal_graph = CausalGraph(variation_outputs[removed_object_key]["causal_graph"])
        enables = get_different_event_list(original_causal_graph, variation_causal_graph, output_dict['original_video_output']['scene_states'][0]['scene']['objects'], removed_object_id)
        prevents = get_different_event_list(variation_causal_graph, original_causal_graph, output_dict['original_video_output']['scene_states'][0]['scene']['objects'], removed_object_id)

        output_dict_enables.extend([{removed_object_key: enabled_event_id} for enabled_event_id in enables])
        output_dict_prevents.extend([{removed_object_key: prevent_event_id} for prevent_event_id in prevents])

    output_dict["enables"] = output_dict_enables
    output_dict["prevents"] = output_dict_prevents


def run_variations(args):
    final_output_json = {}
    original_output_path = json.load(open(args.path, "r"))
    final_output_json["original_video_output"] = original_output_path
    variation_outputs = {}

    controller_paths = create_variations(args.path, json.load(open(args.controller_path, "r")), original_output_path)
    for c in controller_paths:
        run_simulation(args.exec_path, c[1])
        variation_outputs[str(c[0])] = get_variation_output(c[1])
    final_output_json["variations_outputs"] = variation_outputs

    write_enables_prevents(final_output_json)

    json.dump(final_output_json, open(args.variations_output_path, "w"))


def init_args(arg_list=None):

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path','--original-path', action='store', dest='path', required=True,
                        help='Simulation\'s original output JSON path.')
    parser.add_argument('-c', '--controller-path', action='store', dest='controller_path', required=True,
                        help='Simulation\'s controller JSON path.')
    parser.add_argument('-exec', '--executable-path', action='store', dest='exec_path', required=False, nargs='?', type=str,
                        default="\"../../simulation/2d/SVQA-Box2D/Build/bin/x86_64/Release/Testbed\"",
                        help='Testbed executable path.')
    parser.add_argument('-o', '--variations-output-path', action='store', dest='variations_output_path', required=True,
                        help='Variations\' output JSON path.')

    return parser.parse_args() if arg_list is None else parser.parse_args(arg_list)


if __name__ == '__main__':
    args = init_args()
    print(f"Executable path: '{args.exec_path}'\nController path: '{args.controller_path}'\nSimulation\'s output JSON path: '{args.path}'")
    run_variations(args)
