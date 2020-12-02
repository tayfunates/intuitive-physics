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








import pandas as pd


def getResponses(csv_path):
    data = pd.read_csv(csv_path)
    res_matrix  = [[key for key in data.keys()]]
    for i in range(len(data)):
        temp = []
        for user_response in data.iloc[i]:
            temp.append(user_response)
        res_matrix.append(temp)
    res_matrix.pop(2)
    return res_matrix

discard = ['StartDate', 'EndDate', 'Status', 'IPAddress', 'Progress', 'Duration (in seconds)', 'Finished',
               'RecordedDate',
               'ResponseId', 'RecipientLastName', 'RecipientFirstName', 'RecipientEmail',
               'ExternalReference', 'LocationLatitude', 'LocationLongitude', 'DistributionChannel', 'UserLanguage'
               ]
def getQuestions(data):

    d = dict()
    for i in range(len(data[0])):
        if (data[0][i] not in discard):
            d[((data[0][i])[1:]).split(".")[0]] = data[1][i]
    return d



part1_data = getResponses("/Users/cagatayyigit/Projects/intuitive-physics/dataset/scripts/human_eval/part1.csv")
part2_data = getResponses("/Users/cagatayyigit/Projects/intuitive-physics/dataset/scripts/human_eval/part2.csv")
part3_data = getResponses("/Users/cagatayyigit/Projects/intuitive-physics/dataset/scripts/human_eval/part3.csv")
part4_data = getResponses("/Users/cagatayyigit/Projects/intuitive-physics/dataset/scripts/human_eval/part4.csv")
part5_data = getResponses("/Users/cagatayyigit/Projects/intuitive-physics/dataset/scripts/human_eval/part5.csv")

def getUserAnswers(part1_data):

    first = part1_data[0]
    second = part1_data[1]
    all = []
    for i in range(2,len(part1_data)):
        d = dict()
        for j in range(len(part1_data[i])):
            d[str(first[j])] = part1_data[i][j]
        all.append(d)
    return all



def getOnlyQuestions(part1_data):
    all = getUserAnswers(part1_data)

    res  = []
    for response_dic in all:
        for k in discard:
            del response_dic[k]
        res.append(response_dic)
    return res


class Response:
    def __init__(self, q_num, q_text, u_answer, actual_answer):
        self.question_number = q_num
        self.question_text = q_text
        self.user_answer = u_answer
        self.actual_answer = actual_answer
        self.question_type = ""

    def set_question_type(self, question_type):
        self.question_type = question_type



def statistics(data):

    arr = getOnlyQuestions(data)
    question_pair = getQuestions(data)

    for user_dic in arr:
        pass

    for key in question_pair:
        question_num = int(key.split(".")[0])
        question_text = question_pair[key]

        #print(key)
        #if question_num > 100:
        #    info = getQuestionInfo(question_text, question_num)
        #    print(info)


#print(getQuestionInfo("What shape is the first object to collide with the big purple circle?", 2608))

statistics(part1_data)