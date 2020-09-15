from collections import defaultdict

from autorun.dataset import SVQADataset, Funnel


class DatasetStatistics:

    def __init__(self, dataset_file_path: str, metadata_file_path: str):
        self.dataset = SVQADataset(dataset_file_path, metadata_file_path)
        self.answer_freq_per_tid_and_sid = None
        self.answer_freq_per_sid = None
        self.answer_freq_per_tid = None
        self.answer_freq_total = None

    @staticmethod
    def counts_from_question_list(question_list: list, column: str) -> dict:
        counts = defaultdict(int)

        for question in question_list:
            counts[str(question[column])] += 1

        return counts

    def generate_all_stats(self):
        return self.generate_stat__answer_per_tid_and_sid()\
                .generate_stat__answer_frequencies_per_sid()\
                .generate_stat__answer_per_template()\
                .generate_stat__answer_frequencies()

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

    def generate_stat__answer_frequencies(self):
        answer_counts = DatasetStatistics.counts_from_question_list(self.dataset.questions, "answer")
        self.answer_freq_total = answer_counts
        return self


if __name__ == '__main__':
    dataset_stats = DatasetStatistics("out/Dataset_250_110820/dataset.json", "../svqa/metadata.json")

    dataset_stats = dataset_stats.generate_all_stats()
    print("Done")