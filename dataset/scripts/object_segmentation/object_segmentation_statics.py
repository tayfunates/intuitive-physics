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


def combine_statics(result_path, min_img_path, mean_img_path, max_img_path):
    all_images = [get_transparent_image(mean_img_path),
                  get_transparent_image(min_img_path),
                  get_transparent_image(max_img_path)]
    m1 = all_images[0]
    i = 1
    for img in all_images[1:]:
        alpha = 120
        img.putalpha(alpha)
        img = make_transparent(img)
        m1.paste(img, (0, 0), img)
        i += 1
    m1.save(result_path)



def combine_statics_from_folder(imgs_folder: str, scene_count: int):
    os.makedirs(imgs_folder+"/static_ss", exist_ok=True)
    os.makedirs(imgs_folder+"static_ss/results", exist_ok=True)
    for sid in range(1, scene_count + 1):
        result_img_name = f'{imgs_folder}/static_ss/results/sid_{sid}_statics_combined.png'
        min_name = f'{imgs_folder}/static_ss/sid_{sid}_min.png'
        mean_name = f'{imgs_folder}/static_ss/sid_{sid}_mean.png'
        max_name = f'{imgs_folder}/static_ss/sid_{sid}_max.png'

        combine_statics(result_img_name, min_name, mean_name, max_name)
        print("CREATED:",result_img_name)


def x():

    exec_path = Path("../../../simulation/2d/SVQA-Box2D/Build/bin/x86_64/Release/Testbed").absolute().as_posix()
    output_folder = "C:/Users/cagatay/OneDrive/Desktop/"
    os.makedirs(output_folder + "/static_ss", exist_ok=True)
    os.makedirs(output_folder + "/new_jsons", exist_ok=True)
    os.makedirs(output_folder + "/static_ss/results", exist_ok=True)


    create_and_save_all_jsons_for_statics(20, output_folder+"static_ss", output_folder+"new_jsons")
    run(output_folder+"new_jsons/", exec_path)
    combine_statics_from_folder("C:/Users/cagatay/OneDrive/Desktop", 20)


if __name__ == '__main__':
    # Specify a folder
    # Make sure exec_path and number_of_scene are correct

    output_folder = "./outputs/"
    exec_path = Path("../../../simulation/2d/SVQA-Box2D/Build/bin/x86_64/Release/Testbed").absolute().as_posix()
    number_of_scene = 20

    os.makedirs(output_folder + "/static_ss", exist_ok=True)
    os.makedirs(output_folder + "/new_jsons", exist_ok=True)
    os.makedirs(output_folder + "/static_ss/results", exist_ok=True)

    create_and_save_all_jsons_for_statics(number_of_scene, output_folder + "static_ss", output_folder + "new_jsons")
    run(output_folder + "new_jsons/", exec_path)
    combine_statics_from_folder(output_folder, number_of_scene)
