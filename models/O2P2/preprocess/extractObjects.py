import os
import cv2
import numpy as np
import glob
import shutil
import re

root_path ="../datasets/PhysVQA500/"
scene_folders = os.listdir(root_path)

max_objects_in_a_scene = 12
force_clean = False

noise_remove_kernel = np.ones((3,3),np.uint8)

for scene in scene_folders:
    scene_folder = os.path.join(root_path, scene)
    if os.path.isdir(scene_folder):
        scene_all_repeats = glob.glob(os.path.join(scene_folder, '*FinalUnStable*.png'))
        scene_repeats_segs = [f for f in scene_all_repeats if "NONVisibleSeg" in f]
        scene_repeats_imgs = [f for f in scene_all_repeats if "NONVisibleSeg" not in f and "VisibleSeg" not in f]
        for rp in range(0, len(scene_repeats_segs)):

            repeat = scene_repeats_segs[rp]
            repeat_img = scene_repeats_imgs[rp]

            img = cv2.imread(repeat_img)
            mask = cv2.imread(repeat)
            height, width = img.shape[:2]

            repeat_name = os.path.splitext(os.path.basename(repeat))[0]
            repeat_objects_path = os.path.join(scene_folder, repeat_name+'_objects')

            if force_clean:
                if os.path.exists(repeat_objects_path):
                    shutil.rmtree(repeat_objects_path)

            if not os.path.exists(repeat_objects_path):
                os.makedirs(repeat_objects_path)


            exist_list = [False] * max_objects_in_a_scene
            object_imgs = np.zeros((max_objects_in_a_scene, height, width, 3), np.uint8)

            for i in range(height):
                for j in range(width):
                    (r, g, b) = mask[i, j, :]
                    if r == 0:
                        continue

                    object_imgs[r-1, i, j, :] = img[i, j, :]
                    exist_list[r-1] = True


            disabled_object_index = int(re.search(r'\d+', repeat_name).group())

            for objIndex in range(0, max_objects_in_a_scene):
                if exist_list[objIndex] and objIndex != disabled_object_index:
                    obj_path = os.path.join(repeat_objects_path, str(objIndex) + '.png')
                    raw_image = object_imgs[objIndex, :]
                    object_image = cv2.morphologyEx(raw_image, cv2.MORPH_OPEN, noise_remove_kernel)
                    cv2.imwrite(obj_path, object_image)

