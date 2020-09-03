import argparse
import logging
from autorun.dataset import SVQADataset, DatasetUtils, Funnel, DatasetStatistics
import pandas as pd


class DatasetBalancer:
    def __init__(self, dataset: SVQADataset, output_file_path):
        self.__dataset = SVQADataset(dataset.dataset_json_path, dataset.metadata_json_path)
        self.questions = list(dataset.questions)
        self.output_file_path = output_file_path

    def get_unique_values(self, column: str) -> set:
        return set(pd.DataFrame(self.questions)[column].to_list())

    @staticmethod
    def answer_discard_strategy(class_name: str, val):
        if class_name == "answer":
            return val in range(3, 11)
        return False


    def balance_answers_within_answer_types(self):
        questions = []

        answer_types = self.get_unique_values("answer_type")
        for answer_type in answer_types:
            questions_with_this_answer_type = Funnel(self.questions) \
                .filter(lambda x: x["answer_type"] == answer_type) \
                .get_result()
            questions.extend(DatasetUtils.imblearn_random_undersampling(questions_with_this_answer_type, "answer",
                                                                        discard_strategy_fn=DatasetBalancer.answer_discard_strategy))

        self.questions = questions
        return self

    def balance_answers_within_each_simulation_id(self):
        questions = []
        answer_types = self.get_unique_values("answer_type")
        sim_ids = self.get_unique_values("simulation_id")
        for answer_type in answer_types:
            questions_with_this_answer_type = Funnel(self.questions) \
                .filter(lambda x: x["answer_type"] == answer_type) \
                .get_result()
            for sid in sim_ids:
                questions_with_this_simulation_id = Funnel(questions_with_this_answer_type) \
                    .filter(lambda x: x["simulation_id"] == sid) \
                    .get_result()
                questions.extend(DatasetUtils.imblearn_random_undersampling(questions_with_this_simulation_id, "answer",
                                                                            discard_strategy_fn=DatasetBalancer.answer_discard_strategy))
        self.questions = questions
        return self

    def balance_answers_within_each_template_and_simulation_ids(self):
        questions = []
        sim_ids = self.get_unique_values("simulation_id")
        template_ids = self.get_unique_values("template_id")
        for sid in sim_ids:
            for template_id in template_ids:
                questions_with_this_template_id = Funnel(self.questions) \
                    .filter(lambda x: x["template_id"] == template_id and x["simulation_id"] == sid) \
                    .get_result()
                undersampled = DatasetUtils.imblearn_random_undersampling(questions_with_this_template_id, "answer",
                                                                          discard_strategy_fn=DatasetBalancer.answer_discard_strategy)
                questions.extend(undersampled)

        self.questions = questions
        return self

    def balance_answers_within_each_template_id(self):
        questions = []

        template_ids = self.get_unique_values("template_id")
        for template_id in template_ids:
            questions_with_this_template_id = Funnel(self.questions) \
                .filter(lambda x: x["template_id"] == template_id) \
                .get_result()
            questions.extend(DatasetUtils.imblearn_random_undersampling(questions_with_this_template_id, "answer",
                                                                        discard_strategy_fn=DatasetBalancer.answer_discard_strategy))

        self.questions = questions
        return self

    def balance_template_ids_within_each_simulation_id(self):
        questions = []

        simulation_ids = self.get_unique_values("simulation_id")
        for sid in simulation_ids:
            questions_with_this_sid = Funnel(self.questions) \
                .filter(lambda x: x["simulation_id"] == sid) \
                .get_result()
            questions.extend(DatasetUtils.imblearn_random_undersampling(questions_with_this_sid, "template_id"))

        self.questions = questions
        return self

    def get_result(self) -> list:
        return self.questions

    def dump(self):
        with open(self.output_file_path, "w") as out_file:
            out_file.write(SVQADataset.convert_to_original_dataset_json(self.__dataset, self.questions))
            out_file.close()
        return


def init_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--output-dataset-file-path', action='store', dest='output_dataset_file_path',
                        required=True,
                        help="""
                                    File path to balanced dataset JSON file.
                               """)

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
    dataset_obj.generate_statistics(output_folder="imbalanced")

    logging.info(f"Performing various undersampling operations on dataset...")
    DatasetBalancer(dataset_obj, args.output_dataset_file_path)\
        .balance_answers_within_each_template_and_simulation_ids()\
        .dump()
    balanced_dataset = SVQADataset(args.output_dataset_file_path, args.metadata_file_path)


    balanced_dataset.generate_statistics(output_folder="balanced")
