import sys

from loguru import logger

from framework.dataset import DatasetGenerationConfig, DatasetGenerator
from framework.utils import FileIO

if __name__ == '__main__':
    # Enqueue is because of multiprocessing.
    logger.add("out/dataset_generation.log", enqueue=True)

    dataset_generation_config_file_path = sys.argv[1]
    config = DatasetGenerationConfig(FileIO.read_json(dataset_generation_config_file_path))

    dataset_generator = DatasetGenerator(config)
    dataset_generator.execute()
