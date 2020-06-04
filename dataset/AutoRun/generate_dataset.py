import argparse
import glob
import json
import os
import subprocess
import pathlib
import traceback

import AutoRun.variation_run as variation_run
import svqa.generate_questions as generate_questions

"""
Generates a dataset that contains simulation outputs with variations and their videos.

Single data in the dataset is generated as follows:
- Run a simulation
- Run its variations
- Unify them under a single output file
- Generate question-answer pairs according to the output
- Merge the questions into a single file along with video paths.

- Dataset folder
  - /intermediates          (A folder for intermediate outputs, may be used for debugging purposes.)
    - /sim-id-0  
      - train_XXXXXX.json   (One simulation output with variations.)
      - test_XXXXXX.json    
      - val_XXXXXX.json      
      - /debug              (A folder for intermediate variation outputs, cli outputs, and controller files.)
    - /sim-id-1
      ...
    ...
  - /videos
    - /sim-id-0
      - train_xxxxxx.mpg
      - test_xxxxxx.mpg
      - val_xxxxxx.mpg
  - dataset.json            (This json file contains all the video paths, and can questions generated from the outputs.)
"""


class Config(object):
    def __init__(self, config_dict):
        self.dataset_size = config_dict['dataset_size']
        self.executable_path = os.path.abspath(config_dict['executable_path']).replace("\\", "/")
        self.output_folder_path = os.path.abspath(config_dict['output_folder_path']).replace("\\", "/")
        self.test_set_ratio = config_dict['test_set_ratio']
        self.validation_set_ratio = config_dict['validation_set_ratio']
        self.train_set_ratio = config_dict['train_set_ratio']
        self.simulation_configs = config_dict['simulation_configs']


def init_args():
    parser = argparse.ArgumentParser()

    """
    Example configuration file content is as follows:
        {
          "dataset_size": 1000,
          "executable_path": "../../simulation/2d/SVQA-Box2D/Build/bin/x86_64/Release/Testbed",
          "output_folder_path": "dataset1000/",
          "test_set_ratio": 0.2,
          "validation_set_ratio": 0.2,
          "train_set_ratio": 0.6,
          "simulation_configs": [
            {
              "id": 0,
              "step_count": 600,
              "width": 256,
              "height": 256
            },
            {
              "id": 1,
              "step_count": 600,
              "width": 256,
              "height": 256
            }
          ]
        }
    
    If more than one simulation config is specified as above, for example 2, total dataset_size will be 2 * 1000.
    """

    parser.add_argument('-config', '--configuration-file', action='store', dest='configuration_file', required=True,
                        help="""
                                    File path to a JSON file that includes parameters for generating a dataset.
                               """)

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    return parser.parse_args()


def delete_files(folder_path, *wildcards):
    files_to_be_removed = []
    for w in wildcards:
        files_to_be_removed.extend([os.path.abspath(c) for c in glob.glob(f"{folder_path}/{w}")])

    for path in files_to_be_removed:
        os.remove(path) if os.path.exists(path) else None


def run_simulation(exec_path: str, controller_json_path: str, debug_output_path=None):
    subprocess.call(f"{exec_path} {controller_json_path}", shell=True, universal_newlines=True,
                    stdout=open(
                        f"{pathlib.Path(controller_json_path).parent}/cl_debug_{pathlib.Path(controller_json_path).name.replace('.json', '.txt').replace('controller_', '').replace('_controller', '')}".replace("\\", "/"), "w")
                    if debug_output_path is None
                    else open(debug_output_path, "w"))


def generate(config: Config):
    os.makedirs(config.output_folder_path, exist_ok=True)

    dataset = json.loads("[]")

    json.dump(
        dataset,
        open(f"{config.output_folder_path}/dataset.json", "w"),
        indent=4
    )

    intermediates_folder_path = f"{config.output_folder_path}/intermediates"
    for sim in config.simulation_configs:
        os.makedirs(f"{intermediates_folder_path}/sim-id-{sim['id']}/debug", exist_ok=True)
        os.makedirs(f"{config.output_folder_path}/videos/sim-id-{sim['id']}", exist_ok=True)

    test = int(float(config.test_set_ratio) * config.dataset_size)
    val = int(float(config.validation_set_ratio) * config.dataset_size)
    train = int(float(config.train_set_ratio) * config.dataset_size)

    data_types = ["test"] * test + ["val"] * val + ["train"] * train

    for i in range(len(data_types)):
        data_type = data_types[i]
        for sim in config.simulation_configs:

            # Create controller file.
            controller_json_path = f"{intermediates_folder_path}/sim-id-{sim['id']}/debug/controller_{data_type}_{i:06d}.json"
            output_json_path = f"{intermediates_folder_path}/sim-id-{sim['id']}/debug/{data_type}_{i:06d}.json"

            with open(controller_json_path, 'w') as controller_file:
                json.dump(
                    json.loads(
                        f"""{{
                                "simulationID": {sim['id']},
                                "offline": true,
                                "outputVideoPath": "{config.output_folder_path}/videos/sim-id-{sim['id']}/{data_type}_{i:06d}.mpg",
                                "outputJSONPath": "{output_json_path}",
                                "width":  {sim['width']},
                                "height": {sim['height']},
                                "inputScenePath":  "",
                                "numberOfObjects": 2,
                                "numberOfObstacles": 1,
                                "numberOfPendulums": 1,
                                "stepCount": {sim['step_count']}
                            }}"""),
                    controller_file,
                    indent=4
                )

            # Run simulation.
            run_simulation(config.executable_path, f"{controller_json_path}",
                           f"{intermediates_folder_path}/sim-id-{sim['id']}/debug/cl_debug_{data_type}_{i:06d}.txt")

            # Run its variations.
            variations_output_path = f"{intermediates_folder_path}/sim-id-{sim['id']}/{data_type}_{i:06d}.json"
            variation_run.run_variations(variation_run.init_args(['-exec', config.executable_path,
                                                                  '-c', controller_json_path,
                                                                  '-p', output_json_path,
                                                                  '-o', variations_output_path]))

            questions_file_path = f"{intermediates_folder_path}/sim-id-{sim['id']}/qa_{data_type}_{i:06d}.json"

            # Generate questions.
            try:
                generate_questions.main(
                    generate_questions.parser.parse_args(['--input-scene-file', variations_output_path,
                                                          '--output-questions-file', questions_file_path,
                                                          '--metadata-file', '../svqa/metadata.json',
                                                          '--synonyms-json', '../svqa/synonyms.json',
                                                          '--template-dir', '../svqa/SVQA_1.0_templates']))
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)

            # Add them into dataset.json
            dataset.append(
                json.loads(f"""
                            {{
                                "simulation_id": {sim['id']},
                                "split": {data_type},
                                "video_path": "{config.output_folder_path}/videos/sim-id-{sim['id']}/{data_type}_{i:06d}.mpg",
                                "questions": {json.load(open(questions_file_path, "r"))}
                            }}
                            """)
            )

            json.dump(
                dataset,
                open(f"{config.output_folder_path}/dataset.json", "w"),
                indent=4
            )


def main(args):
    with open(args.configuration_file, 'r') as config_json:
        config = Config(json.loads(config_json.read()))

    generate(config)


if __name__ == "__main__":
    args = init_args()
    print("Running simulations...")
    main(args)
