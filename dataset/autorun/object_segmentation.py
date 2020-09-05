import json
import os
import subprocess

def get_all_combinations(snapshot: json) -> list:
    result = []
    python_dict = json.loads(snapshot)
    object_list = python_dict["objects"]
    shape_list = ["cube", "circle"]
    for obj in object_list:
        if obj["shape"] in shape_list:
            temp = dict()
            temp["directions"] = python_dict["directions"]
            temp["objects"] = [obj]
            result.append(json.dumps(temp, indent=4))
    return result


def get_unique_object_name(field: dict, step_count: int) -> str:
    return field["size"] + "_" + field["color"] + "_" + field["shape"] + "_" + str(step_count)


def read_all_snapshot_jsons(path: str) -> list:
    all_snapshot_jsons = []
    for file_name in os.listdir(path):
        full_path = path + "/" + file_name
        frame = int(file_name.split(".")[0][5:])  # filename: frame375.json
        with open(full_path) as json_file:
            all_snapshot_jsons.append([frame, json.load(json_file)])
    return all_snapshot_jsons


def get_all_combinations_with_name(path: str):
    result = []
    for snapshot_json in read_all_snapshot_jsons(path):
        frame = snapshot_json[0]
        ss = snapshot_json[1]

        all_comb = get_all_combinations(json.dumps(ss,indent=4))
        for i in all_comb:
            d = json.loads(i)["objects"]
            name = get_unique_object_name(d[0], frame)
            result.append([name, i])
            print(name)
    return result

def write_to_file(input_path, output_path):
    arr = get_all_combinations_with_name(input_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)


    for snapshot in arr:
        name = snapshot[0]
        snapshot_json = snapshot[1]
        print(name)
        print(snapshot_json)
        f = open(output_path + "/" + name + ".json", "w")
        f.write(snapshot_json)
        f.close()


def get_json(base_path: str, controller_name: str, simulation_id: int):
    return json.loads(
        f"""{{
                "simulationID": {simulation_id},
                "offline": true,
                "outputVideoPath": "output.mpg",
                "outputJSONPath":  "output.json",
                "width": 256,
                "height": 256,
                "inputScenePath":  "{base_path}/{controller_name}",
                "numberOfObjects": 2,
                "numberOfObstacles": 1,
                "numberOfPendulums": 1,
                "stepCount": 1
            }}""")



def write_new_jsons(basepath: str, output_folder: str):
    new_controllers = os.listdir(basepath)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for f in new_controllers:
        j = get_json(basepath,f, simulation_id= 11)
        file = open(output_folder + "/" + f , "w")
        file.write(json.dumps(j))
        file.close()



def run_simulation(exec_path: str, controller_json_path: str):
    subprocess.call(f"{exec_path} {controller_json_path}", shell=True, universal_newlines=True)


def run(controller_base_path: str, exe_path: str):
    files = os.listdir(controller_base_path)

    for f in files:
        full_controller_path = controller_base_path + "/" +f
        print("RUNNING SIMULATION::" + full_controller_path)
        run_simulation(exe_path, controller_base_path)



input_path = "/Users/cagatayyigit/Desktop/snapshots" # this snapshots folders must contains snapshots with name format :  snapshot58.json
output_path = "/Users/cagatayyigit/Desktop/new_snapshots" # new_snapshots is folder name
new_controller_path = "/Users/cagatayyigit/Desktop/newControllers"
exec_path = "/Users/cagatayyigit/Projects/SVQA-Box2D/Build/bin/x86_64/Release/Testbed"



write_new_jsons(output_path, new_controller_path)
run(new_controller_path, exec_path)








