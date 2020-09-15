import argparse
import logging

import sys

from autorun.dataset import SVQADataset, DatasetStatisticsExporter


def init_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--dataset-file-path', action='store', dest='dataset_file_path', required=True,
                        help="""
                                    File path to a dataset JSON file.
                               """)

    parser.add_argument('-m', '--metadata-file-path', action='store', dest='metadata_file_path', required=True,
                        help="""
                                    File path to metadata.json.
                               """)

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    return parser.parse_args()


if __name__ == '__main__':

    args = init_args()

    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s]\t%(asctime)s\t%(message)s')

    logging.info(f"Reading dataset from {args.dataset_file_path}")
    dataset_obj = SVQADataset(args.dataset_file_path, args.metadata_file_path)

    stats = DatasetStatisticsExporter(dataset_obj, export_png=True)

    logging.info(f"Generating statistics: Answer frequencies per template ID")
    stats.generate_stat__answer_per_template()
    logging.info(f"Generating statistics: Template ID frequencies per simulation ID")
    stats.generate_stat__template_per_sim_id()
    logging.info(f"Generating statistics: Answer frequencies in the dataset")
    stats.generate_stat__answer_frequencies()