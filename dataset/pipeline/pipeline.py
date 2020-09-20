from abc import ABC, abstractmethod
from typing import List

from pipeline.balance import DatasetInspector
from pipeline.dataset import DatasetGenerationConfig, DatasetGenerator, SVQADataset, DatasetStatistics


class Stage(ABC):

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


class DatasetGenerationStage(Stage):

    def __init__(self):
        self.__dataset = None

    def process(self, config: DatasetGenerationConfig):
        dataset_generator = DatasetGenerator(config)
        dataset_generator.execute()
        self.__dataset_folder_path = dataset_generator.config.output_folder_path

    def postprocess(self):
        # TODO: Maybe move this relative path to simulation generation configuration file?
        self.__dataset = SVQADataset(self.__dataset_folder_path, "../svqa/metadata.json")

    def get_output(self):
        return self.__dataset


class DatasetStatisticsGenerationStage(Stage):

    def __init__(self):
        self.__dataset_statistics = None

    def process(self, dataset: SVQADataset):
        self.__dataset_statistics = DatasetStatistics(dataset)
        self.__dataset_statistics.generate_all_stats()

    def get_output(self):
        return self.__dataset_statistics


class InspectionStage(Stage):

    def __init__(self):
        self.__output = None

    def process(self, stats: DatasetStatistics):
        inspector = DatasetInspector(stats)
        self.__output = inspector.inspect_tid_and_sid_versus_answer_balance()

    def cleanup(self):
        pass

    def get_output(self):
        return self.__output


class BalancingStage(Stage):

    def preprocess(self):
        pass

    def process(self, obj: object):
        pass

    def postprocess(self):
        pass

    def cleanup(self):
        pass

    def get_output(self):
        pass


class Pipeline:

    def __init__(self, stages: List[Stage] = None):
        self.stages: List[Stage] = [] if stages is None else stages

    def add_stage(self, stage: Stage):
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
