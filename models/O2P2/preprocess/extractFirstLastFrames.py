import os
import cv2
#from PIL import Image

root = "D:\\data\\physnet\\blocks_real\\block_camera_combined_scaled2\\mask_order"

files = os.listdir(root)

cropped_width = 224
cropped_height = 224

for file in files:
    full_path = os.path.join(root, file)
    img_name, extension = os.path.splitext(file)
    scene = Image.open(full_path, mode='r')
    width, height = scene.size
    #scene = cv2.imread(full_path)
    #first_frame = scene[0: cropped_height, :]
    #last_frame = scene[-cropped_height:, :]
    first_frame = scene.crop((0, 0, cropped_width, cropped_height))
    last_frame = scene.crop((0, height - cropped_height, cropped_width, height))
    first_frame_name = img_name + "_first" + extension
    last_frame_name = img_name + "_last" + extension
    first_frame_path = os.path.join(root, first_frame_name)
    last_frame_path = os.path.join(root, last_frame_name)
    #cv2.imwrite(first_frame_path, first_frame)
    #cv2.imwrite(last_frame_path, last_frame)
    first_frame.save(first_frame_path)
    last_frame.save(last_frame_path)
