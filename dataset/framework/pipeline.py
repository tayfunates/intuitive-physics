import json
import time
from abc import ABC, abstractmethod
from collections import defaultdict
from random import Random
from typing import List

from loguru import logger

from framework.balance import DatasetInspector, DatasetUnderSampler
from framework.dataset import DatasetGenerationConfig, DatasetGenerator, CRAFTDataset, DatasetStatistics, DatasetUtils
from framework.utils import FileIO


class Stage(ABC):

    def __init__(self, name=None):
        self._owner = None
        self.name = name

    @abstractmethod
    def process(self, obj: object):
        pass

    def cleanup(self):
        pass

    @abstractmethod
    def get_output(self):
        pass

    def set_owner(self, owner):
        self._owner = owner


class Pipeline:

    def __init__(self, stages: List[Stage] = None):
        self.stages: List[Stage] = [] if stages is None else stages

    def add_stage(self, stage: Stage):
        stage.set_owner(self)
        self.stages.append(stage)

    def execute_all(self):
        stage_index = 1
        next_input = self.__initial_data
        for stage in self.stages:
            start_time = time.time()

            stage.process(next_input)
            stage.cleanup()

            next_input = stage.get_output()

            logger.info(f"{stage.name if stage.name is not None else f'Pipeline Stage {stage_index}'} "
                        f"took {round((time.time() - start_time) / 60, 2)} minutes")
            stage_index += 1

    def feed_first_stage(self, initial_data: object):
        self.__initial_data: object = initial_data


class DatasetGenerationStage(Stage):

    def __init__(self):
        super().__init__(name="Dataset Generation Stage")
        self.__dataset = None

    def process(self, config: DatasetGenerationConfig):
        logger.info("Initiating dataset generation process...")
        dataset_generator = DatasetGenerator(config)
        dataset_generator.execute()
        dataset_folder_path = dataset_generator.config.output_folder_path
        self.__dataset = CRAFTDataset(dataset_folder_path, FileIO.read_json(config.dataset_metadata_file_path))

    def get_output(self):
        return self.__dataset


class DatasetStatisticsGenerationStage(Stage):

    def __init__(self):
        super().__init__()
        self.__dataset_statistics = None

    def process(self, dataset: CRAFTDataset):
        self.__dataset_statistics = DatasetStatistics(dataset)
        self.__dataset_statistics.generate_all_stats()

    def get_output(self):
        return self.__dataset_statistics


class InspectionStage(Stage):

    def __init__(self):
        super().__init__()
        self.__needed_answers = None
        self.__inspector = None

    def process(self, stats: DatasetStatistics):
        self.__inspector = DatasetInspector(stats)
        self.__needed_answers: dict = self.__inspector.compute_answers_needed_for_tid_and_sid_versus_answer_balance()

    def cleanup(self):
        pass

    def get_output(self):
        return {"needed_answers": self.__needed_answers}


class PreBalancingPostProcessStage(Stage):

    def __init__(self):
        super().__init__(name="Pre-Balancing Post-Process Stage")
        self.__dataset_obj: CRAFTDataset = None

    def process(self, dataset_obj: CRAFTDataset):
        logger.info("Initiating post process stage before balancing...")

        self.__dataset_obj = dataset_obj

        # Preprocess Before Balancing 1: Do not ask shape if only one shape is present in the scene.
        for instance_id in range(len(dataset_obj.video_index_to_questions_map.keys())):
            # Getting instance_id from range is dangerous, if len - 1 is less than max_video_index
            question_list = dataset_obj.video_index_to_questions_map[instance_id]
            sid = int(question_list[0]["simulation_id"])

            annotations = FileIO.read_json(dataset_obj.get_simulation_with_variations_output_path(sid, instance_id))
            objects_in_scene = annotations["original_video_output"]["scene_states"][0]["scene"]["objects"]
            dynamic_objects = [object for object in objects_in_scene if object["bodyType"] == 2]

            new_questions_list = []
            for question in question_list:
                answer_type = dataset_obj.get_answer_type_for_answer(question["answer"])
                if answer_type == "Shape":
                    if len(set([f"{object['shape']}" for object in dynamic_objects])) <= 1:
                        # Remove the question that asks shape
                        logger.info(f"Question asks shape even though there's only 1 "
                                    f"shape present in the scene. Removing {question['video_index']}/{question['question_index']}")
                        continue
                new_questions_list.append(question)

            question_list[:] = new_questions_list

        # Continue preprocessing before balancing here

        self.__rewrite_dataset()

    def __rewrite_dataset(self):
        with open(f"{self.__dataset_obj.dataset_folder_path}/dataset_minimal.json", "w") as minimal_dataset_file:
            minimal_dataset_file.write("[")

            logger.info(f"Rewriting preprocessed minimal dataset...")
            N = len(self.__dataset_obj.video_index_to_questions_map.keys())
            for instance_id in range(N):
                question_list = self.__dataset_obj.video_index_to_questions_map[instance_id]

                for i, question in enumerate(question_list):
                    minimal_dataset_file.write(json.dumps(question))
                    if instance_id == N - 1 and i == len(question_list) - 1:
                        pass
                    else:
                        minimal_dataset_file.write(",")

            minimal_dataset_file.write("]")

            logger.info(f"Successfully rewritten to: {self.__dataset_obj.dataset_folder_path}")

    def cleanup(self):
        logger.info(f"Re-reading preprocessed minimal dataset...")
        self.__dataset_obj = CRAFTDataset(self.__dataset_obj.dataset_folder_path, self.__dataset_obj.metadata)

    def get_output(self):
        return self.__dataset_obj


class BalancingStage(Stage):

    def __init__(self):
        super().__init__(name="Balancing Stage")

    def process(self, dataset_obj: CRAFTDataset):
        logger.info("Initiating dataset balancing stage...")

        dataset_obj.generate_statistics(output_folder=f"{dataset_obj.dataset_folder_path}/stats/imbalanced")

        logger.info(f"Performing various under-sampling operations on dataset...")
        balanced_dataset_output_path = f"{dataset_obj.dataset_folder_path}/balanced_dataset.json"
        DatasetUnderSampler(dataset_obj, balanced_dataset_output_path) \
            .balance_answers_within_each_template_and_simulation_ids() \
            .dump()
        balanced_dataset = CRAFTDataset(balanced_dataset_output_path, dataset_obj.metadata)

        balanced_dataset.generate_statistics(output_folder=f"{dataset_obj.dataset_folder_path}/stats/balanced")

    def cleanup(self):
        pass

    def get_output(self):
        pass


class DatasetSplitStage(Stage):

    def __init__(self, config):
        super().__init__(name="Dataset Split Stage", )
        self.__dataset_obj: CRAFTDataset = None
        self.config = config

    def process(self, dataset_obj: CRAFTDataset):
        logger.info("Initiating dataset splitting stage...")
        rnd = Random(10435)

        self.__dataset_obj = dataset_obj

        splits = defaultdict(list)
        vi_qi_to_split = {}

        if self.config == "hard":
            split_indices = {
                "test": (16, 20),
                "validation": (12, 16),
                "train": (0, 12)
            }

            chosen = {"test": [], "validation": [], "train": []}

            sids = [2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
            rnd.shuffle(sids)

            chosen["train"] = sids[split_indices["train"][0]:split_indices["train"][1]]
            chosen["validation"] = sids[split_indices["validation"][0]:split_indices["validation"][1]]
            chosen["test"] = sids[split_indices["test"][0]:split_indices["test"][1]]

            counterparts = {1: 18, 3: 16, 4: 17}

            for key in counterparts:
                if counterparts[key] not in chosen["train"]:
                    chosen["train"].insert(split_indices["train"][0], key)
                elif counterparts[key] not in chosen["validation"]:
                    chosen["validation"].insert(split_indices["validation"][0], key)
                elif counterparts[key] not in chosen["test"]:
                    chosen["test"].insert(split_indices["test"][0], key)

            counts = defaultdict(int)
            for question in dataset_obj.questions:
                if int(question["simulation_id"]) in chosen["train"]:
                    counts["train"] += 1
                if int(question["simulation_id"]) in chosen["validation"]:
                    counts["validation"] += 1
                if int(question["simulation_id"]) in chosen["test"]:
                    counts["test"] += 1

            sid_to_split = {}
            for split, sids in chosen.items():
                for sid in sids:
                    sid_to_split[sid] = split

            for question in dataset_obj.questions:
                sid = int(question["simulation_id"])
                splits[sid_to_split[sid]].append({
                    "video_index": question["video_index"],
                    "question_index": question["question_index"]
                })
                vi_qi_to_split[(question["video_index"], question["question_index"])] = sid_to_split[sid]

        elif self.config == "easy":

            idxs = list(range(len(self.__dataset_obj.questions)))
            N = len(idxs)
            test_count = int(N * 0.2)
            val_count = int(N * 0.2)
            train_count = int(N * 0.6)
            train_count += N - test_count - val_count - train_count
            rnd.shuffle(idxs)

            train = idxs[:train_count]
            val = idxs[train_count:train_count + val_count]
            test = idxs[train_count + val_count:N]

            for i in train:
                question = self.__dataset_obj.questions[i]
                splits["train"].append({
                    "video_index": question["video_index"],
                    "question_index": question["question_index"]
                })
            for i in val:
                question = self.__dataset_obj.questions[i]
                splits["validation"].append({
                    "video_index": question["video_index"],
                    "question_index": question["question_index"]
                })
            for i in test:
                question = self.__dataset_obj.questions[i]
                splits["test"].append({
                    "video_index": question["video_index"],
                    "question_index": question["question_index"]
                })

        FileIO.write_json(dict(splits), f"{dataset_obj.dataset_folder_path}/split_info_{self.config}.json")

    def get_output(self):
        return self.__dataset_obj
