import copy
import json
import pathlib
import pandas as pd


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
            answer = question_obj["answer"]
            question = question_obj["question"]
            video_file_path = question_obj["video_filename"]
            templates[template_filename].append({"question": question,
                                                 "answer": answer,
                                                 "video_file_path": video_file_path})
    return templates


def dataset_grouped_by_video_indices(dataset_json) -> dict:
    videos = defaultdict(list)

    for qa_json in dataset_json:
        question_list = qa_json["questions"]["questions"]
        for question_obj in question_list:
            template_filename = question_obj["template_filename"]
            answer = question_obj["answer"]
            question = question_obj["question"]
            video_file_path = question_obj["video_filename"]
            video_index = question_obj["video_index"]
            videos[str(video_index)].append({"question": question,
                                             "answer": str(answer),
                                             "template_filename": template_filename,
                                             "video_file_path": video_file_path})
    return videos


def answer_counts(dataset_json) -> dict:
    templates = dataset_grouped_by_templates(dataset_json)

    answer_counts = defaultdict(int)

    for template_filename in templates:
        template_obj = templates[template_filename]
        for question in template_obj:
            answer_counts[str(question["answer"])] += 1

    return answer_counts


def balance_dataset(dataset_json) -> dict:
    new_dataset = []
    for qa_json in dataset_json:
        question_list = qa_json["questions"]["questions"]
        q_list_json = undersample_data(question_list, "answer")
        qa_json["questions"]["questions"] = q_list_json
        new_dataset.append(qa_json)

    return json.loads(json.dumps(new_dataset))


def undersample_data(data, class_name: str):
    """
    Strictly performs undersampling by randomly deleting excess elements.
    :param data: List of data with features.
    :param class_name: Name of the feature that will be used in grouping.
    :return:
    """
    df = pd.DataFrame(data)
    g = df.groupby(class_name)
    df = pd.DataFrame(g.apply(lambda x: x.sample(g.size().min()).reset_index(drop=True)))
    return json.loads(df.to_json(orient='records'))


# TODO: Move statistics computation here.
