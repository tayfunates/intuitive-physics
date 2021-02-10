import json
import sys

from loguru import logger

from framework.dataset import DatasetGenerationConfig, DatasetGenerator
from framework.pipeline import Pipeline, DatasetGenerationStage, BalancingStage, PreBalancingPostProcessStage
from framework.utils import FileIO


sample_config_file_json = """
{
  "dataset_size": 100,
  "executable_path": "../../../simulation/2d/SVQA-Box2D/Build/bin/x86_64/Release/Testbed",
  "metadata_file_path": "../../svqa/metadata.json",
  "output_folder_path": "out/Dataset_100_Test",
  "split_ratios": {
    "train": 0.5,
    "validation": 0.3,
    "test": 0.2
  },
  "sim_ids_for_each_split": {
    "train": null,
    "validation": null,
    "test": null
  },
  "offline": true,
  "simulation_configs": [
    {
      "id": 1,
      "step_count": 600,
      "width": 256,
      "height": 256,
      "excluded_task_ids": null
    },
    {
      "id": 2,
      "step_count": 600,
      "width": 256,
      "height": 256,
      "excluded_task_ids": null
    },
    {
      "id": 3,
      "step_count": 600,
      "width": 256,
      "height": 256,
      "excluded_task_ids": null
    },
    {
      "id": 4,
      "step_count": 600,
      "width": 256,
      "height": 256,
      "excluded_task_ids": null
    },
    {
      "id": 5,
      "step_count": 600,
      "width": 256,
      "height": 256,
      "excluded_task_ids": null
    },
    {
      "id": 6,
      "step_count": 600,
      "width": 256,
      "height": 256,
      "excluded_task_ids": null
    },
    {
      "id": 7,
      "step_count": 600,
      "width": 256,
      "height": 256,
      "excluded_task_ids": null
    },
    {
      "id": 8,
      "step_count": 600,
      "width": 256,
      "height": 256,
      "excluded_task_ids": null
    },
    {
      "id": 9,
      "step_count": 600,
      "width": 256,
      "height": 256,
      "excluded_task_ids": null
    },
    {
      "id": 10,
      "step_count": 600,
      "width": 256,
      "height": 256,
      "excluded_task_ids": null
    }
  ]
}
"""


if __name__ == '__main__':
    # Enqueue is because of multiprocessing.
    logger.add("out/dataset_generation.log", enqueue=True)

    craft_dataset_generation_pipeline = Pipeline([
        DatasetGenerationStage(),
        PreBalancingPostProcessStage(),
        BalancingStage()
    ])
    logger.info("Dataset generation pipeline object initiated")
    
    # Setup the configuration for dataset generation
    config = DatasetGenerationConfig(json.loads(sample_config_file_json))
    logger.info("Dataset generation configuration file loaded")

    # Send the first input to the pipeline
    craft_dataset_generation_pipeline.feed_first_stage(config)

    logger.info("Starting execution...")
    craft_dataset_generation_pipeline.execute_all()
