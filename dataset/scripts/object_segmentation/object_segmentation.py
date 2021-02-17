import json
import os
import subprocess
from pathlib import Path

from loguru import logger

from framework.utils import FileIO, ParallelProcessor

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
    for file_name in os.listdir(folder_path):  # filename: 5_375.json
        full_path = folder_path + "/" + file_name
        sim_id = (file_name[:-5]).split("_")[0]  # simulation_id = 5
        frame = (file_name[:-5]).split("_")[1]  # current_frame = 375

        if file_name == ".DS_Store":
            continue
        with open(full_path) as json_file:

            d = dict()
            d["frame"] = frame
            d["simulation_id"] = sim_id
            d["snapshot"] = json.load(json_file)
            all_snapshots.append(d)
    return all_snapshots


## STEP 2
"""
"direction :
"objects": []
"""


def create_all_combinations_from_one_snapshot(snapshot: dict) -> list:
    shape_list = ["cube", "circle", "triangle"]
    result = []
    for obj in snapshot["objects"]:
        if obj["shape"] in shape_list:
            temp = dict()
            temp["directions"] = snapshot["directions"]
            temp["objects"] = [obj]
            result.append(temp)

    return result


def get_static_objects(old_json_folder_path, new_json_folder_path):
    p = old_json_folder_path + "/" + os.listdir(old_json_folder_path)[0]

    file = open(p, "r")
    snapshot = json.loads(file.read())
    file.close()

    shape_list = ["cube", "circle", "triangle"]

    temp = dict()
    temp["directions"] = snapshot["directions"]
    temp["objects"] = []
    for obj in snapshot["objects"]:
        if obj["shape"] not in shape_list:
            temp["objects"].append(obj)

    f = open(new_json_folder_path + "/idstatic.json", "w")
    f.write(json.dumps(temp, indent=4))
    f.close()
    return temp


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
        color = snapshot["snapshot"]["objects"][0]["color"]
        name = "id" + snapshot["simulation_id"] + "_" + "frame" + snapshot[
            "frame"] + "_" + size + "_" + color + "_" + shape
        f = open(new_snapshots_folder_path + "/" + name + ".json", "w")
        f.write(json.dumps(snapshot["snapshot"], indent=4))
        f.close()

    get_static_objects(old_snapshots_folder_path, new_snapshots_folder_path)


def get_controller_json(base_path: str, controller_name: str, simulation_id: int,
                        screenshot_output_folder="", snapshot_output_folder=""):
    return json.loads(
        f"""{{
                "simulationID": {simulation_id},
                "offline": true,
                "outputVideoPath": "output.mpg",
                "outputJSONPath":  "output.json",
                "width": 1024,
                "height": 1024,
                "inputScenePath":  "{base_path}/{controller_name}",
                "screenshotOutputFolder": "{screenshot_output_folder}",
                "snapshotOutputFolder": "{snapshot_output_folder}",
                "stepCount": 3
            }}""")


def write_new_controller_to_file(new_snapshots: str, output_folder: str, screenshots_folder):
    new_controllers = os.listdir(new_snapshots)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    sim_id = int(new_controllers[0].split("_")[0][2:])
    for f in new_controllers:
        if f == ".DS_Store":
            continue
        if f == "static.json":
            j = get_controller_json(new_snapshots, "id_" + f, sim_id)
            file = open(output_folder + "/" + f, "w")
            file.write(json.dumps(j, indent=4))
            file.close()
        j = get_controller_json(new_snapshots, f, sim_id, screenshot_output_folder=screenshots_folder + "/dynamics_ss/")
        file = open(output_folder + "/" + f, "w")
        file.write(json.dumps(j, indent=4))
        file.close()


def run_simulation(exec_path: str, controller_json_path: str, working_dir=None):
    subprocess.call(f"{exec_path} {controller_json_path}", shell=True, cwd=working_dir, universal_newlines=True)


def run(controller_base_path: str, exe_path: str, working_dir=None):
    files = os.listdir(controller_base_path)

    for f in files:
        full_controller_path = controller_base_path + "/" + f
        # print("RUNNING SIMULATION::" + full_controller_path)
        run_simulation(exe_path, full_controller_path, working_dir=working_dir )


def produce_snapshots_and_controllers(old_snapshots_folder: str, new_snapshots_folder: str, new_controllers_folder: str,
                                      exec_path: str, screenshots_folder):
    logger.info("Creating snapshots")
    write_new_snapshots_to_file(old_snapshots_folder, new_snapshots_folder)
    logger.info("Fragmenting controllers")
    write_new_controller_to_file(new_snapshots_folder, new_controllers_folder, screenshots_folder)
    logger.info("Running simulations")
    run(new_controllers_folder, exec_path)


from PIL import Image


def make_transparent(img):
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    return img


def get_transparent_image(image_path):
    return make_transparent(Image.open(image_path).convert("RGBA"))


def get_all_image(base_path):
    result = []
    files = os.listdir(base_path)
    filenames = []
    sim_id = ""
    frames = dict()
    shape = dict()
    for f in files:
        if f == ".DS_Store":
            continue
        if f == "idstatic.png":
            continue
        sim_id = str(f.split("_")[0])
        frm = str(f.split("_")[1][5:])

        shp = str(f.split("_")[2]) + "_" + str(f.split("_")[3]) + "_" + str(f.split("_")[4][:-4])

        if frm not in frames:
            frames[frm] = 1
        if shp not in shape:
            shape[shp] = 1
    frame_arr = []
    for k in frames.keys():
        frame_arr.append(int(k))
    frame_arr.sort()

    shape_arr = []
    for k in shape.keys():
        shape_arr.append((k))

    count = 1
    total = len(shape_arr) * len(frame_arr)
    for shape in shape_arr:
        for frame in frame_arr:  # id5_frame10_large_cyan_circle.png"
            full_path = base_path + str(sim_id) + "_frame" + str(frame) + "_" + str(shape) + ".png"
            print("Loaded:" + str(count) + "/" + str(total) + "  -->>" + full_path)
            count += 1
            result.append([get_transparent_image(full_path), frame])

    return [result, len(frame_arr)]


def combine(screenshots_folder):
    m1 = get_transparent_image(f"{screenshots_folder}/dynamics_ss/idstatic.png")
    images, frame_per_object = get_all_image(f"{screenshots_folder}/dynamics_ss/")
    i = int(255 / frame_per_object)
    j = 1
    for img in images:
        img[0].putalpha(i * (j + 10))
        img[0] = make_transparent(img[0])
        m1.paste(img[0], (0, 0), img[0])
        if j < frame_per_object:
            j += 1
        else:
            j = 1
    m1.show()
    m1.save(f"./{screenshots_folder}_combined.png")


def object_segmentation(video_index: int):
    old_snapshots_folder = str(Path(f"./{video_index}_snapshots/").absolute().as_posix())
    new_snapshots_folder = str(Path(f"./{video_index}_new_snapshots/").absolute().as_posix())
    new_controllers_folder = str(Path(f"./{video_index}_new_controllers/").absolute().as_posix())
    new_screenshots_folder = str(Path(f"./{video_index}_screenshots/").absolute().as_posix())
    new_screenshots_folder_dynamic = str(Path(f"./{video_index}_screenshots/dynamics_ss").absolute().as_posix())

    os.makedirs(old_snapshots_folder, exist_ok=True)
    os.makedirs(new_snapshots_folder, exist_ok=True)
    os.makedirs(new_controllers_folder, exist_ok=True)
    os.makedirs(new_screenshots_folder, exist_ok=True)
    os.makedirs(new_screenshots_folder_dynamic, exist_ok=True)

    input_scene_path = str(Path(f"./run/{video_index:06}.json").absolute().as_posix())
    exec_path = Path("../../../simulation/2d/SVQA-Box2D/Build/bin/x86_64/Release/Testbed").absolute().as_posix()
    working_directory = Path("../../../simulation/2d/SVQA-Box2D/Testbed").absolute().as_posix()

    simulation_id = int(str(video_index)[3]) + 1
    cj = json.loads(
        f"""{{
                    "simulationID": {simulation_id},
                    "offline": false,
                    "outputVideoPath": "output.mpg",
                    "outputJSONPath":  "output.json",
                    "width": 256,
                    "height": 256,
                    "inputScenePath":  "{input_scene_path}",
                    "snapshotOutputFolder": "{old_snapshots_folder}/",
                    "stepCount": 600
                }}""")

    os.makedirs(Path("./run/controllers/").absolute().as_posix(), exist_ok=True)
    controller_path = Path(f"./run/controllers/{video_index}_controller.json").absolute().as_posix()
    FileIO.write_json(cj, controller_path)
    run_simulation(exec_path, controller_path, working_dir=working_directory)
    produce_snapshots_and_controllers(old_snapshots_folder, new_snapshots_folder, new_controllers_folder, exec_path,
                                      new_screenshots_folder)
    combine(new_screenshots_folder)


if __name__ == '__main__':
    # Create a directory named "run" on cwd, and add inside the scene output jsons that
    # will be used for object segmentation.
    # Make sure exec_path in object_segmentation function is correct
    files = os.listdir("./run")

    jobs = []
    args = []

    for fn in files:
        if ("controllers" not in fn) and ("DS_Store" not in fn):
            jobs.append(object_segmentation)
            args.append([int(fn.split(".")[0][2:])])

    parallel_processor = ParallelProcessor(jobs, args)

    logger.info("Forking processes into parallel")

    parallel_processor.fork_processes()
    logger.info("Starting all parallel processes")

    parallel_processor.start_all()
    logger.info("Waiting for parallel processes to finish")

    parallel_processor.join_all()

    logger.info("Finished.")
