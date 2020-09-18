from collections import defaultdict
from typing import List

from autorun.dataset import SVQADataset, Funnel


class DatasetStatistics:

    def __init__(self, dataset: SVQADataset):
        self.dataset = dataset
        self.answer_freq_per_tid_and_sid = None
        self.answer_freq_per_sid = None
        self.answer_freq_per_tid = None
        self.answer_freq_total = None
        self.template_id_freq_per_sid = None

    @staticmethod
    def counts_from_question_list(question_list: list, column: str) -> dict:
        counts = defaultdict(int)

        for question in question_list:
            counts[str(question[column])] += 1

        return counts

    def generate_all_stats(self):
        return self.generate_stat__answer_per_tid_and_sid() \
            .generate_stat__answer_frequencies_per_sid() \
            .generate_stat__answer_per_template() \
            .generate_stat__answer_frequencies() \
            .generate_stat__template_per_sid()

    def generate_stat__answer_per_template(self):
        answer_freq_v_template_id = []
        template_ids = self.dataset.get_unique_values("template_id")
        for tid in template_ids:
            questions = Funnel(self.dataset.questions) \
                .filter(lambda q: q["template_id"] == tid) \
                .get_result()

            answer_counts = DatasetStatistics.counts_from_question_list(questions, "answer")
            for answer, count in answer_counts.items():
                answer_freq_v_template_id.append({"template_id": tid,
                                                  "answer": answer,
                                                  "answer_type": self.dataset.get_answer_type_for_answer(answer),
                                                  "count": count})
        self.answer_freq_per_tid = answer_freq_v_template_id
        return self

    def generate_stat__answer_per_tid_and_sid(self):
        answer_freq_per_tid_and_sid = []
        template_ids = self.dataset.get_unique_values("template_id")
        simulation_ids = self.dataset.get_unique_values("simulation_id")
        for sid in simulation_ids:
            for tid in template_ids:
                questions = Funnel(self.dataset.questions) \
                    .filter(lambda q: q["template_id"] == tid and q["simulation_id"] == sid) \
                    .get_result()

                answer_counts = DatasetStatistics.counts_from_question_list(questions, "answer")
                for answer, count in answer_counts.items():
                    answer_freq_per_tid_and_sid.append({"template_id": tid,
                                                        "simulation_id": sid,
                                                        "answer": answer,
                                                        "answer_type": self.dataset.get_answer_type_for_answer(answer),
                                                        "count": count})
        self.answer_freq_per_tid_and_sid = answer_freq_per_tid_and_sid
        return self

    def generate_stat__answer_frequencies_per_sid(self):
        sim_id_v_answer_freq = []
        sim_ids = self.dataset.get_unique_values("simulation_id")
        for sid in sim_ids:
            questions = Funnel(self.dataset.questions) \
                .filter(lambda q: q["simulation_id"] == sid) \
                .get_result()

            answer_id_counts = DatasetStatistics.counts_from_question_list(questions, "answer")
            for answer, count in answer_id_counts.items():
                sim_id_v_answer_freq.append({"simulation_id": sid,
                                             "answer": answer,
                                             "answer_type": self.dataset.get_answer_type_for_answer(answer),
                                             "count": count})
        self.answer_freq_per_sid = sim_id_v_answer_freq
        return self

    def generate_stat__template_per_sid(self):
        sim_id_v_template_freq = []
        sim_ids = self.dataset.get_unique_values("simulation_id")
        for sid in sim_ids:
            questions = Funnel(self.dataset.questions) \
                .filter(lambda q: q["simulation_id"] == sid) \
                .get_result()

            template_id_counts = DatasetStatistics.counts_from_question_list(questions, "template_id")
            for tid, count in template_id_counts.items():
                sim_id_v_template_freq.append({"simulation_id": sid, "template_id": tid, "count": count})
        self.template_id_freq_per_sid = sim_id_v_template_freq
        return self

    def generate_stat__answer_frequencies(self):
        answer_counts = DatasetStatistics.counts_from_question_list(self.dataset.questions, "answer")
        self.answer_freq_total = answer_counts
        return self


class DatasetInspector:

    def __init__(self, stats: DatasetStatistics):
        self.stats = stats
        self.dataset = stats.dataset

    def inspect_tid_and_sid_versus_answer_balance(self):
        unique_answers = self.dataset.get_unique_values("answer")
        # TODO: Include 0 count answers in tidsid...
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
                        dict_of_needed_answers[simulation_id][template_id][answer_type][answer] = answer_with_max_count["count"]

        return dict_of_needed_answers


if __name__ == '__main__':
    dataset = SVQADataset("out/Dataset_250_110820", "../svqa/metadata.json")
    dataset_stats = DatasetStatistics(dataset)

    dataset_stats = dataset_stats.generate_all_stats()

    inspector = DatasetInspector(dataset_stats)
    d = inspector.inspect_tid_and_sid_versus_answer_balance()

    print("Done")
