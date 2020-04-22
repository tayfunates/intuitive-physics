
# Takes 1 input that is the output of the simulation.
# Produces variations of it (number of object + 1)

import sys
import argparse
import json
import subprocess
import os
import glob
import copy
from autorun import run_simulation

args = None


def new_output_json(output: json, i: int):
    output = copy.deepcopy(output)
    del output["scene_states"][0]["scene"]["objects"][i]
    return output


def create_variations(controller: json, output: json) -> list:
    start_scene_state = output["scene_states"][0]
    objects = start_scene_state["scene"]["objects"]
    variations = [(objects[i]["uniqueID"], new_output_json(output, i)) for i in range(len(objects)) if objects[i]["bodyType"] != 0] #0 for static objects
    controller_paths = []
    for i in range(len(variations)):
        output = variations[i]
        name = f"{os.path.splitext(args.path)[0]}_var_{output[0]}"
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


def init_args():
    global args

    parser = argparse.ArgumentParser()
    parser.add_argument('--path', action='store', dest='path', required=True,
                        help='Simulation\'s output JSON path.')
    parser.add_argument('--controller-path', action='store', dest='controller_path', required=True,
                        help='Simulation\'s controller JSON path.')
    parser.add_argument('--executable-path', action='store', dest='exec_path', required=False, nargs='?', type=str,
                        default="\"../../simulation/2d/SVQA-Box2D/Build/bin/x86_64/Release/Testbed\"",
                        help='Testbed executable path.')
    parser.add_argument('--variations-output-path', action='store', dest='variations_output_path', required=True,
                        help='Simulation\'s output JSON path.')

    args = parser.parse_args()

def get_variation_output(controller: str):
    with open(controller) as controller_json_file:
        controller_data = json.load(controller_json_file)
        with open(controller_data["outputJSONPath"]) as output_json_file:
            output_data = json.load(output_json_file)

    return output_data


def run_variations():
    final_output_json = {}
    original_output_path = json.load(open(args.path, "r"))
    final_output_json["original_video_output"] = original_output_path
    variation_outputs = {}

    controller_paths = create_variations(json.load(open(args.controller_path, "r")), original_output_path)
    for c in controller_paths:
        run_simulation(args.exec_path, c[1])
        variation_outputs[str(c[0])] = get_variation_output(c[1])
    final_output_json["variations_outputs"] = variation_outputs

    json.dump(final_output_json, open(args.variations_output_path, "w"))


if __name__ == '__main__':
    init_args()
    print(f"Executable path: '{args.exec_path}'\nController path: '{args.controller_path}'\nSimulation\'s output JSON path: '{args.path}'")
    run_variations()
