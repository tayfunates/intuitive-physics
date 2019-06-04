from torch.utils.data import Dataset
import cv2

class O2P2Dataset(Dataset):

    def __init__(self, dataset, transform=None):
        self.dataset = dataset
        self.transform = transform

    def __getitem__(self, index):
        img0_path, img1_path, seg_paths = self.dataset[index]
        img0 = cv2.imread(img0_path)
        img0 = cv2.cvtColor(img0, cv2.COLOR_BGR2RGB)
        img1 = cv2.imread(img1_path)
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        segs = []
        for seg_path in seg_paths:
            seg = cv2.imread(seg_path)
            seg = cv2.cvtColor(seg, cv2.COLOR_BGR2RGB)
            segs.append(seg)
        if self.transform is not None:
            img0 = self.transform(img0)
            img1 = self.transform(img1)
            for i, seg in enumerate(segs):
                segs[i] = self.transform(seg)
        return img0, img1, segs

    def __len__(self):
        return len(self.dataset)