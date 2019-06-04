import os.path as osp

class PhysNetReal:

    def __init__(self, path):
        print("Loading PhysNet Real Dataset")
        self.img0_dir = osp.join(path, "First")
        self.img1_dir = osp.join(path, "Last")
        self.seg_dir = osp.join(path, "Segment")
        self.split_file = osp.join(path, "split.txt")

        self.train, self.val, self.test = self.parse_split_file()

        print("Train data count {}".format(len(self.train)))
        print("Val data count {}".format(len(self.val)))
        print("Test data count {}".format(len(self.test)))

        print("PhysNet Real Dataset Loaded")

    def parse_split_file(self):
        train = []
        val = []
        test = []
        with open(self.split_file) as f:
            for line in f:
                idx, spl = line.split()
                if int(spl) == 0:
                    continue
                elif int(spl) > 3:
                    print("Wrong split at index {}".format(idx))
                    continue
                img0_name = "img_concat_" + idx + "_first.png"
                img0_path = osp.join(self.img0_dir, img0_name)
                if not osp.isfile(img0_path):
                    print("First image not available at index {}".format(idx))
                    continue
                img1_name = "img_concat_" + idx + "_last.png"
                img1_path = osp.join(self.img1_dir, img1_name)
                if not osp.isfile(img1_path):
                    print("Last image not available at index {}".format(idx))
                    continue
                seg1_name = "imgseg_" + idx + "_A.png"
                seg2_name = "imgseg_" + idx + "_B.png"
                seg3_name = "imgseg_" + idx + "_C.png"
                seg4_name = "imgseg_" + idx + "_D.png"
                seg1_path = osp.join(self.seg_dir, seg1_name)
                seg2_path = osp.join(self.seg_dir, seg2_name)
                seg3_path = osp.join(self.seg_dir, seg3_name)
                seg4_path = osp.join(self.seg_dir, seg4_name)
                if not osp.isfile(seg1_path):
                    print("First segmentation not available at index {}".format(idx))
                    continue
                if not osp.isfile(seg2_path):
                    print("Second segmentation not available at index {}".format(idx))
                    continue
                seg_paths = [seg1_path, seg2_path]
                if osp.isfile(seg3_path):
                    seg_paths.append(seg3_path)
                if osp.isfile(seg4_path):
                    seg_paths.append(seg4_path)
                data = (img0_path, img1_path, seg_paths)
                if int(spl) == 1:
                    train.append(data)
                elif int(spl) == 2:
                    val.append(data)
                elif int(spl) == 3:
                    test.append(data)
                else:
                    print("Unexpected!")
        return train, val, test
