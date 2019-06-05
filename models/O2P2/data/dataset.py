from torch.utils.data import Dataset
import cv2
import numpy as np

class O2P2Dataset(Dataset):

    def __init__(self, dataset, max_objects, transform=None):
        self.dataset = dataset
        self.transform = transform
        self.max_objects = max_objects

    def __getitem__(self, index):
        img0_path, img1_path, mask0_path, mask1_path, seg_paths = self.dataset[index]
        pair_arr_path = [img0_path, img1_path, mask0_path, mask1_path]
        pair_arr_img = []
        for i in range(len(pair_arr_path)):
            img = cv2.imread(pair_arr_path[i])
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pair_arr_img.append(img)

        segs = np.zeros((self.max_objects, 3, pair_arr_img[0].shape[0], pair_arr_img[0].shape[1]), np.float32)
        segs_arr = []

        for seg_path in seg_paths:
            seg = cv2.imread(seg_path)
            seg = cv2.cvtColor(seg, cv2.COLOR_BGR2RGB)
            segs_arr.append(seg)

        if self.transform is not None:
            for i in range(len(pair_arr_img)):
                pair_arr_img[i] = self.transform(pair_arr_img[i])

            for i, seg in enumerate(segs_arr):
                segs[i, :] = self.transform(seg)
        return pair_arr_img[0], pair_arr_img[1], pair_arr_img[2], pair_arr_img[3], segs

    def __len__(self):
        return len(self.dataset)