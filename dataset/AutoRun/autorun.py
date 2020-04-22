import sys
import argparse
import json
import subprocess
import os
import glob

parser = argparse.ArgumentParser()

args = None

sim_id_to_step_count = {
    0: 600,
    1: 1200
}


def get_json(data_type: str, simulation_id: int, controller_id: int):
    return json.loads(
        f"""{{
                "simulationID": {simulation_id},
                "offline": true,
                "outputVideoPath": "outputs/{data_type}_{controller_id}.mpg",
                "outputJSONPath":  "outputs/{data_type}_{controller_id}.json",
                "width": 1024,
                "height": 640,
                "inputScenePath":  "",
                "numberOfObjects": 2,
                "numberOfObstacles": 1,
                "numberOfPendulums": 1,
                "stepCount": {sim_id_to_step_count[simulation_id]}
            }}""")


def construct_jsons(run_count: int, simulation_id: int):
    test = float(args.test_set_ratio) * int(run_count)
    val = float(args.validation_set_ratio) * int(run_count)
    train = float(args.train_set_ratio) * int(run_count)

    if not os.path.exists("controllers"):
        os.makedirs("controllers")

    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    for i in range(int(test)):
        controller_json_path = f"controllers/controller_test_{i:06d}.json"
        with open(controller_json_path, 'w') as the_file:
            json.dump(get_json("test", simulation_id, f"{i:06d}"), the_file, indent=4)

    for i in range(int(val)):
        controller_json_path = f"controllers/controller_val_{i:06d}.json"
        with open(controller_json_path, 'w') as the_file:
            json.dump(get_json("val", simulation_id, f"{i:06d}"), the_file, indent=4)

    for i in range(int(train)):
        controller_json_path = f"controllers/controller_train_{i:06d}.json"
        with open(controller_json_path, 'w') as the_file:
            json.dump(get_json("train", simulation_id, f"{i:06d}"), the_file, indent=4)


def get_controller_json_path(data_type: str, controller_id: int):
    return f"controllers/controller_{data_type}_{controller_id:06d}"


def run_simulation(exec_path: str, controller_json_path: str):
    subprocess.call(f"{exec_path} {controller_json_path}", shell=True, universal_newlines=True)


def run_all_simulations():
    base_full_path = os.getcwd()
    controller_filenames = [c for c in glob.glob("./controllers/*.json")]

    for name in controller_filenames:
        print(f"Running: {base_full_path}/{name}")
        run_simulation(args.exec_path, f"{base_full_path}/{name}")


def main():
    construct_jsons(int(args.number_of_runs), int(args.simulation_id))
    run_all_simulations()


def init_args():
    parser.add_argument('--executable-path', action='store', dest='exec_path', required=False, nargs='?', type=str,
                        default="\"../../Build/bin/x86_64/Release/Testbed\"",
                        help='Testbed executable path.')

    parser.add_argument('--simulation-id', action='store', dest='simulation_id', required=True,
                        help='Simulation id.')

    parser.add_argument('--number-of-runs', action='store', dest='number_of_runs', required=True,
                        help='Number of simulation runs.')

    parser.add_argument('--test-set-ratio', action='store', dest='test_set_ratio', required=True,
                        help='Test dataset ratio.')

    parser.add_argument('--validation-set-ratio', action='store', dest='validation_set_ratio', required=True,
                        help='Validation dataset ratio.')

    parser.add_argument('--train-set-ratio', action='store', dest='train_set_ratio', required=True,
                        help='Train dataset ratio.')

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    global args
    args = parser.parse_args()


if __name__ == "__main__":
    init_args()
    print("Running simulations...")
    main()
