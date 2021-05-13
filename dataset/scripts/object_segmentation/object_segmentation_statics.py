import json
import os
import subprocess
from PIL import Image
from pathlib import Path




def get_controller_json_for_statics(min_mean_max_random: str, simulation_id: int, screenshot_output_folder: str):
    return json.loads(
        f"""{{
                "simulationID": {simulation_id},
                "offline": true,
                "outputVideoPath": "output.mpg",
                "outputJSONPath":  "output.json",
                "width": 1024,
                "height": 1024,
                "inputScenePath":  "",
                "includeDynamicObjects": false,
                "screenshotOutputFolder": "{screenshot_output_folder}",
                "staticObjectPositioningType": "{min_mean_max_random}",
                "stepCount": 3
            }}""")


def create_and_save_all_jsons_for_statics(num_of_scenes, screenshot_output_folder: str, new_jsons_output_folder: str):
    res = []
    for scene_id in range(1, num_of_scenes + 1):
        min_ = get_controller_json_for_statics("min", scene_id, screenshot_output_folder)
        mean_ = get_controller_json_for_statics("mean", scene_id, screenshot_output_folder)
        max_ = get_controller_json_for_statics("max", scene_id, screenshot_output_folder)
        res.append(min_)
        res.append(mean_)
        res.append(max_)

        json_name = f"sid_{scene_id}_min.json"
        file = open(new_jsons_output_folder + "/" + json_name, "w")
        file.write(json.dumps(min_, indent=4))
        file.close()

        json_name = f"sid_{scene_id}_mean.json"
        file = open(new_jsons_output_folder + "/" + json_name, "w")
        file.write(json.dumps(mean_, indent=4))
        file.close()

        json_name = f"sid_{scene_id}_max.json"
        file = open(new_jsons_output_folder + "/" + json_name, "w")
        file.write(json.dumps(max_, indent=4))
        file.close()

    return res




def run_simulation(exec_path: str, controller_json_path: str):
    subprocess.call(f"{exec_path} {controller_json_path}", shell=True, universal_newlines=True)


def run(controller_base_path: str, exe_path: str):
    files = os.listdir(controller_base_path)

    for f in files:
        full_controller_path = controller_base_path + "/" + f
        run_simulation(exe_path, full_controller_path)


exec_path = Path("../../../simulation/2d/SVQA-Box2D/Build/bin/x86_64/Release/Testbed").absolute().as_posix()

#create_and_save_all_jsons_for_statics(20,"C:/Users/cagatay/OneDrive/Desktop/static_ss","C:/Users/cagatay/OneDrive/Desktop/new_jsons")
#run("C:/Users/cagatay/OneDrive/Desktop/new_jsons/", exec_path)


def read_img_and_make_transparent(image_path):
    img = Image.open(image_path).convert("RGBA")
    data = img.getdata()
    new_data = []
    for item in data:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)
    return img


def combine_statics(result_path, img1_path, img2_path, img3_path):
    all_images = [read_img_and_make_transparent(img1_path),
                  read_img_and_make_transparent(img2_path),
                  read_img_and_make_transparent(img3_path)]
    m1 = all_images[0]
    i = 1
    for img in all_images[1:]:
        alpha = 120
        img.putalpha(alpha)
        img = read_img_and_make_transparent(img)
        m1.paste(img, (0, 0), img)
        i += 1
    m1.save(result_path)


d = "C:/Users/cagatay/OneDrive/Desktop/"
# combine_statics(d + "result.png", d+"/static_ss/1.png", d+"/static_ss/2.png", d+"/static_ss/3.png")
