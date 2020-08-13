import copy
import json
import math
import pathlib
from collections import defaultdict, Counter
from math import exp

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from colour import Color
from tabulate import tabulate




# Assuming the working directory is intuitive-physics/dataset/autorun.
metadata = json.load(open("../svqa/metadata.json"))

metadata_types = metadata["types"]
metadata_booleans = ["False", "True"]
metadata_shapes = metadata_types["Shape"]
metadata_colors = metadata_types["Color"]
metadata_sizes = metadata_types["Size"]


def get_answer_type_for_answer(answer: str) -> str:
    return ("Boolean" if answer in metadata_booleans
            else "Shape" if answer in metadata_shapes
    else "Color" if answer in metadata_colors
    else "Size" if answer in metadata_sizes
    else "Count")


def minimized_dataset(dataset_json) -> dict:
    video_to_qa = {}
    for qa_json in dataset_json:
        video_to_qa[pathlib.Path(qa_json["questions"]["info"]["video_filename"]).name] = \
            [
                {
                    "question": question_obj["question"],
                    "answer": question_obj["answer"],
                    "template_filename": question_obj["template_filename"]
                }
                for question_obj in qa_json["questions"]["questions"]
            ]
    return video_to_qa


def relativize_paths(dataset_json, dataset_folder_path) -> dict:
    folder_name = pathlib.Path(dataset_folder_path).name
    return json.loads(json.dumps(dataset_json).replace(dataset_folder_path, f"./{folder_name}"))


def dataset_grouped_by_templates(dataset_json) -> dict:
    templates = defaultdict(list)

    for qa_json in dataset_json:
        question_list = qa_json["questions"]["questions"]
        for question_obj in question_list:
            template_filename = question_obj["template_filename"]
            question = get_question_from_question_obj(question_obj)
            if question["answer_type"] == "Count" and int(question["answer"]) > 3:
                continue
            templates[template_filename].append(question)

    return templates


def dataset_grouped_by_video_indices(dataset_json) -> dict:
    videos = defaultdict(list)

    for qa_json in dataset_json:
        question_list = qa_json["questions"]["questions"]
        for question_obj in question_list:
            video_index = question_obj["video_index"]
            question = get_question_from_question_obj(question_obj)
            if question["answer_type"] == "Count" and int(question["answer"]) > 3:
                continue
            videos[str(video_index)].append(question)

    return videos


def answer_counts(dataset_json) -> dict:
    templates = dataset_grouped_by_templates(dataset_json)

    answer_counts = defaultdict(int)

    for template_filename in templates:
        template_obj = templates[template_filename]
        for question in template_obj:
            answer_counts[str(question["answer"])] += 1

    return answer_counts


def answer_counts_from_question_list(all_questions: list) -> dict:
    answer_counts = defaultdict(int)

    for question in all_questions:
        answer_counts[str(question["answer"])] += 1

    return answer_counts


def undersample_data_per_answer_type(questions: list) -> list:
    counting_questions = [question for question in questions if question["answer_type"] == "Count"]
    shape_questions = [question for question in questions if question["answer_type"] == "Shape"]
    color_questions = [question for question in questions if question["answer_type"] == "Color"]

    undersampled_per_answer_type = []

    undersampled_counting = undersample_data(counting_questions, "answer") if len(counting_questions) > 0 else []
    undersampled_shape = undersample_data(shape_questions, "answer") if len(shape_questions) > 0 else []
    undersampled_color = undersample_data(color_questions, "answer") if len(color_questions) > 0 else []

    undersampled_per_answer_type.extend(undersampled_counting)
    undersampled_per_answer_type.extend(undersampled_shape)
    undersampled_per_answer_type.extend(undersampled_color)

    return undersampled_per_answer_type


def get_all_questions_as_list(dataset_json):
    questions = []

    for qa_json in dataset_json:
        questions.extend(get_question_list_from_qa_json(qa_json))

    return questions


def get_question_from_question_obj(question_obj):
    template_filename = question_obj["template_filename"]
    answer = str(question_obj["answer"])
    question = question_obj["question"]
    video_file_path = question_obj["video_filename"]
    video_index = question_obj["video_index"]
    question_index = question_obj["question_index"]

    return {"question": question,
            "answer": answer,
            "answer_type": get_answer_type_for_answer(answer),
            "template_filename": template_filename,
            "video_file_path": video_file_path,
            "video_index": video_index,
            "question_index": question_index}


def get_question_list_from_qa_json(qa_json):
    questions = []
    question_list = qa_json["questions"]["questions"]
    for question_obj in question_list:
        questions.append(get_question_from_question_obj(question_obj))

    return questions


def balance_dataset_per_video(questions_per_video) -> list:
    question_list = []

    for video_index in questions_per_video:
        undersampled_per_answer_type_per_video = \
            undersample_data_per_answer_type(questions_per_video[video_index])
        question_list.extend(undersampled_per_answer_type_per_video)

    return question_list


def balance_dataset_per_template(questions_per_template) -> list:
    question_list = []

    for template_filename in questions_per_template:
        undersampled_per_answer_type_per_template = \
            undersample_data_per_answer_type(questions_per_template[template_filename])
        question_list.extend(undersampled_per_answer_type_per_template)

    return question_list


def apply_fun(g, x):
    m = g.size().min()
    sample = x.sample(m)
    reset = sample.reset_index(drop=True)
    return reset




def undersample_data(data, class_name: str):
    """
    Strictly performs undersampling by randomly deleting excess elements.
    :param data: List of data with features.
    :param class_name: Name of the feature that will be used in grouping.
    :return:
    """
    df = pd.DataFrame(data)
    g = df.groupby(class_name)
    df = pd.DataFrame(g.apply(lambda x: apply_fun(g, x)).reset_index(drop=True))
    return json.loads(df.to_json(orient='records'))




def generate_pie_chart(answer_counts, title):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    answers = list(answer_counts.keys())

    colors = []
    answers_sorted = []
    counting_answers = [answer for answer in answers if get_answer_type_for_answer(answer) == "Count"]
    shape_answers = [answer for answer in answers if get_answer_type_for_answer(answer) == "Shape"]
    color_answers = [answer for answer in answers if get_answer_type_for_answer(answer) == "Color"]
    answers_sorted.extend(counting_answers)
    colors.extend(Color("red").range_to(Color("#ffaaaa"), len(counting_answers)))
    answers_sorted.extend(shape_answers)
    colors.extend(Color("green").range_to(Color("#aaffaa"), len(shape_answers)))
    answers_sorted.extend(color_answers)
    colors.extend(Color("blue").range_to(Color("#aaaaff"), len(color_answers)))

    counts = [answer_counts[answer] for answer in answers_sorted]

    answers_sorted = [f"{answer} ({answer_counts[answer]})" for answer in answers_sorted]
    # explodes_s = [0.1] * len(answers_sorted)
    proportions = {c: c / sum(counts) for c in counts}
    explodes = [pow(1 - proportions[c] / max(proportions.values()), 2) for c in counts]

    fig1, ax1 = plt.subplots(figsize=(12, 12))
    ax1.pie(counts,
            labels=answers_sorted,
            colors=[color.rgb for color in colors],
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


def convert_to_question_tuple_list(questions):
    return [(q["question"], q["answer"], q["template_filename"][:-5], q["video_file_path"]) for q in
            questions]


def print_statistics(question_list: list):
    print()
    print("Statistics of Generated Questions:")
    print()

    # List of (question, answer, template, video_filename).
    q_a_t_f_list = convert_to_question_tuple_list(question_list)

    # Printing all questions:
    # print(tabulate(q_a_t_f_list, headers=["Question", "Answer", "Template File", "Video"]))
    # print()

    # Calculate and print answer frequencies.
    print(get_answer_frequencies(q_a_t_f_list))


def get_answer_frequencies(q_a_t_f_list):
    answer_set: list = list(set([q[1] for q in q_a_t_f_list]))
    template_file_to_question_count_map = defaultdict(int)
    for q in q_a_t_f_list: template_file_to_question_count_map[q[2]] += 1

    template_file_to_answer_freq_map = {"**Total**": Counter({})}
    for template_file in template_file_to_question_count_map.keys():
        answers_for_this_template_file = [q[1] for q in q_a_t_f_list if q[2] == template_file]
        freq_map = Counter(answers_for_this_template_file)
        template_file_to_answer_freq_map[template_file] = freq_map
        template_file_to_answer_freq_map["**Total**"] += Counter(freq_map)

    template_file_to_question_count_map["**Total**"] = len(q_a_t_f_list)

    def answer_count_row_for(template_file):
        row = []
        for answer in answer_set:
            if answer not in template_file_to_answer_freq_map[template_file]:
                row.append("")
            else:
                count = template_file_to_answer_freq_map[template_file][answer]
                total = sum(template_file_to_answer_freq_map[template_file].values())
                row.append(f"{count} (%{round(100 * (count / total))})")
        return row

    template_count_list = [[k, v] + answer_count_row_for(k) for k, v in template_file_to_question_count_map.items()]

    answer_set_header = lambda answer_set: [f"Answer: {answer}" for answer in answer_set]

    return tabulate(template_count_list, headers=["Template File", "Question Count"] + answer_set_header(answer_set),
                    tablefmt="github")

