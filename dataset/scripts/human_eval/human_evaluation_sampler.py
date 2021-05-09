import os
import random
from collections import defaultdict

import pandas as pd

from framework.dataset import CRAFTDataset
from framework.utils import FileIO


def contains_right_amount_of_q_cat(qs):
    q_cat = count_question_categories(qs)

    if sum(q_cat.values()) - q_cat["Descriptive"] > 1:
        return True
    return False


def count_question_categories(qs):
    q_cat = {
        "Descriptive": 0,
        "Counterfactual": 0,
        "Cause": 0,
        "Prevent": 0,
        "Enable": 0
    }
    for q in qs:
        q_cat[q["question_type"]] += 1

    return q_cat


def random_simulation_select(seed, sid_vi_q_map, visited):
    ret = []
    rnd = random.Random(seed)
    sids = sorted(list(sid_vi_q_map.keys()))

    for sid in sids:
        vis = list(sid_vi_q_map[sid].keys())
        vi = rnd.choice(vis)

        while vi in visited or not contains_right_amount_of_q_cat(sid_vi_q_map[sid][vi]):
            vi = rnd.choice(vis)

        visited.add(vi)
        ret.append(vi)

    return ret


def generate_random_parts(nparts: int):
    split_info_random = FileIO.read_json(f"{dataset.dataset_folder_path}/split_info_random.json")
    split_info_hard = FileIO.read_json(f"{dataset.dataset_folder_path}/split_info_hard.json")
    test_questions = []
    split_setting = {}
    for pair in split_info_random["test"]:
        video_index = pair["video_index"]
        question_index = pair["question_index"]

        for question in dataset.video_index_to_questions_map[video_index]:
            if question["question_index"] == question_index:
                test_questions.append(question)
                split_setting[f"{video_index}-{question_index}"] = "random"
                continue
    for pair in split_info_hard["test"]:
        video_index = pair["video_index"]
        question_index = pair["question_index"]

        for question in dataset.video_index_to_questions_map[video_index]:
            if question["question_index"] == question_index:
                test_questions.append(question)
                split_setting[f"{video_index}-{question_index}"] = "hard"
                continue
    human_test_dataset = CRAFTDataset(dataset_folder_path, metadata, load_immediately=False)
    human_test_dataset.questions = test_questions
    human_test_dataset.prepare_auxiliaries()
    human_test_dataset.build_sid_vi_q_map()
    visited = set()
    parts = []
    for i in range(nparts):
        vis = random_simulation_select(i + 3123, human_test_dataset.sid_vi_q_map, visited)
        parts.append(vis)
    chosen_qs = []
    for i in range(len(parts)):
        part = parts[i]
        for vi in part:
            qlist = human_test_dataset.video_index_to_questions_map[vi]
            for q in qlist:
                q["part"] = i + 1
            chosen_qs.extend(qlist)

    return parts, chosen_qs, split_setting, test_questions


def undersample(questions):
    q_aux = list(questions)
    qcat_to_qs = defaultdict(list)

    for q in q_aux:
        qcat_to_qs[q["question_type"]].append(q)

    min_qcat = min(qcat_to_qs.items(), key=lambda x: len(x[1]))
    N = len(min_qcat[1])

    chosen_qs_qcat_balanced = []
    rnd = random.Random(23213)

    for qcat in qcat_to_qs:
        qs = list(qcat_to_qs[qcat])
        rnd.shuffle(qs)
        undersampled = qs[: N]
        chosen_qs_qcat_balanced.extend(undersampled)

    return chosen_qs_qcat_balanced


def equalize_distributions(questions):
    rnd = random.Random(23213)
    # questions = list(questions)
    # rnd.shuffle(questions)

    vi_q_map = defaultdict(list)
    for q in questions:
        vi_q_map[q["video_index"]].append(q)

    chosen_qs_qcat_balanced = []

    for vi in vi_q_map:
        qcat_counts = count_question_categories(vi_q_map[vi])
        qcat_qs_map = defaultdict(list)

        for q in vi_q_map[vi]:
            qcat_qs_map[q["question_type"]].append(q)

        min_present_qcat = min(qcat_qs_map.items(), key=lambda x: len(x[1])) if len(qcat_qs_map.keys()) > 1 else (
            "", [1])
        N = len(min_present_qcat[1])

        for qcat in qcat_qs_map:
            qs = list(qcat_qs_map[qcat])
            rnd.shuffle(qs)
            undersampled = qs[:N]
            chosen_qs_qcat_balanced.extend(undersampled)

    return chosen_qs_qcat_balanced


if __name__ == '__main__':
    output_folder_path = "./human_eval_CRAFT_10K_balanced"
    dataset_folder_path = "../../framework/out/CRAFT_10K"
    metadata = FileIO.read_json("../../svqa/metadata.json")
    dataset = CRAFTDataset(dataset_folder_path, metadata)

    os.makedirs(f"{output_folder_path}/", exist_ok=True)

    parts, chosen_qs, split_setting, test_questions = generate_random_parts(5)

    chosen_qs_qcat_balanced = undersample(chosen_qs)

    undersampled_human_test_dataset = CRAFTDataset(dataset_folder_path, metadata, load_immediately=False)
    undersampled_human_test_dataset.questions = chosen_qs_qcat_balanced
    undersampled_human_test_dataset.prepare_auxiliaries()
    undersampled_human_test_dataset.build_sid_vi_q_map()

    FileIO.write_json(undersampled_human_test_dataset.questions, f"{output_folder_path}/all_human_test_questions.json")

    undersampled_human_test_dataset.generate_statistics(f"{output_folder_path}/stats")

    videos_per_part = defaultdict(list)
    for i in range(len(parts)):
        part = parts[i]
        qs_for_part = []
        for vi in part:
            qs = undersampled_human_test_dataset.video_index_to_questions_map[vi]
            if len(qs) > 0:
                videos_per_part[i + 1].append(vi)
            qs_for_part.extend(qs)

        for q in qs_for_part:
            vi = q["video_index"]
            qi = q["question_index"]

            q["split_setting"] = split_setting[f"{vi}-{qi}"]

        vq = defaultdict(list)
        for q in qs_for_part:
            vq[q["video_index"]].append(q)

        FileIO.write_json(vq, f"{output_folder_path}/part_{i + 1}_questions.json")

        pd.DataFrame(qs_for_part).to_csv(f"{output_folder_path}/part_{i + 1}_questions.csv")

    FileIO.write_json(videos_per_part, f"{output_folder_path}/videos_per_part.json")

    for part in videos_per_part:
        os.makedirs(f"{output_folder_path}/videos/part_{part}", exist_ok=True)

    for part in videos_per_part:
        for vi in videos_per_part[part]:
            sid = undersampled_human_test_dataset.vi_sid_map[vi]
            FileIO.copy(undersampled_human_test_dataset.get_video_output_path(sid, vi),
                        f"{output_folder_path}/videos/part_{part}/{vi:06d}.mpg")

    exit(0)
