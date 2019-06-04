import os, shutil

metadata_path = "..\\all_metadata.txt"
original_path = "/home/burak/Documents/pytorch-CycleGAN-and-pix2pix/datasets/physnet_234"
path2 = "/home/burak/Documents/pytorch-CycleGAN-and-pix2pix/datasets/physnet_2"
path3 = "/home/burak/Documents/pytorch-CycleGAN-and-pix2pix/datasets/physnet_3"
path4 = "/home/burak/Documents/pytorch-CycleGAN-and-pix2pix/datasets/physnet_4"
path23 = "/home/burak/Documents/pytorch-CycleGAN-and-pix2pix/datasets/physnet_23"
path24 = "/home/burak/Documents/pytorch-CycleGAN-and-pix2pix/datasets/physnet_24"

block2 = set()
block3 = set()
block4 = set()
with open(metadata_path, "r") as metadata:
    for scene in metadata:
        scene_att = scene.split()
        idx = scene_att[0]
        block_color3 = scene_att[16]
        block_color4 = scene_att[17]
        if int(block_color4) != 0:
            block4.add(idx)
        elif int(block_color3) != 0:
            block3.add(idx)
        else:
            block2.add(idx)

files = os.listdir(original_path)

for file in files:
    img_name, extension = os.path.splitext(file)
    num = img_name.split("_")[2]
    source_path = os.path.join(original_path, file)
    if num in block4:
        shutil.copy(source_path, path4)
        shutil.copy(source_path, path24)
    elif num in block3:
        shutil.copy(source_path, path3)
        shutil.copy(source_path, path23)
    else:
        shutil.copy(source_path, path2)
        shutil.copy(source_path, path23)
        shutil.copy(source_path, path24)