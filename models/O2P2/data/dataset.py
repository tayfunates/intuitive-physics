from torch.utils.data import Dataset
import cv2
import numpy as np

class O2P2Dataset(Dataset):

    def __init__(self, dataset, max_objects, transform=None):
        self.dataset = dataset
        self.transform = transform
        self.max_objects = max_objects

    def __getitem__(self, index):
        img0_path, img1_path, seg_paths = self.dataset[index]
        img0 = cv2.imread(img0_path)
        img0 = cv2.cvtColor(img0, cv2.COLOR_BGR2RGB)
        img1 = cv2.imread(img1_path)
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        segs = np.zeros((self.max_objects, 3, img0.shape[0], img0.shape[1]), np.float32)
        segs_arr = []

        for seg_path in seg_paths:
            seg = cv2.imread(seg_path)
            seg = cv2.cvtColor(seg, cv2.COLOR_BGR2RGB)
            segs_arr.append(seg)

        if self.transform is not None:
            img0 = self.transform(img0)
            img1 = self.transform(img1)
            for i, seg in enumerate(segs_arr):
                segs[i, :] = self.transform(seg)
        return img0, img1, segs

    def __len__(self):
        return len(self.dataset)