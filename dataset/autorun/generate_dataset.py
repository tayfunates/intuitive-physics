import argparse
import glob
import json
import os
import subprocess
import pathlib
import sys
import traceback

import numpy as np
import time
import logging

import autorun.variation_run as variation_run
import svqa.generate_questions as generate_questions
import autorun.dataset_utils as dataset_utils

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
  - dataset.json            (This json file contains all the video paths, and questions generated from the outputs.)
"""


class Config(object):
    def __init__(self, config_dict):
        self.dataset_size = config_dict['dataset_size']
        self.executable_path = os.path.abspath(config_dict['executable_path']).replace("\\", "/")
        self.output_folder_path = os.path.abspath(config_dict['output_folder_path']).replace("\\", "/")
        self.test_set_ratio = config_dict['test_set_ratio']
        self.validation_set_ratio = config_dict['validation_set_ratio']
        self.train_set_ratio = config_dict['train_set_ratio']
        self.sim_ids_for_each_split = config_dict['sim_ids_for_each_split']
        self.simulation_configs = config_dict['simulation_configs']
        self.offline = config_dict['offline']


def init_args():
    parser = argparse.ArgumentParser()

    """
    Example configuration file content is as follows:
        {
          "dataset_size": 1000,
          "executable_path": "../../simulation/2d/SVQA-Box2D/Build/bin/x86_64/Release/Testbed",
          "output_folder_path": "dataset1000/",
          "train_set_ratio": 0.6,
          "validation_set_ratio": 0.2,
          "test_set_ratio": 0.2,
          "sim_ids_for_each_split": {
            "train": [1], 
            "validation": [1,2],
            "test": [1,2]
          },
          "simulation_configs": [
            {
              "id": 1,
              "excluded_task_ids": null,
              "step_count": 600,
              "width": 256,
              "height": 256
            },
            {
              "id": 2,
              "excluded_task_ids": [
                "('enable.json', 0)",
                "('enable.json', 1)",
                "('enable.json', 2)",
                "('enable.json', 3)"
              ],
              "step_count": 600,
              "width": 256,
              "height": 256
            }
          ]
        }
        
    If "excluded_task_ids" are null, then all tasks in all template files will be used to generate questions for that scene.
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
    # TODO: Find if debug_output_path is None, print to console.
    subprocess.call(f"{exec_path} {controller_json_path}", shell=True, universal_newlines=True,
                    stdout=open(
                        f"{pathlib.Path(controller_json_path).parent}/cl_debug_{pathlib.Path(controller_json_path).name.replace('.json', '.txt').replace('controller_', '').replace('_controller', '')}".replace(
                            "\\", "/"), "w")
                    if debug_output_path is None
                    else open(debug_output_path, "w"))


def generate(config: Config):
    """
    Generates a dataset with parameters specified in the configuration file.
    """
    os.makedirs(config.output_folder_path, exist_ok=True)

    dataset = json.loads("[]")

    # To print statistics about generated questions.
    generated_questions = {"train": [], "validation": [], "test": []}

    json.dump(
        dataset,
        open(f"{config.output_folder_path}/dataset.json", "w"),
        indent=4
    )

    intermediates_folder_path = f"{config.output_folder_path}/intermediates"
    for sim in config.simulation_configs:
        os.makedirs(f"{intermediates_folder_path}/sim-id-{sim['id']}/debug", exist_ok=True)
        os.makedirs(f"{config.output_folder_path}/videos/sim-id-{sim['id']}", exist_ok=True)

    train = int(float(config.train_set_ratio) * config.dataset_size)
    val = int(float(config.validation_set_ratio) * config.dataset_size)
    test = int(float(config.test_set_ratio) * config.dataset_size)

    train_simulations = config.sim_ids_for_each_split["train"]
    validation_simulations = config.sim_ids_for_each_split["validation"]
    test_simulations = config.sim_ids_for_each_split["test"]

    # If no simulation id specified for a split, use all.
    if train_simulations is None:
        train_simulations = [config["id"] for config in config.simulation_configs]
    if validation_simulations is None:
        validation_simulations = [config["id"] for config in config.simulation_configs]
    if test_simulations is None:
        test_simulations = [config["id"] for config in config.simulation_configs]

    # Breakup split ratios to each scene ID.
    splits = [("train", sid) for sid in train_simulations * (train // len(train_simulations))]
    splits.extend([("validation", sid) for sid in validation_simulations] * (val // len(validation_simulations)))
    splits.extend([("test", sid) for sid in test_simulations] * (test // len(test_simulations)))

    # To measure remaining time.
    start_time = time.time()
    times = np.array([])
    for i in range(len(splits)):
        t1 = time.time()  # To measure remaining time.

        split_v_id = splits[i]
        split = split_v_id[0]
        sim = next((x for x in config.simulation_configs if x['id'] == split_v_id[1]), None)
        assert sim is not None, f"Specified simulation ID ({split_v_id[1]}) in 'sim_ids_for_each_split' " \
                                f"isn't present in 'simulation_configs'."
        logging.info(f"Running, split: {split}, sim_id: {sim['id']}, N: {i:06d}")

        # Create controller file.
        controller_json_path = f"{intermediates_folder_path}/sim-id-{sim['id']}/debug/controller_{split}_{i:06d}.json"
        output_json_path = f"{intermediates_folder_path}/sim-id-{sim['id']}/debug/{split}_{i:06d}.json"

        with open(controller_json_path, 'w') as controller_file:
            json.dump(
                json.loads(
                    f"""{{
                            "simulationID": {sim['id']},
                            "offline": {str(config.offline).lower()},
                            "outputVideoPath": "{config.output_folder_path}/videos/sim-id-{sim['id']}/{split}_{i:06d}.mpg",
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
                       f"{intermediates_folder_path}/sim-id-{sim['id']}/debug/cl_debug_{split}_{i:06d}.txt")

        # Run its variations.
        variations_output_path = f"{intermediates_folder_path}/sim-id-{sim['id']}/{split}_{i:06d}.json"
        variation_run.run_variations(variation_run.init_args(['-exec', config.executable_path,
                                                              '-c', controller_json_path,
                                                              '-p', output_json_path,
                                                              '-o', variations_output_path]))

        questions_file_path = f"{intermediates_folder_path}/sim-id-{sim['id']}/qa_{split}_{i:06d}.json"

        # Generate questions.
        try:
            questions = generate_questions.main(
                generate_questions.parser.parse_args(['--input-scene-file', variations_output_path,
                                                      '--output-questions-file', questions_file_path,
                                                      '--metadata-file', '../svqa/metadata.json',
                                                      '--synonyms-json', '../svqa/synonyms.json',
                                                      '--template-dir', '../svqa/SVQA_1.0_templates',
                                                      '--restrict-template-count-per-video', False,
                                                      '--print-stats', False,
                                                      '--excluded-task-ids', sim["excluded_task_ids"]]))
            generated_questions[split].extend(questions)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)

        # Add them into dataset.json
        dataset.append(
            json.loads(f"""{{
                            "simulation_id": "{sim['id']}",
                            "split": "{split}",
                            "video_path": "{config.output_folder_path}/videos/sim-id-{sim['id']}/{split}_{i:06d}.mpg",
                            "questions": {json.dumps(json.load(open(questions_file_path, "r")))}
                        }}""")
        )

        json.dump(
            dataset,
            open(f"{config.output_folder_path}/dataset.json", "w"),
            indent=2
        )

        diff = time.time() - t1
        times = np.append(times, diff)
        logging.info(f"Approx. {round((np.mean(times) * (len(splits) - i - 1)) / 60, 2)} "
                     "minutes remaining...".ljust(75, " "))

    logging.info(f"Dataset generation is complete. Process took {round((time.time() - start_time) / 60, 2)} minutes.")

    # Print questions and answer frequencies for each template in the generated dataset.
    for split in ["train", "validation", "test"]:
        logging.info(f"Answers for split: {split}")
        table = generate_questions.get_answer_frequencies(
            generate_questions.convert_to_question_tuple_list(generated_questions[split]))
        logging.info(f"{os.linesep}"
                     f"{table}")

    dataset = dataset_utils.relativize_paths(dataset, config.output_folder_path)

    json.dump(
        dataset,
        open(f"{config.output_folder_path}/dataset.json", "w"),
        indent=2
    )

    # Dump minimal version of the dataset for easier debugging.
    json.dump(
        dataset_utils.minimized_dataset(dataset),
        open(f"{config.output_folder_path}/dataset_minimal.json", "w"),
        indent=2
    )


def main(args):
    logging.basicConfig(
        level=logging.NOTSET,
        format='[%(levelname)s]\t%(asctime)s\t%(message)s',
        handlers=[logging.FileHandler("dataset_generation.log"), logging.StreamHandler(sys.stdout)])

    logging.info("Opening dataset generation configuration file.")
    with open(args.configuration_file, 'r') as config_json:
        s = config_json.read()
        config = Config(json.loads(s))
        logging.debug(f"Configuration:{os.linesep}{s}")

    logging.info("Running simulations...")
    generate(config)


if __name__ == "__main__":
    args = init_args()
    main(args)
