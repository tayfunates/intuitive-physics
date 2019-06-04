import os, shutil

metadata_path = "..\\all_metadata.txt"
original_path = "/home/burak/Documents/pytorch-CycleGAN-and-pix2pix/datasets/physnet_all/train"
stable_path = "/home/burak/Documents/pytorch-CycleGAN-and-pix2pix/datasets/physnet_stable/train"
unstable_path = "/home/burak/Documents/pytorch-CycleGAN-and-pix2pix/datasets/physnet_unstable/train"

unstable = set()
with open(metadata_path, "r") as metadata:
    for scene in metadata:
        scene_att = scene.split()
        idx = scene_att[0]
        fall = scene_att[18]
        if int(fall):
            unstable.add(idx)

files = os.listdir(original_path)

for file in files:
    img_name, extension = os.path.splitext(file)
    num = img_name.split("_")[2]
    source_path = os.path.join(original_path, file)
    if num in unstable:
        shutil.copy(source_path, unstable_path)
    else:
        shutil.copy(source_path, stable_path)