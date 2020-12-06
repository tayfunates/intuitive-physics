import json
from collections import defaultdict
from copy import deepcopy

from framework.utils import FileIO
import pandas as pd

from spellchecker import SpellChecker
import spacy

spell = SpellChecker()


nlp = spacy.load('en_core_web_md')

questions = FileIO.read_json("../human_eval/questions.json")


def getQuestionInfo(questionText: str, video_index: int):
    for q in questions:
        if q["question"].strip().lower().replace(" ", "") == questionText.strip().lower().replace(" ", "") and int(
                q["video_index"]) == video_index:
            return q


class Question:

    def __init__(self, q_number, q_text):
        self.q_number = q_number
        self.q_text = q_text
        self.u_answers = []
        self.actual_answer = ""
        self.question_type = ""
        self.info = None
        self.finished = []
        self.unique_ids = []
        self.ips = []

    def set_info(self, info):
        self.info = info

    def set_finished(self, lst):
        self.finished = lst

    def set_user_answers(self, u_answer):
        self.u_answers = u_answer

    def set_actual_answer(self, actual_answer):
        self.actual_answer = actual_answer

    def set_question_type(self, question_type):
        self.question_type += question_type

    def printQuestion(self):
        print("Question number: ", self.q_number)
        print("Question text: ", self.q_text)
        print("User answers: ", self.u_answers)
        print("Actual answer: ", self.actual_answer)
        print("Question type: ", self.question_type)
        print()


def extract_user_responses(csv_path):
    data = pd.read_csv(csv_path)
    user_datas = []
    for key in data.keys()[17:]:
        question = Question(key, data[key][0])
        user_datas.append(question)
        ans_temp = []
        for ans in data[key][2:]:
            processed = str(ans).strip().lower()
            if processed == "no":
                processed = "false"
            if processed == "yes":
                processed = "true"
            ans_temp.append(processed)
        question.set_user_answers(ans_temp)

        finished_list = []
        for f in data["Finished"][2:]:
            finished_list.append(f)

        for id in data["ResponseId"][2:]:
            question.unique_ids.append(id)

        for ip in data["IPAddress"][2:]:
            question.ips.append(ip)

        question.set_finished(finished_list)

    for q in user_datas:
        q_number = int((q.q_number[1:]).split(".")[0])
        q_text = q.q_text

        info = getQuestionInfo(q_text, q_number)

        if info:
            q.set_actual_answer(info["answer"])
            q.set_question_type(info["question_type"])
            q.set_info(info)
        else:
            q.set_actual_answer("not found")
            q.set_question_type("not found")

    return user_datas


def evaluate():
    part1_data = extract_user_responses("./part1.csv")

    part2_data = extract_user_responses("./part2.csv")

    part3_data = extract_user_responses("./part3.csv")

    part4_data = extract_user_responses("./part4.csv")

    part5_data = extract_user_responses("./part5.csv")

    all_questions = []
    all_questions.extend(part1_data)
    all_questions.extend(part2_data)
    all_questions.extend(part3_data)
    all_questions.extend(part4_data)
    all_questions.extend(part5_data)

    evaluation = {
        "total": {
            "question_count": 0,
            "answered": 0,
            "true": 0,
            "false": 0,
            "empty": {
                "did_not_understand": 0,
                "was_too_hard_to_answer": 0,
                "no_reason": 0
            }
        },

        "per_question": {

        }
    }

    flattened = []
    for i in range(0, len(all_questions), 2):
        d = all_questions[i]
        if d.info is None:
            continue
        for ii in range(len(d.u_answers)):
            ans = d.u_answers[ii]
            q_empty_rationale = all_questions[i + 1]
            r = q_empty_rationale.u_answers[ii]
            human_answer_rationale = "answered" if ans != "nan" else "no_reason"
            if ans == "nan" and r == "true":
                human_answer_rationale = "did_not_understand"
            elif ans == "nan" and r == "false":
                human_answer_rationale = "was_too_hard_to_answer"
            qinfo = deepcopy(d.info)
            if ans == "grey":
                ans = "gray"
            qinfo["human_answer"] = ans
            qinfo["human_answer_rationale"] = human_answer_rationale
            flattened.append(qinfo)

    hards = defaultdict(list)
    for a in flattened:
        evaluation["total"]["question_count"] += 1
        if a["human_answer_rationale"] == "answered":
            ground_truth = a["answer"].strip().lower()
            ans = a["human_answer"].strip().lower()
            evaluation["total"]["answered"] += 1
            if ground_truth == ans:
                evaluation["total"]["true"] += 1
            else:
                def denote_false():
                    evaluation["total"]["false"] += 1
                    hards["false"].append(a)
                if ans.isnumeric():
                    denote_false()
                    continue
                if (ans == "true" and ground_truth == "false") or (ans == "false" and ground_truth == "true"):
                    denote_false()
                    continue

                print()
                similarity = get_similarity([ground_truth, ans])
                if similarity > 0.85:
                    print(f"Question: {a['question']}")
                    print(f"Automatically accepted: Truth: '{ground_truth}', Answer: '{ans}'.")
                    evaluation["total"]["true"] += 1
                    continue
                else:
                    print(f"Question: {a['question']}")
                    det = str(input(f"Truth: '{ground_truth}', Answer: '{ans}'. Is this correct? y/n "))
                    if det == "y":
                        evaluation["total"]["true"] += 1
                        continue
                denote_false()
        else:
            evaluation["total"]["empty"][a["human_answer_rationale"]] += 1
            if a["human_answer_rationale"] != "no_reason":
                hards[a["human_answer_rationale"]].append(a)

    FileIO.write_json(hards, "hard_not_understandable_questions.json")

    print(f"Performance among answered questions: {(evaluation['total']['true'] / (evaluation['total']['answered'])) * 100}")
    print(f"Performance among questions including 'too hard to answer':"
          f" {(evaluation['total']['true'] / (evaluation['total']['answered'] + evaluation['total']['empty']['was_too_hard_to_answer'])) * 100}")
    print(json.dumps(evaluation, indent=2))


def get_similarity(words):
    misspelled = spell.unknown(words)

    words = list(set(words).difference(misspelled))
    for word in misspelled:
        # Get the one `most likely` answer
        corrected = spell.correction(word)
        print(f"Corrected: '{word}' -> '{corrected}'")
        words.append(corrected)

    tokens = nlp(" ".join(words))

    token1, token2 = tokens[0], tokens[1]
    similarity = token1.similarity(token2)

    return similarity


if __name__ == '__main__':
    evaluate()
