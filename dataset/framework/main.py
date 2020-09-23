import json
import time

from loguru import logger

from framework.balance import DatasetInspector, DatasetBalancer, DatasetUnderSampler
from framework.utils import FileIO
from framework.dataset import DatasetGenerationConfig, SVQADataset, DatasetStatistics, DatasetUtils

if __name__ == '__main__':

   #dataset_json = FileIO.read_json("C:/shamil/stuff/Dataset_3000_270820/dataset.json")
   #dataset_as_list = DatasetUtils.dataset_as_list(dataset_json, "../svqa/metadata.json")
   #FileIO.write_json(dataset_as_list, "C:/shamil/stuff/Dataset_3000_270820/dataset_as_list.json")

   #dataset = SVQADataset("C:/shamil/stuff/Dataset_3000_270820", "../svqa/metadata.json")
   #undersampler = DatasetUnderSampler(dataset, "C:/shamil/stuff/Dataset_3000_270820/dataset_as_list.json")
   #undersampler.balance_answers_within_each_template_and_simulation_ids().dump_as_list()

    logger.add(f"out/dataset_balancing_{time.time()}.log")



    config = DatasetGenerationConfig(FileIO.read_json("C:/shamil/stuff/Dataset_3000_270820/dataset_gen_config.json"))

    #dataset = SVQADataset("C:/shamil/stuff/Dataset_3000_270820", "../svqa/metadata.json")

    #dataset_stats = DatasetStatistics(dataset)
    #dataset_stats.generate_stat__answer_per_tid_and_sid()

    #inspector = DatasetInspector(dataset_stats)

    #answers_needed = inspector.inspect_tid_and_sid_versus_answer_balance()

    dataset_balancer = DatasetBalancer(config, None, 3000)

    dataset_balancer.start_balancing()

