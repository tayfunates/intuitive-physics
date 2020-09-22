import copy
import json
import os
import subprocess
import sys

from svqa.causal_graph import CausalGraph


class SimulationRunner(object):

    def __init__(self, exec_path: str):
        self.exec_path = exec_path

    def run_simulation(self, controller_json_path: str, debug_output_path=None):
        subprocess.call(f"{self.exec_path} {controller_json_path}",
                        shell=True,
                        universal_newlines=True,
                        stdout=sys.stdout if debug_output_path is None else open(debug_output_path, "w"))

    def run_variations(self, controller_json_path: str, variations_output_path: str, debug_output_path=None):
        variation_runner = VariationRunner(self)
        variation_runner.run_variations(controller_json_path, variations_output_path, debug_output_path)


class SimulationInstance:

    def __init__(self, instance_id: int, runner: SimulationRunner, controller_json_path: str):
        self.__runner = runner
        self.__controller_json_path = controller_json_path
        self.instance_id = instance_id

    def run_simulation(self, debug_output_path=None):
        self.__runner.run_simulation(self.__controller_json_path, debug_output_path)

    def run_variations(self, variations_output_path: str, debug_output_path=None):
        self.__runner.run_variations(self.__controller_json_path, variations_output_path, debug_output_path)


class VariationRunner(object):

    def __init__(self, runner: SimulationRunner):
        self.__runner = runner

    def __new_output_json(self, output: json, i: int):
        ret = copy.deepcopy(output)
        del ret["scene_states"][0]["scene"]["objects"][i]
        del ret["causal_graph"]
        for i in range(len(ret["scene_states"])):
            if ret["scene_states"][i]["step"] != 0:
                del ret["scene_states"][i]
        return ret

    def __create_variations(self, path: str, controller: json, output: json) -> list:
        start_scene_state = output["scene_states"][0]  # best to check step count
        objects = start_scene_state["scene"]["objects"]
        variations = [(objects[i]["uniqueID"], self.__new_output_json(output, i)) for i in range(len(objects)) if
                      objects[i]["bodyType"] != 0]  # 0 for static objects
        controller_paths = []
        for i in range(len(variations)):
            output = variations[i]
            name = f"{os.path.splitext(path)[0]}_var_{output[0]}"
            json.dump(output[1], open(f"{name}.json", "w"))
            controller_paths.append((output[0], self.__create_controller_variations(controller, name)))

        return controller_paths

    def __create_controller_variations(self, controller: json, name: str) -> str:
        controller = copy.deepcopy(controller)
        controller["outputVideoPath"] = f"{name}_out.mpg"
        controller["outputJSONPath"] = f"{name}_out.json"
        controller["inputScenePath"] = f"{name}.json"

        name = f"{name}_controller.json"
        json.dump(controller, open(name, "w"))
        return name

    def __get_variation_output(self, controller: str):
        with open(controller) as controller_json_file:
            controller_data = json.load(controller_json_file)
            with open(controller_data["outputJSONPath"]) as output_json_file:
                output_data = json.load(output_json_file)

        return output_data

    def __is_equal_without_step(self, event1, event2):
        return set(event1["objects"]) == set(event2["objects"]) and event1["type"] == event2["type"]

    def __get_different_event_list(self, causal_graph_src: CausalGraph, causal_graph_compare: CausalGraph,
                                   object_props: dict,
                                   discarded_object_id: int):
        src_events = causal_graph_src.events
        compare_events = causal_graph_compare.events

        discarded_shapes = ['platform']
        objects_ids_discarded = [object['uniqueID'] for object in object_props if
                                 object['shape'] in discarded_shapes]

        res = []
        for src_event in src_events:
            objects_of_event = src_event['objects']
            # discard events including object to be discarded
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
                if self.__is_equal_without_step(src_event, compare_event):
                    found_equal = True
                    break
            if not found_equal:
                res.append(src_event["id"])

        return res

    def __write_enables_prevents(self, output_dict: dict):
        original_causal_graph = CausalGraph(output_dict["original_video_output"]["causal_graph"])
        variation_outputs = output_dict["variations_outputs"]

        output_dict_enables = []
        output_dict_prevents = []
        for removed_object_key in variation_outputs:
            removed_object_id = int(removed_object_key)
            variation_causal_graph = CausalGraph(variation_outputs[removed_object_key]["causal_graph"])
            enables = self.__get_different_event_list(original_causal_graph, variation_causal_graph,
                                                      output_dict['original_video_output']['scene_states'][0]['scene'][
                                                          'objects'],
                                                      removed_object_id)
            prevents = self.__get_different_event_list(variation_causal_graph, original_causal_graph,
                                                       output_dict['original_video_output']['scene_states'][0]['scene'][
                                                           'objects'],
                                                       removed_object_id)

            output_dict_enables.extend([{removed_object_key: enabled_event_id} for enabled_event_id in enables])
            output_dict_prevents.extend([{removed_object_key: prevent_event_id} for prevent_event_id in prevents])

        output_dict["enables"] = output_dict_enables
        output_dict["prevents"] = output_dict_prevents

    def run_variations(self, controller_json_path: str, variations_output_path: str, debug_output_path: str):
        final_output_json = {}

        controller_json = json.load(open(controller_json_path, "r"))
        original_output_path: str = controller_json["outputJSONPath"]
        original_output: dict = json.load(open(original_output_path, "r"))
        final_output_json["original_video_output"] = original_output
        variation_outputs = {}

        controller_paths = self.__create_variations(original_output_path,
                                                    controller_json,
                                                    original_output)
        for c in controller_paths:
            self.__runner.run_simulation(c[1], debug_output_path)
            variation_outputs[str(c[0])] = self.__get_variation_output(c[1])
        final_output_json["variations_outputs"] = variation_outputs

        self.__write_enables_prevents(final_output_json)

        with open(variations_output_path, "w") as f:
            json.dump(final_output_json, f)


class QuestionGenerator:

    def __init__(self,
                 input_scene_file_path: str,
                 output_file_path: str,
                 simulation_config: dict,
                 instances_per_template=5):
        self.__args = QuestionGeneratorScript.parser.parse_args(['--input-scene-file', input_scene_file_path,
                                                                 '--output-questions-file', output_file_path,
                                                                 '--metadata-file', '../svqa/metadata.json',
                                                                 '--synonyms-json', '../svqa/synonyms.json',
                                                                 '--template-dir', '../svqa/SVQA_1.0_templates',
                                                                 '--restrict-template-count-per-video', False,
                                                                 '--print-stats', False,
                                                                 '--excluded-task-ids',
                                                                 simulation_config["excluded_task_ids"]])

    def execute(self):
        QuestionGeneratorScript.main(self.__args)
