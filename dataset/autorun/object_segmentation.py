import json
import os
import subprocess

"""
STEPS
1- read all snaphot.json's
2- create snapshot.json for all individual object
3- create controllers for all snapshots created at step 2
4- run all controllers
"""

## STEP 1
def read_old_snapshots(folder_path: str):
    all_snapshots = list()
    for file_name in os.listdir(folder_path):     # filename: 5_375.json
        full_path = folder_path + "/" + file_name
        sim_id = (file_name[:-5]).split("_")[0]       # simulation_id = 5
        frame = (file_name[:-5]).split("_")[1]        # current_frame = 375

        with open(full_path) as json_file:
            d = dict()
            d["frame"] = frame
            d["simulation_id"] = sim_id
            d["snapshot"] = json.load(json_file)
            all_snapshots.append(d)
    return all_snapshots

## STEP 2

def create_all_combinations_from_one_snapshot(snapshot: dict) -> list:
    shape_list = ["cube", "circle", "triangle"]
    result = []
    for obj in snapshot["objects"]:
        if obj["shape"] in shape_list and obj["size"]   == "large":
            temp = dict()
            temp["directions"] = snapshot["directions"]
            temp["objects"] = [obj]
            result.append(temp)

    return result

def create_all_combinations(all_old_snapshots_dict: list):
    result = []

    for custom_dict in all_old_snapshots_dict:
        actual_snapshot = custom_dict["snapshot"]
        all_comb_from_this_ss = create_all_combinations_from_one_snapshot(actual_snapshot)

        for i in all_comb_from_this_ss:
            d = dict()
            d["frame"] = custom_dict["frame"]
            d["simulation_id"] = custom_dict["simulation_id"]
            d["snapshot"] = i
            result.append(d)

    return result

def write_new_snapshots_to_file(old_snapshots_folder_path: str, new_snapshots_folder_path: str):
    all_old_snapshots = read_old_snapshots(old_snapshots_folder_path)

    arr = create_all_combinations(all_old_snapshots)

    if not os.path.exists(new_snapshots_folder_path):
        os.makedirs(new_snapshots_folder_path)

    for snapshot in arr:
        shape = snapshot["snapshot"]["objects"][0]["shape"]
        size = snapshot["snapshot"]["objects"][0]["size"]
        name = "id" + snapshot["simulation_id"] + "_" + "frame" + snapshot["frame"] + "_" + size + "_" + shape
        f = open(new_snapshots_folder_path + "/" + name + ".json", "w")
        f.write(json.dumps(snapshot["snapshot"],indent=4))
        f.close()





def get_controller_json(base_path: str, controller_name: str, simulation_id: int):
    return json.loads(
        f"""{{
                "simulationID": {simulation_id},
                "offline": true,
                "outputVideoPath": "output.mpg",
                "outputJSONPath":  "output.json",
                "width": 1024,
                "height": 1024,
                "inputScenePath":  "{base_path}/{controller_name}",
                "stepCount": 3
            }}""")


def write_new_controller_to_file(new_snapshots: str, output_folder: str):
    new_controllers = os.listdir(new_snapshots)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for f in new_controllers:
        if f == ".DS_Store":
            continue
        j = get_controller_json(new_snapshots, f, int(f.split("_")[0][2:]) )
        file = open(output_folder + "/" + f , "w")
        file.write(json.dumps(j, indent=4))
        file.close()


def run_simulation(exec_path: str, controller_json_path: str):
    subprocess.call(f"{exec_path} {controller_json_path}", shell=True, universal_newlines=True)


def run(controller_base_path: str, exe_path: str):
    files = os.listdir(controller_base_path)

    for f in files:
        full_controller_path = controller_base_path + "/" +f
        print("RUNNING SIMULATION::" + full_controller_path)
        run_simulation(exe_path, full_controller_path)



def x(old_snapshots_folder: str, new_snapshots_folder: str, new_controllers_folder: str, exec_path: str):
    write_new_snapshots_to_file(old_snapshots_folder, new_snapshots_folder)
    write_new_controller_to_file(new_snapshots_folder, new_controllers_folder)
    run(new_controllers_folder, exec_path)



old_snapshots_folder = "/Users/cagatayyigit/Desktop/snapshots"
new_snapshots_folder = "/Users/cagatayyigit/Desktop/new_snapshots"
new_controllers_folder = "/Users/cagatayyigit/Desktop/new_controllers"
exec_path = "/Users/cagatayyigit/Projects/SVQA-Box2D/Build/bin/x86_64/Release/Testbed"


#x(old_snapshots_folder, new_snapshots_folder,new_controllers_folder , exec_path)



from PIL import Image

img_base_path  = "/Users/cagatayyigit/Desktop/screenshots/"
img1 = Image.open(img_base_path + "id5_frame140_large_circle.png")
img2 = Image.open(img_base_path + "id5_frame510_large_circle.png")





img = Image.blend(img1,img2, 0.9)

#img.show()


def abc():
    result = Image.blend(img1, img2, 0.5)

    files = os.listdir(img_base_path)
    i = 0.0
    for f in files:
        if f == ".DS_Store":
            continue

        new_img = Image.open(img_base_path + f)
        result = Image.blend(new_img, result, 0.5)


    result.show()


