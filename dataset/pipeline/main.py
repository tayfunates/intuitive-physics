import json

from pipeline.dataset import DatasetGenerationConfig
from pipeline.pipeline import Pipeline, DatasetGenerationStage, DatasetStatisticsGenerationStage, InspectionStage, \
    BalancingStage

if __name__ == '__main__':
    pipeline = Pipeline([
        DatasetGenerationStage(),
        DatasetStatisticsGenerationStage(),
        InspectionStage(),
        BalancingStage(),
    ])

    config = DatasetGenerationConfig(json.load(open("dataset_gen_config.json")))
    pipeline.feed_first_stage(config)

    pipeline.execute_all()
