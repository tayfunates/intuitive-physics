import json
from framework.utils import FileIO

questions = FileIO.read_json("../human_eval/questions.json")

def getQuestionInfo(questionText: str, video_index: int):
    for q in questions:
        if q["question"] == questionText and int(q["video_index"]) == video_index:
            return q

question_type = ["Prevent", "Counterfactual", "Descriptive", "Enable", "Cause"]
template_id = []
answer_type = ["Boolean", "Count", "Color", "Shape"]

"""

"""

for q in questions:
    question_type.append(q["question_type"])
    template_id.append(q["template_id"])
    answer_type.append(q["answer_type"])


for i in set(question_type):
    print(i)
print("-------")
for i in set(template_id):
    print(i)
print("-------")
for i in set(answer_type):
    print(i)



getQuestionInfo("What shape is the first object to collide with the big purple circle?", 2608)
