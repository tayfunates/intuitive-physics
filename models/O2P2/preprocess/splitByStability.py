metadata_path = "..\\datasets\\PhysNetReal\\all_metadata.txt"
split_path = "..\\datasets\\PhysNetReal\\split_only_unstable.txt"

unstable = set()
scene_count = 0
with open(metadata_path, "r") as metadata:
    for scene in metadata:
        scene_count += 1
        scene_att = scene.split()
        idx = scene_att[0]
        fall = scene_att[18]
        if int(fall):
            unstable.add(int(idx))

unstable_scene_count = len(unstable)
num_train = round(unstable_scene_count * 0.8)
num_val = round(unstable_scene_count * 0.1)
num_test = unstable_scene_count - num_train - num_val

f = open(split_path, "w+")

count_unstables_added = 0

for scene in range(scene_count):
    if scene+1 in unstable:
        if count_unstables_added < num_train:
            split = 1
        elif count_unstables_added < num_train + num_val:
            split = 2
        else:
            split = 3
        count_unstables_added += 1
    else:
        split = 0
    f.write(str(scene+1) + "\t" + str(split) + "\n")
f.close()
