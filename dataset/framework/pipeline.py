from abc import ABC, abstractmethod
from typing import List

from framework.balance import DatasetInspector, DatasetBalancer
from framework.dataset import DatasetGenerationConfig, DatasetGenerator, SVQADataset, DatasetStatistics


class Stage(ABC):

    def __init__(self):
        self._owner = None

    def preprocess(self):
        pass

    @abstractmethod
    def process(self, obj: object):
        pass

    def postprocess(self):
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
        next_input = self.__initial_data
        for stage in self.stages:
            stage.preprocess()
            stage.process(next_input)
            stage.postprocess()
            next_input = stage.get_output()
            stage.cleanup()

    def feed_first_stage(self, feed: object):
        self.__initial_data: object = feed


class DatasetGenerationStage(Stage):

    def __init__(self):
        super().__init__()
        self.__dataset = None

    def process(self, config: DatasetGenerationConfig):
        dataset_generator = DatasetGenerator(config)
        dataset_generator.execute()
        dataset_folder_path = dataset_generator.config.output_folder_path
        # TODO: Maybe move this relative path to simulation generation configuration file?
        self.__dataset = SVQADataset(dataset_folder_path, "../svqa/metadata.json")

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
        return {"needed_answers": self.__needed_answers }


class BalancingStage(Stage):

    def preprocess(self):
        pass

    def process(self, needed_answers: object):
        balancer = DatasetBalancer()
        pass

    def postprocess(self):
        pass

    def cleanup(self):
        pass

    def get_output(self):
        pass

