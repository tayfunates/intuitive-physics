import sys
from datetime import datetime

from loguru import logger

from framework.dataset import DatasetGenerationConfig, DatasetGenerator
from framework.pipeline import Pipeline, DatasetGenerationStage, BalancingStage, PreBalancingPostProcessStage
from framework.utils import FileIO

if __name__ == '__main__':

    # Enqueue is because of multiprocessing.
    logger.add(f"out/dataset_generation_{datetime.now().strftime('%m%d%Y_%H%M')}.log", enqueue=True)

    craft_dataset_generation_pipeline = Pipeline([
        DatasetGenerationStage(),
        PreBalancingPostProcessStage(),
        BalancingStage()
    ])
    logger.info("Dataset generation pipeline object initiated")

    dataset_generation_config_file_path = sys.argv[1]
    config = DatasetGenerationConfig(FileIO.read_json(dataset_generation_config_file_path))
    logger.info("Dataset generation configuration file loaded")

    craft_dataset_generation_pipeline.feed_first_stage(config)

    logger.info("Starting execution...")
    craft_dataset_generation_pipeline.execute_all()
