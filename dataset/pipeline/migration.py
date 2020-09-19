import json
import os
from pathlib import Path

from loguru import logger

from pipeline.utils import DictUtils


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
                    DictUtils.scrub(json_obj, "split")
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