import copy
import json
import pathlib


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


# TODO: Move statistics computation here.
