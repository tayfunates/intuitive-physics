import os
import os.path as osp
import glob

class PhysVQA:

    def __init__(self, path):
        print("Loading PhysVQA Dataset")
        self.path = path
        self.split_file = osp.join(path, "split.txt")

        self.train, self.val, self.test = self.parse_split_file()

        print("Train data count {}".format(len(self.train)))
        print("Val data count {}".format(len(self.val)))
        print("Test data count {}".format(len(self.test)))

        print("Loading PhysVQA Loaded")

    def parse_split_file(self):
        train = []
        val = []
        test = []
        with open(self.split_file) as f:
            for line in f:
                scene, spl = line.split()
                if int(spl) == 0:
                    continue
                elif int(spl) > 3:
                    print("Wrong split for scene {}".format(scene))
                    continue

                scene_folder = osp.join(self.path, scene)
                if osp.isdir(scene_folder):
                    scene_all_unstable_repeats = glob.glob(osp.join(scene_folder, '*FinalUnStable*.png'))
                    scene_all_unstable_repeats.sort()
                    scene_repeats_segs = [f for f in scene_all_unstable_repeats if "NONVisibleSeg" in f]
                    scene_repeats_first_imgs = [f for f in scene_all_unstable_repeats if "NONVisibleSeg" not in f and "VisibleSeg" not in f]

                    scene_all_stable_repeats = glob.glob(osp.join(scene_folder, '*FinalStable*.png'))
                    scene_all_stable_repeats.sort()
                    scene_repeats_last_imgs = [f for f in scene_all_stable_repeats if "NONVisibleSeg" not in f and "VisibleSeg" not in f]

                    for rp in range(0, len(scene_repeats_segs)):
                        repeat = scene_repeats_segs[rp]
                        repeat_first_img = scene_repeats_first_imgs[rp]
                        repeat_last_img = scene_repeats_last_imgs[rp]

                        repeat_name = osp.splitext(osp.basename(repeat))[0]
                        repeat_objects_path = osp.join(scene_folder, repeat_name + '_objects')

                        if not osp.exists(repeat_objects_path):
                            print("Objects cannot be found {}".format(scene))

                        object_paths = [osp.join(repeat_objects_path, f) for f in os.listdir(repeat_objects_path)]
                        data = (repeat_first_img, repeat_last_img, object_paths)

                        if int(spl) == 1:
                            train.append(data)
                        elif int(spl) == 2:
                            val.append(data)
                        elif int(spl) == 3:
                            test.append(data)
                        else:
                            print("Unexpected!")

        return train, val, test
