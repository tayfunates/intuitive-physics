import os
import cv2
import numpy as np

root_path ="../datasets/PhysNetReal/All/"
images_path = os.path.join(root_path, "First")
masks_path = os.path.join(root_path, "Mask")
segments_path = os.path.join(root_path, "Segment")

image_files = os.listdir(images_path)

for image_file in image_files:
    img_name, extension = os.path.splitext(image_file)
    img_num = img_name.split("_")[2]
    mask_file = "mask_order_" + img_num + "_first.png"
    img_path = os.path.join(images_path, image_file)
    mask_path = os.path.join(masks_path, mask_file)
    img = cv2.imread(img_path)
    mask = cv2.imread(mask_path)
    height, width = img.shape[:2]
    obj_1_name = "imgseg_" + img_num + "_A.png"
    obj_2_name = "imgseg_" + img_num + "_B.png"
    obj_3_name = "imgseg_" + img_num + "_C.png"
    obj_4_name = "imgseg_" + img_num + "_D.png"
    obj_1_path = os.path.join(segments_path, obj_1_name)
    obj_2_path = os.path.join(segments_path, obj_2_name)
    obj_3_path = os.path.join(segments_path, obj_3_name)
    obj_4_path = os.path.join(segments_path, obj_4_name)
    obj_1 = np.zeros((height, width, 3), np.uint8)
    obj_2 = np.zeros((height, width, 3), np.uint8)
    obj_3 = np.zeros((height, width, 3), np.uint8)
    obj_4 = np.zeros((height, width, 3), np.uint8)
    obj_3_exists = False
    obj_4_exists = False
    for i in range(height):
        for j in range(width):
            (r, g, b) = mask[i, j, :]
            if r == 0:
                pass
            elif r == 1:
                obj_1[i, j, :] = img[i, j, :]
            elif r == 2:
                obj_2[i, j, :] = img[i, j, :]
            elif r == 3:
                obj_3[i, j, :] = img[i, j, :]
                obj_3_exists = True
            elif r == 4:
                obj_4[i, j, :] = img[i, j, :]
                obj_4_exists = True
            else:
                print("Unexpected mask!")

    cv2.imwrite(obj_1_path, obj_1)
    cv2.imwrite(obj_2_path, obj_2)
    if obj_3_exists:
        cv2.imwrite(obj_3_path, obj_3)
    if obj_4_exists:
        cv2.imwrite(obj_4_path, obj_4)

