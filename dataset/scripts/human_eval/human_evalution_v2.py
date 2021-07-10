import json

import pandas as pd
from framework.utils import FileIO
import math

user_responses_csv = "data/May '21 ML Human Evaluation_July 10, 2021_05.41.csv"
questions = FileIO.read_json("data/dataset_minimal.json")


def get_q(path):
    a = FileIO.read_json(path)
    q = []
    for i in a:
        for j in a[i]:
            q.append(j)
    return q


parts = [get_q("data/json_part_1_questions.json"),
         get_q("data/json_part_2_questions.json"),
         get_q("data/json_part_3_questions.json"),
         get_q("data/json_part_4_questions.json"),
         get_q("data/json_part_5_questions.json")]





#{'Descriptive', 'Prevent', 'Counterfactual', 'Enable', 'Cause'}

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


def get_user_responses(csv_path):
    df = pd.read_csv(csv_path)
    user_responses = []

    for i in range(2, len(df)):
        response = df.iloc[i]
        user_responses.append(response)

    return user_responses

def parse_qnum(i):
    s = i.split("_")
    s[0] = s[0][1:]
    if (len(s) == 1):
        s.append("1")

    part = int(s[1])
    qnum = int(s[0])
    return [part-1, qnum]

df = pd.read_csv(user_responses_csv)

"""
df = pd.read_csv(user_responses_csv)
for i in df.columns[21:-1]:
    #print(parse_qnum(i))
    part, num = parse_qnum(i)[0], parse_qnum(i)[1]
    print(parts[part][num])
"""

def get_answer(qnum: str):
    part, num = parse_qnum(qnum)[0], parse_qnum(qnum)[1]
    info = parts[part][num]
    return info
responses = get_user_responses(user_responses_csv)

"""
StartDate 2021-06-06 04:03:30
EndDate 2021-06-06 04:03:43
Status IP Address
IPAddress 46.104.100.111
Progress 1
Duration (in seconds) 13
Finished False
RecordedDate 2021-06-06 05:03:44
ResponseId R_3fwVkV5OPaHVqWW
RecipientLastName nan
RecipientFirstName nan
RecipientEmail nan
ExternalReference nan
LocationLatitude nan
LocationLongitude nan
DistributionChannel anonymous
UserLanguage EN
Q999 I agree to participate in the research study. I understand the purpose and nature of this study and I am participating voluntarily. I understand that I can withdraw from the study at any time, without any penalty or consequences.

Q998_1 nan
Q997_4 nan
Q996 nan
Q0_1 nan
Q1 nan
"""

"""
Q999 - INFORMED VOLUNTEER CONSENT FORM We kindly request that you par...
Q994 - This is the end of the study. Thank you for your participation. We are...
Q996 - Do you have trouble distinguishing colors?
"""

per_user = []

participants = []

for response in responses:
    prgs = response["Progress"]
    a = response["Q999"]
    response_id = response["ResponseId"]
    ip = response["IPAddress"]
    age = response["Q998_1"] # How old are you?
    eng_level = response["Q997_4"] #If you evaluate your English reading comprehension, what would be your score approximately? (0 = beginner, 100 = advanced)
    color_blindness = response["Q996"] #Do you have trouble distinguishing colors?
    comment = response["Q994"] # We are glad to hear your opinions and suggestions about this study.

    participant = {
        "age": str(age),
        "eng_level": str(eng_level),
        "is_color_blind": str(color_blindness),
        "comment": str(comment),
        "response_id": response_id,
        "ip": ip,
        "qualtrics_progress": prgs,
        "answers": []
    }

    evaluation = {
        "default_questions" : {
            "response_id": response_id,
            "age": age,
            "english_level": eng_level,
            "progress": prgs,
            "color_blindness": color_blindness
        },
        "questions": {
            "question_count": 0,
            "true": 0,
            "false": 0,
        },

    }

    for row in range(21, len(response)-1):
        qnum = df.columns[row]
        user_answer = str(response[row]).lower()
        info = get_answer(qnum)

        answer_obj = {
            "question_number": qnum,
            "participants_answer": str(user_answer),
            "question_info": info,
        }

        participant["answers"].append(answer_obj)

        if user_answer == "nan":
            #evaluation["questions"]["question_count"] += 1
            continue

        correct_answ = info["answer"].lower()
        if ( correct_answ == "true"):
            correct_answ = "yes"
        if ( correct_answ == "false"):
            correct_answ = "no"

        #print(user_answer, correct_answ)

        if (user_answer == correct_answ):
            evaluation["questions"]["true"] += 1
        elif (user_answer != correct_answ):
            evaluation["questions"]["false"] += 1

        evaluation["questions"]["question_count"] += 1

    per_user.append(evaluation)

    participants.append(participant)

with open("participants.json", "w") as outfile:
    json.dump(participants, outfile, indent=4)

res = {"overview": {
            "total_individual_count" : 0,
            "total_answered_question": 0,
            "total_correct_answer": 0,
            "total_wrong_answer": 0,
            "correctness_rate(%)": 0,
            "color_blindness_count" : 0,
            "non_color_blindness_count": 0,
            "num_of_question_answered_progress_under_75": 0,
            "num_of_question_answered_progress_under_80": 0,
            "num_of_question_answered_progress_under_85": 0,
            "num_of_question_answered_progress_under_90": 0,

},
        "individual": []
       }
for i in per_user:
    res["individual"].append(i)
    #print(json.dumps(i, indent=4))



for i in per_user:
    default_q = i["default_questions"]
    questions = i["questions"]

    if (default_q["color_blindness"] == "Yes"):
        res["overview"]["color_blindness_count"] += 1
    else:
        res["overview"]["non_color_blindness_count"] += 1

    res["overview"]["total_individual_count"] += 1

    if int(default_q["progress"]) < 75:
        res["overview"]["num_of_question_answered_progress_under_75"] += questions["true"] + questions["false"]
    if int(default_q["progress"]) < 80:
        res["overview"]["num_of_question_answered_progress_under_80"] += questions["true"] + questions["false"]
    if int(default_q["progress"]) < 85:
        res["overview"]["num_of_question_answered_progress_under_85"] += questions["true"] + questions["false"]
    if int(default_q["progress"]) < 90:
        res["overview"]["num_of_question_answered_progress_under_90"] += questions["true"] + questions["false"]

    res["overview"]["total_answered_question"] += questions["question_count"]
    res["overview"]["total_correct_answer"] += questions["true"]
    res["overview"]["total_wrong_answer"] += questions["false"]


res["overview"]["correctness_rate(%)"] = float(format((res["overview"]["total_correct_answer"] / res["overview"]["total_answered_question"]), '.2f'))


with open("evalution.json", "w") as outfile:
    json.dump(res, outfile, indent=4)
