from framework.utils import FileIO
import pandas as pd

questions = FileIO.read_json("../human_eval/questions.json")
def getQuestionInfo(questionText: str, video_index: int):
    for q in questions:
        if q["question"] == questionText and int(q["video_index"]) == video_index:
            return q


class Question:

    def __init__(self, q_number, q_text):
        self.q_number = q_number
        self.q_text = q_text
        self.u_answers = []
        self.actual_answer = ""
        self.question_type = ""

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
            ans_temp.append(ans)
        question.set_user_answers(ans_temp)

    for q in user_datas:
        q_number = int((q.q_number[1:]).split(".")[0])
        q_text = q.q_text

        info = getQuestionInfo(q_text, q_number)

        if info:
            q.set_actual_answer(info["answer"])
            q.set_question_type(info["question_type"])
        else:
            q.set_actual_answer("not found")
            q.set_question_type("not found")

    return user_datas


part1_data = extract_user_responses("/Users/cagatayyigit/Projects/intuitive-physics/dataset/scripts/human_eval/part1.csv")
for i in part1_data:
    i.printQuestion()

part2_data = extract_user_responses("/Users/cagatayyigit/Projects/intuitive-physics/dataset/scripts/human_eval/part2.csv")


part3_data = extract_user_responses("/Users/cagatayyigit/Projects/intuitive-physics/dataset/scripts/human_eval/part3.csv")


part4_data = extract_user_responses("/Users/cagatayyigit/Projects/intuitive-physics/dataset/scripts/human_eval/part4.csv")


part5_data = extract_user_responses("/Users/cagatayyigit/Projects/intuitive-physics/dataset/scripts/human_eval/part5.csv")
