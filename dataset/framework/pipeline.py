import time
from abc import ABC, abstractmethod
from typing import List

from loguru import logger

from framework.balance import DatasetInspector, DatasetBalancer, DatasetUnderSampler
from framework.dataset import DatasetGenerationConfig, DatasetGenerator, SVQADataset, DatasetStatistics
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
                        f"took {round(time.time() - start_time, 2)} seconds")
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
        self.__dataset = SVQADataset(dataset_folder_path, FileIO.read_json(config.dataset_metadata_file_path))

    def get_output(self):
        return self.__dataset


class DatasetStatisticsGenerationStage(Stage):

    def __init__(self):
        super().__init__()
        self.__dataset_statistics = None

    def process(self, dataset: SVQADataset):
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
        self.__dataset_obj = None

    def process(self, dataset_obj: SVQADataset):

    def cleanup(self):
        self.__dataset_obj.prepare_auxiliaries()

    def get_output(self):
        return self.__dataset_obj


class BalancingStage(Stage):

    def __init__(self):
        super().__init__(name="Balancing Stage")

    def process(self, dataset_obj: SVQADataset):
        logger.info("Initiating dataset balancing stage...")

        dataset_obj.generate_statistics(output_folder=f"{dataset_obj.dataset_folder_path}/stats/imbalanced")

        logger.info(f"Performing various under-sampling operations on dataset...")
        balanced_dataset_output_path = f"{dataset_obj.dataset_folder_path}/balanced_dataset.json"
        DatasetUnderSampler(dataset_obj, balanced_dataset_output_path) \
            .balance_answers_within_each_template_and_simulation_ids() \
            .dump()
        balanced_dataset = SVQADataset(balanced_dataset_output_path, dataset_obj.metadata)

        balanced_dataset.generate_statistics(output_folder=f"{dataset_obj.dataset_folder_path}/stats/balanced")

    def cleanup(self):
        pass

    def get_output(self):
        pass
