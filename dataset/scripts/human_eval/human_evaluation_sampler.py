import random
from collections import defaultdict

from framework.dataset import SVQADataset, DatasetStatistics, DatasetStatisticsExporter
from framework.utils import FileIO

if __name__ == '__main__':
    dataset_folder_path = "/Users/msa/Research/CRAFT/Dataset_3000_230920"

    dataset = SVQADataset(dataset_folder_path, FileIO.read_json("../svqa/metadata.json"))

    test_dataset = []

    for item in dataset.dataset_json:
        if item["split"] == "test":
            test_dataset.append(item)

    dataset.dataset_json = test_dataset
    dataset.populate_question_list()

    sampled = random.sample(dataset.questions, 150)

    dataset.questions = sampled
    dataset.generate_statistics("./human_eval_150")

    FileIO.write_json(sampled, "./human_eval_150/questions.json")

    vq = defaultdict(list)
    for q in sampled:
        vq[q["video_index"]].append(q)

    FileIO.write_json(vq, "./human_eval_150/questions_per_video.json")


