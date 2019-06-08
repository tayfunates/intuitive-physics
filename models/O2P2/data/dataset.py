from torch.utils.data import Dataset
import cv2
import numpy as np

class O2P2Dataset(Dataset):

    def __init__(self, dataset, max_objects, images_reside_in_memory, transform=None):
        self.dataset = dataset
        self.transform = transform
        self.max_objects = max_objects
        self.images_reside_in_memory = images_reside_in_memory

    def __getitem__(self, index):

        # If Want to Use Whole Mask
        #img0, img1, mask0, mask1, segs = self.dataset[index]
        img0, img1, seg_imgs = self.dataset[index]

        # If Want to Use Whole Mask
        #pair_arr = [img0, img1, mask0, mask1]
        pair_arr = [img0, img1]

        pair_arr_img = []
        for i in range(len(pair_arr)):

            if self.images_reside_in_memory == True:
                img = pair_arr[i]
            else:
                img = cv2.imread(pair_arr[i])

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pair_arr_img.append(img)

        segs = np.zeros((self.max_objects, 3, pair_arr_img[0].shape[0], pair_arr_img[0].shape[1]), np.float32)
        segs_arr = []

        for seg_i in seg_imgs:
            if self.images_reside_in_memory == True:
                seg = seg_i
            else:
                seg = cv2.imread(seg_i)

            seg = cv2.cvtColor(seg, cv2.COLOR_BGR2RGB)
            segs_arr.append(seg)

        if self.transform is not None:
            for i in range(len(pair_arr_img)):
                pair_arr_img[i] = self.transform(pair_arr_img[i])

            for i, seg in enumerate(segs_arr):
                segs[i, :] = self.transform(seg)

        #If Want to Use Whole Mask
        #return pair_arr_img[0], pair_arr_img[1], pair_arr_img[2], pair_arr_img[3], segs
        return pair_arr_img[0], pair_arr_img[1], segs

    def __len__(self):
        return len(self.dataset)