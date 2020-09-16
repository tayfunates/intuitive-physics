import json
import os
import glob
import subprocess
import sys
import traceback
from pathlib import Path
from collections import defaultdict

import pandas as pd
from colour import Color
import matplotlib.pyplot as plt
import numpy as np

from autorun import variation_run
from autorun.simulation_runner import SimulationRunner
from svqa import generate_questions


def write_to_file(file_path, content):
    with open(file_path, "w") as f:
        f.write(content)
        f.close()


def run_simulation(exec_path: str, controller_json_path: str):
    subprocess.call(f"{exec_path} {controller_json_path}", shell=True, universal_newlines=True)

class Funnel:
    def __init__(self, lst: list):
        self.__list = list(lst)

    def get_result(self) -> list:
        return self.__list

    def filter(self, predicate):
        self.__list = list(filter(predicate, self.__list))
        return self


class SVQADataset:

    def __init__(self, dataset_folder_path, metadata_json_path):
        self.dataset_folder_path = dataset_folder_path
        self.metadata_json_path = metadata_json_path
        self.metadata = json.load(open(metadata_json_path))
        self.dataset_json = json.load(open(f"{dataset_folder_path}/dataset.json"))
        self.questions = self.get_all_questions_as_list()
        self.questions_dataframe = pd.DataFrame(self.questions)
        self.max_video_index = None

    def generate_new_restricted_sample(self, simulation_id: str, answers_needed: dict) -> dict:
        # TODO: Breakup and refactor this function
        video_index = self.get_last_video_index() + 1

        output_folder_path = f"{self.dataset_folder_path}/append"
        os.makedirs(output_folder_path, exist_ok=True)

        controller_json_path = f"{output_folder_path}/controller_{video_index:06d}.json"
        output_json_path = f"{output_folder_path}/output_{video_index:06d}.json"
        with open(controller_json_path, 'w') as controller_file:
            # TODO: Place wxh and step count here
            json.dump(
                json.loads(f"""{{
                                   "simulationID": {int(simulation_id)},
                                   "offline": {str(False).lower()},
                                   "outputVideoPath": "{str(Path(self.generate_video_path(video_index)).resolve().as_posix())}",
                                   "outputJSONPath": "{str(Path(output_json_path).resolve().as_posix())}",
                                   "width":  256,
                                   "height": 256,
                                   "inputScenePath": "",
                                   "stepCount": 600
                               }}"""),
                controller_file,
                indent=4
            )

        executable_path = str(Path("../../simulation/2d/SVQA-Box2D/Build/bin/x86_64/Release/Testbed").resolve().as_posix())
        run_simulation(executable_path, controller_json_path)

        # Run its variations.
        variations_output_path = self.generate_simulation_output_file_path(video_index)
        variation_run.run_variations(variation_run.init_args(['-exec', executable_path,
                                                              '-c', controller_json_path,
                                                              '-p', output_json_path,
                                                              '-o', variations_output_path]))

        questions_file_path = self.generate_questions_output_file_path(video_index)

        # Generate questions.
        try:
            questions = generate_questions.main(
                generate_questions.parser.parse_args(['--input-scene-file', variations_output_path,
                                                      '--output-questions-file', questions_file_path,
                                                      '--metadata-file', '../svqa/metadata.json',
                                                      '--synonyms-json', '../svqa/synonyms.json',
                                                      '--template-dir', '../svqa/SVQA_1.0_templates',
                                                      '--restrict-template-count-per-video', False,
                                                      '--print-stats', False,
                                                      '--excluded-task-ids', None]))
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)


        acceptable_answers = list(range(3, 50))


        qa_json = json.load(open(questions_file_path))
        new_qa_json = {}
        new_qa_json["info"] = qa_json["info"]
        new_qa_json["questions"] = []
        for question in qa_json["questions"]:
            tid = f"{question['template_filename'].split('.')[0]}_{question['question_family_index']}"
            if tid in answers_needed[simulation_id]:
                answers = list(answers_needed[simulation_id][tid].values())[0]
                if str(question["answer"]) in answers.keys():
                    if answers[str(question["answer"])] > 0:
                        answers[str(question["answer"])] -= 1
                        new_qa_json["questions"].append(question)
                elif question["answer"] in acceptable_answers:
                    new_qa_json["questions"].append(question)

        return answers_needed

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

    def video_path(self, video_index: int) -> str:
        files = glob.glob(self.intermediates_folder_path + f"*/{video_index:06d}.mpg", recursive=True)
        if len(files) == 0:
            raise FileNotFoundError(f"'{video_index:06d}.mpg' not found in the dataset folder.")
        return files[0]

    def simulation_output_file_path(self, video_index: int) -> str:
        files = glob.glob(self.intermediates_folder_path + f"*/{video_index:06d}.json", recursive=True)
        if len(files) == 0:
            raise FileNotFoundError(f"'{video_index:06d}.json' not found in the dataset folder.")
        return files[0]

    def questions_output_file_path(self, video_index: int) -> str:
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
        stats = DatasetStatisticsExporter(self, export_png=True, output_folder=output_folder)

        import logging
        logging.info(f"Generating statistics: Answer frequencies per template ID")
        stats.generate_stat__answer_per_template()
        logging.info(f"Generating statistics: Template ID frequencies per simulation ID")
        stats.generate_stat__template_per_sim_id()
        logging.info(f"Generating statistics: Answer frequencies in the dataset")
        stats.generate_stat__answer_frequencies()
        logging.info(f"Generating statistics: Answer frequencies per simulation ID")
        stats.generate_stat__answer_frequencies_per_sim_id()
        logging.info(f"Generating statistics: Answer frequencies per TID and SID")
        stats.generate_stat__answer_per_template_and_simulation()


class DatasetStatisticsExporter:
    def __init__(self, dataset: SVQADataset, output_folder="statistics", export_png=True):
        self.dataset = SVQADataset(dataset.dataset_folder_path, dataset.metadata_json_path)
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

    @staticmethod
    def counts_from_question_list(question_list: list, column: str) -> dict:
        counts = defaultdict(int)

        for question in question_list:
            counts[str(question[column])] += 1

        return counts

    def generate_stat__answer_counts(self, answer_counts, title):
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        answers = list(answer_counts.keys())

        colors = []
        answers_sorted = []
        counting_answers = [answer for answer in answers if self.dataset.get_answer_type_for_answer(answer) == "Count"]
        shape_answers = [answer for answer in answers if self.dataset.get_answer_type_for_answer(answer) == "Shape"]
        color_answers = [answer for answer in answers if self.dataset.get_answer_type_for_answer(answer) == "Color"]
        boolean_answers = [answer for answer in answers if self.dataset.get_answer_type_for_answer(answer) == "Boolean"]

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

    def generate_stat__answer_per_template(self):
        answer_freq_v_template_id = []
        template_ids = self.dataset.get_unique_values("template_id")
        for tid in template_ids:
            questions = Funnel(self.dataset.questions) \
                .filter(lambda q: q["template_id"] == tid) \
                .get_result()

            answer_counts = DatasetStatisticsExporter.counts_from_question_list(questions, "answer")
            self.generate_stat__answer_counts(answer_counts, f'Template ID={tid} - {questions[0]["question"]}'.replace("?", ""))
            for answer, count in answer_counts.items():
                answer_freq_v_template_id.append({"template_id": tid, "answer": answer, "count": count})
        df = pd.DataFrame(answer_freq_v_template_id)
        write_to_file(f"{self.output_folder}{os.path.sep}Answer frequencies per each template ID.csv", df.to_csv())

    def generate_stat__answer_per_template_and_simulation(self):
        answer_freq_v_template_id = []
        template_ids = self.dataset.get_unique_values("template_id")
        simulation_ids = self.dataset.get_unique_values("simulation_id")
        for sid in simulation_ids:
            for tid in template_ids:
                questions = Funnel(self.dataset.questions) \
                    .filter(lambda q: q["template_id"] == tid and q["simulation_id"] == sid) \
                    .get_result()

                answer_counts = DatasetStatisticsExporter.counts_from_question_list(questions, "answer")
                self.generate_stat__answer_counts(answer_counts, f'SID={sid}-TID={tid}')
                for answer, count in answer_counts.items():
                    answer_freq_v_template_id.append({"template_id": tid,"simulation_id": sid, "answer": answer, "count": count})

        df = pd.DataFrame(answer_freq_v_template_id)
        write_to_file(f"{self.output_folder}{os.path.sep}Answer frequencies per each template ID and sim ID.csv", df.to_csv())

    def generate_stat__answer_frequencies_per_sim_id(self):
        sim_id_v_answer_freq = []
        sim_ids = self.dataset.get_unique_values("simulation_id")
        for sid in sim_ids:
            questions = Funnel(self.dataset.questions) \
                .filter(lambda q: q["simulation_id"] == sid) \
                .get_result()

            answer_id_counts = DatasetStatisticsExporter.counts_from_question_list(questions, "answer")
            self.generate_stat__answer_counts(answer_id_counts, f'Answer frequencies for Simulation ID={sid}')
            for answer, count in answer_id_counts.items():
                sim_id_v_answer_freq.append({"simulation_id": sid, "answer": answer, "count": count})

        df = pd.DataFrame(sim_id_v_answer_freq)
        write_to_file(f"{self.output_folder}{os.path.sep}Answer frequencies for each simulation ID.csv",
                      df.to_csv())

    def generate_stat__template_per_sim_id(self):
        sim_id_v_template_freq = []
        sim_ids = self.dataset.get_unique_values("simulation_id")
        for sid in sim_ids:
            questions = Funnel(self.dataset.questions) \
                .filter(lambda q: q["simulation_id"] == sid) \
                .get_result()

            template_id_counts = DatasetStatisticsExporter.counts_from_question_list(questions, "template_id")
            self.generate_stat__answer_counts(template_id_counts, f'Template ID frequencies for Simulation ID={sid}')
            for tid, count in template_id_counts.items():
                sim_id_v_template_freq.append({"simulation_id": sid, "template_id": tid, "count": count})

        df = pd.DataFrame(sim_id_v_template_freq)
        write_to_file(f"{self.output_folder}{os.path.sep}Template ID frequencies for each simulation type.csv",
                      df.to_csv())

    def generate_stat__answer_frequencies(self):
        answer_counts = DatasetStatisticsExporter.counts_from_question_list(self.dataset.questions, "answer")
        self.generate_stat__answer_counts(answer_counts, f'Answer frequencies - Total={sum(answer_counts.values())}')


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

