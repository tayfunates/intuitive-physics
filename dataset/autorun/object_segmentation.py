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


def get_static_objects(old_json_folder_path,new_json_folder_path):
    p = old_json_folder_path + "/" + os.listdir(old_json_folder_path)[0]

    file = open(p , "r")
    snapshot = json.loads(file.read())
    file.close()

    shape_list = ["cube", "circle", "triangle"]

    temp = dict()
    temp["directions"] = snapshot["directions"]
    temp["objects"] = []
    for obj in snapshot["objects"]:
        if obj["shape"] not in shape_list:
            temp["objects"].append(obj)


    f = open(new_json_folder_path + "/idstatic.json" , "w")
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
        name = "id" + snapshot["simulation_id"] + "_" + "frame" + snapshot["frame"] + "_" + size + "_" +color + "_" + shape
        f = open(new_snapshots_folder_path + "/" + name + ".json", "w")
        f.write(json.dumps(snapshot["snapshot"],indent=4))
        f.close()

    get_static_objects(old_snapshots_folder_path, new_snapshots_folder_path)




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

    sim_id = int(new_controllers[0].split("_")[0][2:])
    for f in new_controllers:
        if f == ".DS_Store":
            continue
        if f == "static.json":
            j = get_controller_json(new_snapshots, "id_"+ f, sim_id)
            file = open(output_folder + "/" + f, "w")
            file.write(json.dumps(j, indent=4))
            file.close()
        j = get_controller_json(new_snapshots, f, sim_id )
        file = open(output_folder + "/" + f , "w")
        file.write(json.dumps(j, indent=4))
        file.close()


def run_simulation(exec_path: str, controller_json_path: str):
    subprocess.call(f"{exec_path} {controller_json_path}", shell=True, universal_newlines=True)


def run(controller_base_path: str, exe_path: str):
    files = os.listdir(controller_base_path)

    for f in files:
        full_controller_path = controller_base_path + "/" +f
        #print("RUNNING SIMULATION::" + full_controller_path)
        run_simulation(exe_path, full_controller_path)



def x(old_snapshots_folder: str, new_snapshots_folder: str, new_controllers_folder: str, exec_path: str):
    write_new_snapshots_to_file(old_snapshots_folder, new_snapshots_folder)
    write_new_controller_to_file(new_snapshots_folder, new_controllers_folder)
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



img_base_path  = "/Users/cagatayyigit/Desktop/screenshots/"


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
        for frame in frame_arr: # id5_frame10_large_cyan_circle.png"
            full_path = base_path + str(sim_id) + "_frame" + str(frame) + "_" + str(shape) + ".png"
            print("Loaded:"+str(count) + "/" + str(total) + "  -->>" + full_path)
            count += 1
            result.append([get_transparent_image(full_path), frame])

    return [result,len(frame_arr)]

def combine():
    m1 = get_transparent_image("/Users/cagatayyigit/Desktop/screenshots/idstatic.png")
    images, frame_per_object = get_all_image("/Users/cagatayyigit/Desktop/screenshots/")
    i = int(255 / frame_per_object)
    j = 1
    for img in images:
        img[0].putalpha(i * (j + 10))
        img[0] = make_transparent(img[0])
        m1.paste(img[0], (0,0), img[0])
        if j < frame_per_object:
            j += 1
        else:
            j = 1
    m1.show()
    m1.save("/Users/cagatayyigit/Desktop/result.png")




old_snapshots_folder = "/Users/cagatayyigit/Desktop/snapshots"
new_snapshots_folder = "/Users/cagatayyigit/Desktop/new_snapshots"
new_controllers_folder = "/Users/cagatayyigit/Desktop/new_controllers"
exec_path = "/Users/cagatayyigit/Projects/SVQA-Box2D/Build/bin/x86_64/Release/Testbed"

#run_simulation(exec_path, controller_json_path: str):

#x(old_snapshots_folder, new_snapshots_folder,new_controllers_folder, exec_path)
#combine()



def create_different_static_object(count):
    for i in range(count):
        run_simulation(exec_path, "/Users/cagatayyigit/Projects/SVQA-Box2D/Testbed/controller.json")

#create_different_static_object(100)

def mapFromTo(x,a,b,c,d):

    """
    x:input value;
    a,b:input range
    c,d:output range
    y:return value

    """
    y = (x - a) / (b - a) * (d - c) + c
    return int(y)


def combine_statics():
    files = os.listdir("/Users/cagatayyigit/Desktop/static_ss/")
    all_images = []
    for i in files:
        if i != ".DS_Store":
            all_images.append(get_transparent_image("/Users/cagatayyigit/Desktop/static_ss/" + str(i)))

    size = len(all_images)
    alpha_diff = int(255 / (size))
    m1 = all_images[0]
    i = 1
    for img in all_images:
        alpha = mapFromTo(i,1,size,0,255)
        img.putalpha(alpha)
        img= make_transparent(img)
        m1.paste(img, (0, 0), img)
        i += 1

    m1.show()
    m1.save("/Users/cagatayyigit/Desktop/result.png")

combine_statics()