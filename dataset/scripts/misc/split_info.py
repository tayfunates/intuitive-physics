import json
from collections import defaultdict
import os

from framework.dataset import CRAFTDataset
from framework.utils import FileIO


def split_info(dataset, split):
    with open(f"{dataset.dataset_folder_path}/split_info_{split}.json", "r") as split_info_file:
        split_info = json.load(split_info_file)

        split_to_vid = defaultdict(set)

        for s in split_info:
            for pair in split_info[s]:
                split_to_vid[s].add(pair["video_index"])

        print("Split:", split)
        print("Videos")
        for s in split_to_vid:
            print(s, len(split_to_vid[s]))

        print("Questions")
        question_count_per_split = defaultdict(int)
        for s in split_to_vid:
            for vi in split_to_vid[s]:
                question_count_per_split[s] += len(dataset.video_index_to_questions_map[vi])
        for s, c in question_count_per_split.items():
            print(s, c)

def proof_read():
    with open("./dataset_minimal.json", "r") as dataset_file:
        questions = json.load(dataset_file)

        for q in questions:
            if not os.path.isfile(q["video_file_path"]):
                print(q["video_file_path"], False)


if __name__ == '__main__':
    dataset_folder_path = "../../framework/out/CRAFT_10K"
    metadata = FileIO.read_json("../../svqa/metadata.json")
    dataset = CRAFTDataset(dataset_folder_path, metadata)

    print("Number of videos:", len(dataset.video_index_to_questions_map.keys()))
    split_info(dataset, "random")
    split_info(dataset, "hard")

