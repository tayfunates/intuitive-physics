import json
import os
from pathlib import Path

from loguru import logger


def scrub(obj, key_to_be_removed):
    if isinstance(obj, dict):
        # the call to `list` is useless for py2 but makes
        # the code py2/py3 compatible
        for key in list(obj.keys()):
            if key == key_to_be_removed:
                obj.pop(key, None)
            else:
                scrub(obj[key], key_to_be_removed)
    elif isinstance(obj, list):
        for i in reversed(range(len(obj))):
            if obj[i] == key_to_be_removed:
                del obj[i]
            else:
                scrub(obj[i], key_to_be_removed)

    else:
        # neither a dict nor a list, do nothing
        pass


class DatasetMigration:

    def __init__(self, dataset_folder_path: str):
        self.dataset_folder_path = dataset_folder_path

    def make_dataset_split_agnostic(self):
        for dir, subdirs, listfilename in os.walk(self.dataset_folder_path):
            for filename in listfilename:
                new_filename = filename.replace("train_", "").replace("test_", "").replace("validation_", "")
                src = os.path.join(dir, filename)  # NOTE CHANGE HERE
                dst = os.path.join(dir, new_filename)  # AND HERE
                os.rename(src, dst)
                logger.info(f"{filename} -> {new_filename}")

                if Path(new_filename).suffix == ".json":
                    logger.info(f"'{dst}' is a JSON file, Recursively removing split parameter...")
                    json_obj = json.load(open(dst))
                    scrub(json_obj, "split")
                    logger.info(f"Dumping new JSON file to {dst}")
                    json.dump(json_obj, open(dst, "w"))

    def rename_folders(self):
        for dir, subdirs, listfilename in os.walk(self.dataset_folder_path):
            for subdir in subdirs:
                new_dir_name = subdir.replace("sim-id-", "sid_")
                src = os.path.join(dir, subdir)
                dst = os.path.join(dir, new_dir_name)
                os.rename(src, dst)
                logger.info(f"{subdir} -> {new_dir_name}")


if __name__ == '__main__':
    # dataset_obj = SVQADataset("./out/Dataset_3000_270820/dataset.json", "../svqa/metadata.json")

    # json.dump(
    #     dataset_obj.questions,
    #     open(f"./Dataset_3000_270820/dataset_minimal.json", "w"),
    #     indent=2
    # )

    migration = DatasetMigration("out/Dataset_250_070720")
    logger.info("Starting to migrate the dataset...")
    migration.make_dataset_split_agnostic()
    migration.rename_folders()
    logger.info("Dataset migration complete.")
