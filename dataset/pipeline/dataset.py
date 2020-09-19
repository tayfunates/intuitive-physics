import json
import glob
import os
import subprocess
import traceback
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from colour import Color
from loguru import logger

from pipeline.utils import FileUtils, Funnel


class SVQADataset:

    def __init__(self, dataset_folder_path, metadata_json_path):
        self.dataset_folder_path = dataset_folder_path
        self.metadata_json_path = metadata_json_path
        self.metadata = json.load(open(metadata_json_path))
        self.dataset_json = json.load(open(f"{dataset_folder_path}/dataset.json"))
        self.questions = self.get_all_questions_as_list()
        self.questions_dataframe = pd.DataFrame(self.questions)
        self.max_video_index = None

    def get_last_video_index(self):
        if self.max_video_index is None:
            max_index = 0
            for question in self.questions:
                if max_index < question["video_index"]:
                    max_index = question["video_index"]
            self.max_video_index = max_index
        return self.max_video_index

    @property
    def intermediates_folder_path(self):
        return str(Path(self.dataset_folder_path).joinpath("intermediates").as_posix())

    def generate_video_path(self, video_index: int):
        return self.intermediates_folder_path + f"/{video_index:06d}.mpg"

    def generate_simulation_output_file_path(self, video_index: int):
        return self.intermediates_folder_path + f"/{video_index:06d}.json"

    def generate_questions_output_file_path(self, video_index: int):
        return self.intermediates_folder_path + f"/{video_index:06d}.json"

    def get_video_path(self, video_index: int) -> str:
        files = glob.glob(self.intermediates_folder_path + f"*/{video_index:06d}.mpg", recursive=True)
        if len(files) == 0:
            raise FileNotFoundError(f"'{video_index:06d}.mpg' not found in the dataset folder.")
        return files[0]

    def get_simulation_output_file_path(self, video_index: int) -> str:
        files = glob.glob(self.intermediates_folder_path + f"*/{video_index:06d}.json", recursive=True)
        if len(files) == 0:
            raise FileNotFoundError(f"'{video_index:06d}.json' not found in the dataset folder.")
        return files[0]

    def get_questions_output_file_path(self, video_index: int) -> str:
        files = glob.glob(self.intermediates_folder_path + f"*/qa_{video_index:06d}.json", recursive=True)
        if len(files) == 0:
            raise FileNotFoundError(f"'qa_{video_index:06d}.json' not found in the dataset folder.")
        return files[0]

    def get_answer_type_for_answer(self, answer: str) -> str:
        return ("Boolean" if answer in ["False", "True"]
                else "Shape" if answer in self.metadata["types"]["Shape"]
        else "Color" if answer in self.metadata["types"]["Color"]
        else "Size" if answer in self.metadata["types"]["Size"]
        else "Count")

    def get_unique_values(self, column: str) -> set:
        return set(self.questions_dataframe[column].to_list())

    def get_question_from_question_obj(self, question_obj, simulation_id):
        template_filename = question_obj["template_filename"]
        answer = str(question_obj["answer"])
        question = question_obj["question"]
        video_file_path = question_obj["video_filename"]
        video_index = question_obj["video_index"]
        question_index = question_obj["question_index"]
        question_family_index = question_obj["question_family_index"]

        return {"question": question,
                "answer": answer,
                "answer_type": self.get_answer_type_for_answer(answer),
                "template_filename": template_filename,
                "video_file_path": video_file_path,
                "video_index": video_index,
                "question_index": question_index,
                "question_family_index": question_family_index,
                "template_id": f"{os.path.splitext(template_filename)[0]}_{question_family_index}",
                "simulation_id": simulation_id}

    def get_question_list_from_qa_json(self, qa_json):
        questions = []
        question_list = qa_json["questions"]["questions"]
        simulation_id = qa_json["simulation_id"]
        for question_obj in question_list:
            questions.append(self.get_question_from_question_obj(question_obj, simulation_id))

        return questions

    def get_all_questions_as_list(self):
        questions = []
        for qa_json in self.dataset_json:
            questions.extend(self.get_question_list_from_qa_json(qa_json))
        return questions

    @staticmethod
    def convert_to_original_dataset_json(dataset_obj, questions: list) -> str:
        video_index_question_indices = defaultdict(list)
        for question in questions:
            video_index_question_indices[question["video_index"]].append(question["question_index"])

        for video_index, question_indices in video_index_question_indices.items():
            DatasetUtils.retain_questions(dataset_obj.dataset_json, video_index, question_indices)

        return json.dumps(dataset_obj.dataset_json)

    def generate_statistics(self, output_folder):
        stats = DatasetStatistics(self)
        stats.generate_all_stats()
        exporter = DatasetStatisticsExporter(stats, export_png=True, output_folder=output_folder)

        import logging
        logging.info(f"Generating statistics: Answer frequencies per template ID")
        exporter.generate_chart__answer_per_template()
        logging.info(f"Generating statistics: Template ID frequencies per simulation ID")
        exporter.generate_chart__template_per_sim_id()
        logging.info(f"Generating statistics: Answer frequencies in the dataset")
        exporter.generate_chart__answer_frequencies()
        logging.info(f"Generating statistics: Answer frequencies per simulation ID")
        exporter.generate_chart__answer_frequencies_per_sim_id()
        logging.info(f"Generating statistics: Answer frequencies per TID and SID")
        exporter.generate_chart__answer_per_template_and_simulation()


class DatasetUtils:
    @staticmethod
    def convert_to_list(array):
        dataset = []
        for i, elem in enumerate(array):
            obj = array[i][0]
            dataset.append(obj)
        return dataset

    @staticmethod
    def convert_to_ndarray(dataset: list):
        m = np.array([obj for obj in dataset])
        return m

    @staticmethod
    def imblearn_random_undersampling(dataset: list, class_name, discard_strategy_fn=None):
        freq = defaultdict(int)
        for q in dataset:
            freq[q[class_name]] += 1

        if len(freq.keys()) <= 1:
            return dataset

        outliers = set()
        if discard_strategy_fn is not None:
            for val in freq.keys():
                if discard_strategy_fn(class_name, val):
                    outliers.add(val)

        to_be_resampled = []
        passed = []
        for q in dataset:
            if q[class_name] not in outliers:
                to_be_resampled.append(q)
            else:
                passed.append(q)

        data = DatasetUtils.convert_to_ndarray(to_be_resampled)

        labels = np.array([])
        for item in data:
            labels = np.append(labels, f"{item[class_name]}")

        if len(set(labels)) <= 1:
            return dataset

        reshaped = data.reshape((-1, 1))

        from imblearn.under_sampling import RandomUnderSampler
        rus = RandomUnderSampler()
        X_rus, y_rus = rus.fit_resample(reshaped, labels)

        undersampled_dataset = DatasetUtils.convert_to_list(X_rus)

        undersampled_dataset.extend(passed)

        return undersampled_dataset

    @staticmethod
    def retain_questions(dataset_json, video_index, question_indices: list):
        dataset_json[video_index]["questions"]["questions"] = [
            question for question in dataset_json[video_index]["questions"]["questions"]
            if question["question_index"] in question_indices
        ]

    @staticmethod
    def relativize_paths(dataset_json, dataset_folder_path) -> dict:
        return json.loads(json.dumps(dataset_json).replace(dataset_folder_path, "./"))

    @staticmethod
    def minimized_dataset(dataset_json) -> dict:
        video_to_qa = {}
        for qa_json in dataset_json:
            video_to_qa[Path(qa_json["questions"]["info"]["video_filename"]).name] = \
                [
                    {
                        "question": question_obj["question"],
                        "answer": question_obj["answer"],
                        "template_filename": question_obj["template_filename"]
                    }
                    for question_obj in qa_json["questions"]["questions"]
                ]
        return video_to_qa

    @staticmethod
    def dataset_as_list(dataset_json_path, metadata_json_path) -> list:
        dataset = SVQADataset(dataset_json_path, metadata_json_path)
        return dataset.questions


class DatasetStatistics:

    def __init__(self, dataset: SVQADataset):
        self.dataset = dataset
        self.answer_freq_per_tid_and_sid = None
        self.answer_freq_per_sid = None
        self.answer_freq_per_tid = None
        self.answer_freq_total = None
        self.template_id_freq_per_sid = None
        self.map_of_sid_tid_pairs_to_answer_freqs = {}
        self.map_of_sid_to_answer_freqs = {}
        self.map_of_tid_to_answer_freqs = {}
        self.map_of_sid_to_tid_freqs = {}

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
            self.map_of_tid_to_answer_freqs[tid] = answer_counts
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
                self.map_of_sid_tid_pairs_to_answer_freqs[(sid, tid)] = answer_counts
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
            self.map_of_tid_to_answer_freqs[sid] = answer_id_counts
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
            self.map_of_sid_to_tid_freqs[sid] = template_id_counts
            for tid, count in template_id_counts.items():
                sim_id_v_template_freq.append({"simulation_id": sid, "template_id": tid, "count": count})
        self.template_id_freq_per_sid = sim_id_v_template_freq
        return self

    def generate_stat__answer_frequencies(self):
        answer_counts = DatasetStatistics.counts_from_question_list(self.dataset.questions, "answer")
        self.answer_freq_total = answer_counts
        return self


class DatasetStatisticsExporter:
    def __init__(self, stats: DatasetStatistics, output_folder="statistics", export_png=True):
        self.stats = stats
        self.export_png = export_png
        self.output_folder = output_folder

    def generate_pie_chart(self, title, counts, labels, colors, explodes):
        fig1, ax1 = plt.subplots(figsize=(12, 12))
        ax1.pie(counts,
                labels=labels,
                colors=colors,
                autopct='%1.1f%%',
                startangle=90,
                radius=4,
                explode=explodes)

        """ax1.legend(wedges, answers_sorted,
                  title="Answers",
                  loc="best")"""

        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.set_title(title)
        plt.tight_layout()

        if self.export_png:
            if not os.path.exists(self.output_folder):
                os.makedirs(self.output_folder)
            plt.savefig(self.output_folder + os.path.sep + title + ".png")
        else:
            plt.show()

    @staticmethod
    def answer_counts_from_question_list(question_list: list) -> dict:
        answer_counts = defaultdict(int)

        for question in question_list:
            answer_counts[str(question["answer"])] += 1

        return answer_counts

    def generate_stat__answer_counts(self, answer_counts, title):
        # TODO: Beautify the charts.
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        answers = list(answer_counts.keys())

        colors = []
        answers_sorted = []
        counting_answers = [answer for answer in answers if
                            self.stats.dataset.get_answer_type_for_answer(answer) == "Count"]
        shape_answers = [answer for answer in answers if
                         self.stats.dataset.get_answer_type_for_answer(answer) == "Shape"]
        color_answers = [answer for answer in answers if
                         self.stats.dataset.get_answer_type_for_answer(answer) == "Color"]
        boolean_answers = [answer for answer in answers if
                           self.stats.dataset.get_answer_type_for_answer(answer) == "Boolean"]

        answers_sorted.extend(counting_answers)
        if len(counting_answers) > 0:
            colors.extend(Color("red").range_to(Color("#ffaaaa"), len(counting_answers)))
        answers_sorted.extend(shape_answers)
        if len(shape_answers) > 0:
            colors.extend(Color("green").range_to(Color("#aaffaa"), len(shape_answers)))
        answers_sorted.extend(color_answers)
        if len(color_answers) > 0:
            colors.extend(Color("blue").range_to(Color("#aaaaff"), len(color_answers)))
        answers_sorted.extend(boolean_answers)
        if len(boolean_answers) > 0:
            colors.extend(Color("#555555").range_to(Color("#aaaaaa"), len(boolean_answers)))

        counts = [answer_counts[answer] for answer in answers_sorted]

        answers_sorted = [f"{answer} ({answer_counts[answer]})" for answer in answers_sorted]
        # explodes_s = [0.1] * len(answers_sorted)
        proportions = {c: c / sum(counts) for c in counts}
        explodes = [pow(1 - proportions[c] / max(proportions.values()), 2) for c in counts]

        colors_rgb = [color.rgb for color in colors]

        self.generate_pie_chart(title, counts, labels=answers_sorted, colors=colors_rgb, explodes=explodes)

    def generate_chart__answer_per_template(self):
        df = pd.DataFrame(self.stats.answer_freq_per_tid)
        FileUtils.write_to_file(f"{self.output_folder}{os.path.sep}Answer frequencies per each template ID.csv",
                                df.to_csv())
        for tid in self.stats.map_of_tid_to_answer_freqs:
            self.generate_stat__answer_counts(self.stats.map_of_tid_to_answer_freqs[tid], f'Template ID={tid}')

    def generate_chart__answer_per_template_and_simulation(self):
        df = pd.DataFrame(self.stats.answer_freq_per_tid_and_sid)
        FileUtils.write_to_file(
            f"{self.output_folder}{os.path.sep}Answer frequencies per each template ID and sim ID.csv",
            df.to_csv())
        for key in self.stats.map_of_sid_tid_pairs_to_answer_freqs:
            tid = key[1]
            sid = key[0]
            self.generate_stat__answer_counts(self.stats.map_of_sid_tid_pairs_to_answer_freqs[key],
                                              f'SID={sid}-TID={tid}')

    def generate_chart__answer_frequencies_per_sim_id(self):
        df = pd.DataFrame(self.stats.answer_freq_per_sid)
        FileUtils.write_to_file(f"{self.output_folder}{os.path.sep}Answer frequencies for each simulation ID.csv",
                                df.to_csv())
        for sid in self.stats.map_of_sid_to_answer_freqs:
            self.generate_stat__answer_counts(self.stats.map_of_sid_to_answer_freqs[sid],
                                              f'Answer frequencies for Simulation ID={sid}')

    def generate_chart__template_per_sim_id(self):
        df = pd.DataFrame(self.stats.generate_stat__template_per_sid())
        FileUtils.write_to_file(
            f"{self.output_folder}{os.path.sep}Template ID frequencies for each simulation type.csv",
            df.to_csv())
        for sid in self.stats.map_of_sid_to_tid_freqs:
            self.generate_stat__answer_counts(self.stats.map_of_sid_to_tid_freqs[sid],
                                              f'Template ID frequencies for Simulation ID={sid}')

    def generate_chart__answer_frequencies(self):
        answer_counts = self.stats.answer_freq_total
        self.generate_stat__answer_counts(answer_counts, f'Answer frequencies - Total={sum(answer_counts.values())}')
