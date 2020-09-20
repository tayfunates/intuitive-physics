import copy
import pandas as pd
from deepdiff import DeepDiff

from pipeline.dataset import DatasetStatistics, SVQADataset, DatasetUtils
from pipeline.utils import Funnel


class DatasetUnderSampler:
    def __init__(self, dataset: SVQADataset, output_file_path):
        self.__dataset = SVQADataset(dataset.dataset_folder_path, dataset.metadata_json_path)
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
                                                                        discard_strategy_fn=DatasetUnderSampler.answer_discard_strategy))

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
                                                                            discard_strategy_fn=DatasetUnderSampler.answer_discard_strategy))
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
                                                                          discard_strategy_fn=DatasetUnderSampler.answer_discard_strategy)
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
                                                                        discard_strategy_fn=DatasetUnderSampler.answer_discard_strategy))

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


class DatasetInspector:

    def __init__(self, stats: DatasetStatistics):
        self.stats = stats
        self.dataset = stats.dataset

    def inspect_tid_and_sid_versus_answer_balance(self) -> dict:
        unique_answers = self.dataset.get_unique_values("answer")
        # TODO: Include answers with 0 frequency...
        unique_answers = [answer for answer in unique_answers if answer not in [str(i) for i in range(3, 50)]]
        dict_of_needed_answers = {}

        for row in self.stats.answer_freq_per_tid_and_sid:
            simulation_id = row["simulation_id"]
            template_id = row["template_id"]
            answer_type = row["answer_type"]
            if simulation_id not in dict_of_needed_answers:
                dict_of_needed_answers[simulation_id] = {}
            if template_id not in dict_of_needed_answers[simulation_id]:
                dict_of_needed_answers[simulation_id][template_id] = {}
            if answer_type not in dict_of_needed_answers:
                dict_of_needed_answers[simulation_id][template_id][answer_type] = {}

            answers = Funnel(list(self.stats.answer_freq_per_tid_and_sid)) \
                .filter(lambda x: x["template_id"] == template_id) \
                .filter(lambda x: x["simulation_id"] == simulation_id) \
                .filter(lambda x: x["answer_type"] == answer_type) \
                .get_result()

            answer_with_max_count = max(answers, key=lambda x: x["count"])

            for answer_obj in answers:
                answer = answer_obj["answer"]
                if answer_with_max_count["answer"] != answer:
                    dict_of_needed_answers[simulation_id][template_id][answer_type][answer] \
                        = answer_with_max_count["count"] - answer_obj["count"]

            for answer in unique_answers:
                if self.dataset.get_answer_type_for_answer(answer) == answer_type:
                    if answer not in dict_of_needed_answers[simulation_id][template_id][answer_type].keys():
                        dict_of_needed_answers[simulation_id][template_id][answer_type][answer] = answer_with_max_count[
                            "count"]

        return dict_of_needed_answers


class DatasetBalancer:
    """
    Balances the dataset by generating additional videos and questions.
    """

    def __init__(self, dataset: SVQADataset):
        """
        1. Generate statistics.
        2. Determine the weak answers in a sid-tid pair.
        3. Run simulation and its variations.
        4. Generate questions until it favors the balance.
        5. If not, regenerate video, and ask questions.
        6. Return to 1 for this particular video.
        """
        self.dataset = dataset
        self.stats = DatasetStatistics(dataset)
        self.inspector = DatasetInspector(self.stats)

    def determine_answers_needed(self) -> dict:
        self.inspector.stats.generate_stat__answer_per_tid_and_sid()
        return self.inspector.inspect_tid_and_sid_versus_answer_balance()

    def start_balancing(self,
                        video_generation_max_try: int = 30):
        answers_needed = self.determine_answers_needed()
        prev_answers_needed = copy.deepcopy(answers_needed)

        number_of_video_tries = 0

        for sid in answers_needed:
            while True:
                # TODO:
                new_answers_needed = self.dataset.generate_new_restricted_sample(sid, copy.deepcopy(prev_answers_needed))

                diff = DeepDiff(new_answers_needed, prev_answers_needed, ignore_order=True)

                if prev_answers_needed == new_answers_needed:
                    number_of_video_tries += 1
                else:
                    number_of_video_tries = 0

                prev_answers_needed = copy.deepcopy(new_answers_needed)

                if number_of_video_tries >= video_generation_max_try:
                    break
