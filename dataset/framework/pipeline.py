import json
import os
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
            video_indices = sorted(self.__dataset_obj.video_index_to_questions_map.keys())
            for i, instance_id in video_indices:
                question_list = self.__dataset_obj.video_index_to_questions_map[instance_id]

                for j, question in enumerate(question_list):
                    minimal_dataset_file.write(json.dumps(question))
                    if i == len(video_indices) - 1 and j == len(question_list) - 1:
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

    def __init__(self, purge_single_answers=False):
        """
        :param purge_single_answers: Removes all questions if there are only one answer type for that pair.
        """
        super().__init__(name="Balancing Stage")
        self.purge = purge_single_answers

    def process(self, dataset_obj: CRAFTDataset):
        logger.info("Initiating dataset balancing stage...")

        # dataset_obj.generate_statistics(output_folder=f"{dataset_obj.dataset_folder_path}/stats/imbalanced")

        logger.info(f"Performing various under-sampling operations on dataset...")
        balanced_dataset_output_path = f"{dataset_obj.dataset_folder_path}/balanced_dataset.json"
        DatasetUnderSampler(dataset_obj, balanced_dataset_output_path) \
            .balance_answers_within_each_template_and_simulation_ids(self.purge) \
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
            split_sizes = {"train": 12, "validation": 4, "test": 4}

            counterparts = {1: 18, 3: 16, 4: 17}

            sids = list(range(1, 21))

            chosen = {"test": [], "validation": [], "train": []}

            # Bogo method. The best. I've spend a lot of time until I reached this ultimate conclusion.
            while True:
                rnd.shuffle(sids)
                chosen["train"] = sids[:split_sizes["train"]]
                chosen["validation"] = sids[split_sizes["train"]:split_sizes["train"] + split_sizes["validation"]]
                chosen["test"] = sids[split_sizes["train"] + split_sizes["validation"]:sum(split_sizes.values())]

                ok = True
                for split, ss in chosen.items():
                    for s in ss:
                        if s in counterparts and counterparts[s] in ss:
                            ok = False
                            break
                        if not ok:
                            break
                if ok:
                    break

            counts = defaultdict(int)
            for question in dataset_obj.questions:
                if int(question["simulation_id"]) in chosen["train"]:
                    counts["train"] += 1
                if int(question["simulation_id"]) in chosen["validation"]:
                    counts["validation"] += 1
                if int(question["simulation_id"]) in chosen["test"]:
                    counts["test"] += 1

            logger.info(f"Splits: {json.dumps(chosen)}")

            logger.info(f"Number of questions for each split: {json.dumps(dict(counts))}")

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

        elif self.config == "random":

            video_indices = sorted(self.__dataset_obj.video_index_to_questions_map.keys())
            N = len(video_indices)
            test_count = int(N * 0.2)
            val_count = int(N * 0.2)
            train_count = int(N * 0.6)
            train_count += N - test_count - val_count - train_count
            rnd.shuffle(video_indices)

            train = video_indices[:train_count]
            val = video_indices[train_count:train_count + val_count]
            test = video_indices[train_count + val_count:N]
            assert len(train) + len(val) + len(test) == N

            for video_index in train:
                questions = self.__dataset_obj.video_index_to_questions_map[video_index]
                for question in questions:
                    splits["train"].append({
                        "video_index": question["video_index"],
                        "question_index": question["question_index"]
                    })
            for video_index in val:
                questions = self.__dataset_obj.video_index_to_questions_map[video_index]
                for question in questions:
                    splits["validation"].append({
                        "video_index": question["video_index"],
                        "question_index": question["question_index"]
                    })
            for video_index in test:
                questions = self.__dataset_obj.video_index_to_questions_map[video_index]
                for question in questions:
                    splits["test"].append({
                        "video_index": question["video_index"],
                        "question_index": question["question_index"]
                    })

            split_to_vid = defaultdict(set)

            for s in splits:
                for pair in splits[s]:
                    split_to_vid[s].add(pair["video_index"])

            print(f"Stats for {self.config}:")
            for s in split_to_vid:
                print(s, len(split_to_vid[s]))

            def diff(first, second):
                return [item for item in first if item not in second]

            dtrain = diff(train, split_to_vid["train"])
            dval = diff(val, split_to_vid["validation"])
            dtest = diff(test, split_to_vid["test"])

            print(dtrain, dval, dtest)

        FileIO.write_json(dict(splits), f"{dataset_obj.dataset_folder_path}/split_info_{self.config}.json")

    def get_output(self):
        return self.__dataset_obj


class FullDatasetWriteStage(Stage):

    def __init__(self, output_file_name):
        super().__init__(name="Full Dataset Write Stage", )
        self.__dataset_obj: CRAFTDataset = None
        self.output_file_name = output_file_name

    def process(self, dataset_obj: CRAFTDataset):
        logger.info("Write full dataset...")

        self.__dataset_obj = dataset_obj

        with open(f"{self.__dataset_obj.dataset_folder_path}/{self.output_file_name}", "w") as full_dataset_file:
            full_dataset_file.write("[")
            instance_ids = sorted(list(dataset_obj.video_index_to_questions_map.keys()))
            i = 0
            for instance_id in instance_ids:
                question_list = dataset_obj.video_index_to_questions_map[instance_id]
                sid = int(question_list[0]["simulation_id"])

                questions_file_path = self.__dataset_obj.get_questions_output_path(sid, instance_id)

                try:
                    # Add them into dataset.json
                    with open(questions_file_path, "r") as questions_file:
                        qa_json = json.load(questions_file)

                        filtered_questions = []
                        for q in qa_json["questions"]:
                            ok_questions = self.__dataset_obj.get_questions_for_video(q["video_index"])
                            for ok_q in ok_questions:
                                if ok_q["question_index"] == q["question_index"]:
                                    q["question"] = ok_q["question"]  # If post-processed.
                                    filtered_questions.append(q)
                                    break

                        qa_json["questions"][:] = filtered_questions

                        simulation_instance = json.loads(f"""{{
                                    "simulation_id": "{sid}",
                                    "video_path": "{self.__dataset_obj.get_video_output_path(sid, instance_id)}",
                                    "questions": {json.dumps(qa_json)}
                                 }}""")
                        if instance_id % 10 == 0:
                            logger.info(f"Writing: {instance_id}/{len(instance_ids)}")
                        simulation_instance = \
                            DatasetUtils.relativize_paths([simulation_instance],
                                                          self.__dataset_obj.dataset_folder_path)[0]
                        full_dataset_file.write(json.dumps(simulation_instance))
                        if i != len(instance_ids) - 1:
                            full_dataset_file.write(",")
                        else:
                            full_dataset_file.write("]")
                except FileNotFoundError:
                    logger.warning(f"{instance_id:06d}: Questions file cannot be found")
                i += 1

    def get_output(self):
        return self.__dataset_obj


class AnnotationsFileCollector(Stage):
    def __init__(self, output_file_name):
        super().__init__(name="Annotations File Collector Stage")
        self.__dataset_obj: CRAFTDataset = None
        self.output_file_name = output_file_name

    def process(self, dataset_obj: CRAFTDataset):
        logger.info("Collecting annotations...")
        self.__dataset_obj = dataset_obj
        with open(f"{dataset_obj.dataset_folder_path}/{self.output_file_name}", "w") as annotations_file:
            annotations_file.write("{")
            instance_ids = sorted(list(dataset_obj.video_index_to_questions_map.keys()))
            for i, instance_id in enumerate(instance_ids):
                sid = int(dataset_obj.video_index_to_questions_map[instance_id][0]["simulation_id"])
                annotations_file_path = dataset_obj.get_simulation_with_variations_output_path(sid, instance_id)
                with open(annotations_file_path) as this_annotations_file:
                    annotations_file.write(f"""
                            "{instance_id:06d}": {json.dumps(json.load(this_annotations_file))}
                    """)
                    if i != len(instance_ids) - 1:
                        annotations_file.write(",")
                    if i % 10 == 0:
                        logger.info(f"Collecting annotations: {i}/{len(instance_ids)}")
            annotations_file.write("}")

    def get_output(self):
        return self.__dataset_obj


class CleanupStage(Stage):
    def __init__(self):
        super().__init__(name="Cleanup Stage")
        self.__dataset_obj: CRAFTDataset = None

    def process(self, dataset_obj: CRAFTDataset):
        self.__dataset_obj = dataset_obj
        videos_with_no_questions = []
        ground = list(range(0, 10000))
        for idx in ground:
            if idx not in dataset_obj.video_index_to_questions_map:
                videos_with_no_questions.append(idx)

        with open(f"{dataset_obj.dataset_folder_path}/videos_with_no_questions.json", "w") as vwnq_file:
            json.dump(videos_with_no_questions, vwnq_file)

    def get_output(self):
        return self.__dataset_obj


class PostProcessStage(Stage):

    def __init__(self):
        super().__init__(name="Post-Process Stage")
        self.__dataset_obj: CRAFTDataset = None

    def process(self, dataset_obj: CRAFTDataset):
        logger.info("Initiating post process stage...")

        self.__dataset_obj = dataset_obj

        for instance_id in dataset_obj.video_index_to_questions_map.keys():
            question_list = dataset_obj.video_index_to_questions_map[instance_id]

            for question in question_list:
                if question["template_id"] == "counterfactual_2":
                    question_text: str = question["question"]
                    if question_text.startswith("Will"):
                        question_text = question_text.replace("the basket the", "the basket if the")
                        question_text = question_text.replace("the container the", "the container if the")
                        question_text = question_text.replace("the bucket the", "the bucket if the")
                        question["question"] = question_text
                if question["template_id"] in ["prevent_0", "prevent_1", "prevent_2"]:
                    question_text: str = question["question"]
                    if question_text.startswith("Is"):
                        question_text = question_text.replace("is prevented by", "prevented by")
                        question_text = question_text.replace("is kept by", "kept by")
                        question_text = question_text.replace("is held by", "held by")
                        question_text = question_text.replace("is blocked by", "blocked by")
                        question["question"] = question_text

            logger.info(f"Processed: {instance_id}/{len(dataset_obj.video_index_to_questions_map.keys())}")

        self.__rewrite_dataset()

    def __rewrite_dataset(self):
        with open(f"{self.__dataset_obj.dataset_folder_path}/dataset_minimal.json", "w") as minimal_dataset_file:
            minimal_dataset_file.write("[")

            logger.info(f"Rewriting preprocessed minimal dataset...")
            video_indices = sorted(self.__dataset_obj.video_index_to_questions_map.keys())
            for i, instance_id in enumerate(video_indices):
                question_list = self.__dataset_obj.video_index_to_questions_map[instance_id]

                for j, question in enumerate(question_list):
                    minimal_dataset_file.write(json.dumps(question))
                    if i == len(video_indices) - 1 and j == len(question_list) - 1:
                        pass
                    else:
                        minimal_dataset_file.write(",")

            minimal_dataset_file.write("]")

            logger.info(f"Successfully rewritten to: {self.__dataset_obj.dataset_folder_path}")

    def cleanup(self):
        logger.info(f"Re-reading post-processed minimal dataset...")
        self.__dataset_obj = CRAFTDataset(self.__dataset_obj.dataset_folder_path, self.__dataset_obj.metadata)

    def get_output(self):
        return self.__dataset_obj


class CompilePerturbationlessDataset(Stage):

    def __init__(self, output_folder_path: str):
        super().__init__(name="Compile Perturbation-less Dataset Stage")
        self.__dataset_obj: CRAFTDataset = None
        self.output_folder_path = output_folder_path

    def process(self, dataset_obj: CRAFTDataset):

        self.__dataset_obj = dataset_obj

        original_questions = []

        instance_ids = sorted(list(dataset_obj.video_index_to_questions_map.keys()))
        for i, instance_id in enumerate(instance_ids):
            sid = int(dataset_obj.video_index_to_questions_map[instance_id][0]["simulation_id"])
            original_qa_json = FileIO.read_json(self.__dataset_obj.get_original_questions_path(sid, instance_id))
            for qa in original_qa_json["questions"]:
                original_questions.append(dataset_obj.get_question_from_question_obj(qa, sid))

            logger.info(f"Processed: {instance_id}/{len(instance_ids)}")

        os.makedirs(self.output_folder_path, exist_ok=True)

        FileIO.write_json(original_questions, f"{self.output_folder_path}/dataset_minimal.json")

        self.__dataset_obj = CRAFTDataset(self.output_folder_path, self.__dataset_obj.metadata)

    def get_output(self):
        return self.__dataset_obj
