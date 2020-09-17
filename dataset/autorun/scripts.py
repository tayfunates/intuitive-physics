import json

from autorun.dataset import SVQADataset

if __name__ == '__main__':

    dataset_obj = SVQADataset("./out/Dataset_3000_270820/dataset.json", "../svqa/metadata.json")

    json.dump(
        dataset_obj.questions,
        open(f"./Dataset_3000_270820/dataset_minimal.json", "w"),
        indent=2
    )
