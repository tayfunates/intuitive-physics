import json
import glob
import os
import subprocess
import time
import traceback
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from colour import Color
from loguru import logger

from pipeline.simulation import SimulationRunner, SimulationInstance
from pipeline.utils import FileUtils, Funnel
import svqa.generate_questions as QuestionGeneratorScript


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


class QuestionGenerator:

    def __init__(self,
                 input_scene_file_path: str,
                 output_file_path: str,
                 simulation_config: dict,
                 instances_per_template=5):
        self.__args = QuestionGeneratorScript.parser.parse_args(['--input-scene-file', input_scene_file_path,
                                                                 '--output-questions-file', output_file_path,
                                                                 '--metadata-file', '../svqa/metadata.json',
                                                                 '--synonyms-json', '../svqa/synonyms.json',
                                                                 '--template-dir', '../svqa/SVQA_1.0_templates',
                                                                 '--restrict-template-count-per-video', False,
                                                                 '--print-stats', False,
                                                                 '--instances-per-template', instances_per_template,
                                                                 '--excluded-task-ids',
                                                                 simulation_config["excluded_task_ids"]])

    def execute(self):
        QuestionGeneratorScript.main(self.__args)


class Config:
    def __init__(self, config_dict):
        self.dataset_size = config_dict['dataset_size']
        self.executable_path = os.path.abspath(config_dict['executable_path']).replace("\\", "/")
        self.output_folder_path = os.path.abspath(config_dict['output_folder_path']).replace("\\", "/")
        self.test_set_ratio = config_dict['split_ratios']['test']
        self.validation_set_ratio = config_dict['split_ratios']['validation']
        self.train_set_ratio = config_dict['split_ratios']['train']
        self.sim_ids_for_each_split = config_dict['sim_ids_for_each_split']
        self.simulation_configs = config_dict['simulation_configs']
        self.offline = config_dict['offline']


class DatasetGenerator:
    """
    Generates a dataset that contains simulation outputs with variations and their videos.

    Single data in the dataset is generated as follows:
    - Run a simulation
    - Run its variations
    - Unify them under a single output file
    - Generate question-answer pairs according to the output
    - Merge the questions into a single file along with video paths.

    - Dataset folder
      - /intermediates          (A folder for intermediate outputs, may be used for debugging purposes.)
        - /sid_0
          - XXXXXX.json         (One simulation output with variations.)
          - XXXXXX.json
            ...
          - /debug              (A folder for intermediate variation outputs, cli outputs, and controller files.)
        - /sid_1
          ...
        ...
      - /videos
        - /sid_0
          - XXXXXX.mpg
          - XXXXXX.mpg
            ...
      - dataset.json            (This json file contains all the video paths, and questions generated from the outputs.)
    """

    def __init__(self, config: Config):
        self.config = config
        self.__state_file_path = f"{config.output_folder_path}/dataset_generation_state"
        self.__runner = SimulationRunner(self.config.executable_path)
        # To measure remaining and elapsed_time.
        self.__start_time = None
        self.__times = np.array([])

    def get_state(self) -> int:
        last_state = None
        if os.path.exists(self.__state_file_path):
            with open(self.__state_file_path, "r") as state_file:
                last_state = int(state_file.read())
        return last_state

    def __save_state(self, index: int):
        with(open(self.__state_file_path, "w")) as state_file:
            state_file.write(f"{index}")
            state_file.close()

    def get_simulation_instance(self, instance_id: int, controller_json_path: str):
        return SimulationInstance(instance_id, self.__runner, controller_json_path)

    def run_instance(self, sid: int, instance_id: int):
        simulation = self.get_simulation_instance(instance_id, self.get_controller_path(sid, instance_id))
        simulation.run_simulation(self.get_debug_output_path(sid, instance_id))

    def run_variations(self, sid: int, instance_id: int):
        simulation = self.get_simulation_instance(instance_id, self.get_controller_path(sid, instance_id))
        simulation.run_variations(self.get_simulation_with_variations_output_path(sid, instance_id))

    def dump_controller_file(self, instance_id: int, simulation_config: dict):
        sid = simulation_config["sid"]

        # Create controller file.
        with open(self.get_controller_path(sid, instance_id), 'w') as controller_file:
            json.dump(
                json.loads(
                    f"""{{
                            "simulationID": {sid},
                            "offline": {str(self.config.offline).lower()},
                            "outputVideoPath": "{self.get_video_output_path(sid, instance_id)}",
                            "outputJSONPath": "{self.get_bare_simulation_output_path(sid, instance_id)}",
                            "width":  {simulation_config['width']},
                            "height": {simulation_config['height']},
                            "inputScenePath":  "",
                            "stepCount": {simulation_config['step_count']}
                        }}"""),
                controller_file,
                indent=2
            )

    def __update_clock(self, t1, total_runs: int, current: int):
        diff = time.time() - t1
        times = np.append(self.__times, diff)
        logger.info(f"Approx. {round((np.mean(times) * (total_runs - current - 1)) / 60, 2)} "
                    "minutes remaining...".ljust(75, " "))

    def execute(self):
        logger.info("Dataset generation process has started.")

        # To measure remaining time.
        self.__start_time = time.time()
        times = np.array([])

        self.make_directories()

        configs_to_run = []
        for simulation_config in self.config.simulation_configs:
            configs_to_run.extend(
                [simulation_config] * (self.config.dataset_size // len(self.config.simulation_configs)))

        start = 0
        if self.get_state() is not None:
            start = self.get_state()
            logger.info(f"Dataset generation state file found at output folder path, continuing from {start}...")

        for instance_id in range(start, len(configs_to_run)):
            t1 = time.time()  # To measure remaining time.

            self.__save_state(instance_id)

            simulation_config = configs_to_run[instance_id]
            sid = simulation_config["id"]

            logger.info(f"Running simulation with SID: {sid}, instance_id: {instance_id:06d}...")

            # Create controller file for current simulation instance.
            self.dump_controller_file(instance_id, simulation_config)

            # Run simulation.
            self.run_instance(sid, instance_id)

            # Run its variations.
            self.run_variations(sid, instance_id)

            variations_output_path = self.get_simulation_with_variations_output_path(sid, instance_id)

            questions_file_path = self.get_questions_output_path(sid, instance_id)

            # Generate questions.
            try:
                question_generator = QuestionGenerator(variations_output_path, questions_file_path, simulation_config)
                question_generator.execute()
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)

            self.__update_clock(t1, len(configs_to_run), instance_id)

    def make_directories(self):
        os.makedirs(self.config.output_folder_path, exist_ok=True)

        dataset = json.loads("[]")

        json.dump(
            dataset,
            open(f"{self.config.output_folder_path}/dataset.json", "w"),
            indent=4
        )

        for sim in self.config.simulation_configs:
            os.makedirs(f"{self.config.output_folder_path}/intermediates/sid_{sim['id']}/debug", exist_ok=True)
            os.makedirs(f"{self.config.output_folder_path}/videos/sid_{sim['id']}", exist_ok=True)

    def get_controller_path(self, sid: int, instance_id: int):
        return f"{self.config.output_folder_path}/intermediates/sid_{sid}/debug/controller_{instance_id:06d}.json"

    def get_questions_output_path(self, sid: int, instance_id: int):
        return f"{self.config.output_folder_path}/intermediates/sid_{sid}/qa_{instance_id:06d}.json"

    def get_simulation_with_variations_output_path(self, sid: int, instance_id: int):
        return f"{self.config.output_folder_path}/intermediates/sid_{sid}/{instance_id:06d}.json"

    def get_video_output_path(self, sid: int, instance_id: int):
        return f"{self.config.output_folder_path}/videos/sid_{sid}/{instance_id:06d}.mpg"

    def get_bare_simulation_output_path(self, sid: int, instance_id: int):
        return f"{self.config.output_folder_path}/intermediates/sid_{sid}/debug/{instance_id:06d}.json"

    def get_debug_output_path(self, sid: int, instance_id: int):
        return f"{self.config.output_folder_path}/intermediates/sid_{sid}/debug/cl_debug_{instance_id:06d}.txt"


class DatasetSplitter:

    def __init__(self):
        # TODO
        pass
