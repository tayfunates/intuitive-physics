import json
import subprocess
import sys


class SimulationRunner(object):

    def __init__(self, exec_path: str):
        self.exec_path = exec_path

    def run_simulation(self, controller_json_path: str, debug_output_path=None):
        subprocess.call(f"{self.exec_path} {controller_json_path}",
                        shell=True,
                        universal_newlines=True,
                        stdout=sys.stdout
                        if debug_output_path is None
                        else open(debug_output_path, "w"))

    @staticmethod
    def create_controller_file_for(file_path: str,
                                   simulation_id: int,
                                   offline: bool,
                                   output_video_path: str,
                                   output_json_path: str,
                                   width: int,
                                   height: int,
                                   step: int,
                                   input_scene_file_path: str = None):
        with open(file_path, 'w') as controller_file:
            json.dump(
                json.loads(
                    f"""{{
                            "simulationID": {simulation_id},
                            "offline": {str(offline).lower()},
                            "outputVideoPath": "{output_video_path}",
                            "outputJSONPath": "{output_json_path}",
                            "width":  {width},
                            "height": {height},
                            "inputScenePath":  "{'' if input_scene_file_path is None else input_scene_file_path}",
                            "stepCount": {step}
                        }}"""),
                controller_file,
                indent=4
            )