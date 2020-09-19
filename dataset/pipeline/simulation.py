import subprocess
import sys


class SimulationRunner(object):

    def __init__(self, exec_path: str):
        self.exec_path = exec_path

    def run_simulation(self, controller_json_path: str, debug_output_path=None):
        subprocess.call(f"{self.exec_path} {controller_json_path}",
                        shell=True,
                        universal_newlines=True,
                        stdout=sys.stdout if debug_output_path is None else open(debug_output_path, "w"))

    def run_variations(self):
        pass