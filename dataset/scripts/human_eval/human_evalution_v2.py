import pandas as pd
from framework.utils import FileIO

user_responses_csv = "data/may_21.csv"
questions = FileIO.read_json("data/dataset_minimal.json")


#{'Descriptive', 'Prevent', 'Counterfactual', 'Enable', 'Cause'}


for i in questions:
    print(i)



def get_question_info(question_text: str, video_index: int):
    """
    sample call: get_question_info("If any of ... get into the bucket?",5690)

    returns
    {
    'question': 'If any of the other objects are removed, will the small purple cube get into the bucket?',
     'answer': 'False',
     'answer_type': 'Boolean',
     'template_filename': 'counterfactual.json',
     'video_file_path': './videos/sid_12/005690.mpg',
     'video_index': 5690,
     'question_index': 12,
     'question_family_index': 6,
     'template_id': 'counterfactual_6',
     'simulation_id': '12',
     'question_type': 'Counterfactual'
     }
    """
    for q in questions:
        dataset_text = q["question"].strip().lower().replace(" ", "")
        study_text = question_text.strip().lower().replace(" ", "")
        if dataset_text == study_text and int(q["video_index"]) == video_index:
            return q


class UserResponse:
    def __init__(self, age, eng_score, duration):
        self.age = age
        self.eng_score = eng_score
        self.duration = duration

        self.u_answers = []
        self.actual_answer = ""
        self.question_type = ""
        self.info = None
        self.finished = []
        self.unique_ids = []
        self.ips = []


def get_user_responses(csv_path):
    df = pd.read_csv(csv_path)
    user_responses = []

    valid_responses = 0
    invalid_responses = 0
    for i in range(2, len(df)):
        response = df.iloc[i]
        if int(response["Progress"]) > 75:
            user_responses.append(response)
            valid_responses += 1
        else:
            invalid_responses += 1

    return user_responses


responses = get_user_responses(user_responses_csv)
