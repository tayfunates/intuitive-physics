import os
from sklearn.model_selection import train_test_split

root_path ="../datasets/PhysVQA/"
scene_folders = os.listdir(root_path)

test_ratio = 0.2
val_ratio = 0.2

train_test = train_test_split(scene_folders, test_size=test_ratio, shuffle=True)

train = train_test[0]
test = train_test[1]

train_val = train_test_split(train, test_size=val_ratio, shuffle=True)
train = train_test[0]
val = train_test[1]

split_path = "../datasets/PhysVQA/split.txt"

f = open(split_path, "w+")

for scene in train:
    f.write(scene + "\t" + str(1) + "\n")

for scene in val:
    f.write(scene + "\t" + str(2) + "\n")

for scene in test:
    f.write(scene + "\t" + str(3) + "\n")

f.close()