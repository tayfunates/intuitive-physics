from framework.utils import FileIO


def calculate_progress(participants):
    for participant in participants:
        n_nan = 0
        for answer in participant["answers"]:
            a = str(answer["participants_answer"]).lower()
            if a == "nan":
                n_nan += 1

        n_answered = len(participant["answers"]) - n_nan

        participant["unanswered_percent"] = 100 * (n_nan / len(participant["answers"]))
        participant["answered_percent"] = 100 * (n_answered / len(participant["answers"]))
        participant["n_answered"] = n_answered
        participant["n_nan"] = n_nan


def percentile(participants, min_answered_percent):
    num_valid = 0
    for participant in participants:
        if participant["answered_percent"] >= min_answered_percent:
            num_valid += 1

    return num_valid


def calculate(participants, progress_predicate, eng_level_predicate, is_color_blind):
    ret = []

    for participant in participants:
        correct_count = 0
        wrong_count = 0
        nan_count= 0
        if progress_predicate(participant) \
                and eng_level_predicate(participant) \
                and participant["is_color_blind"] == is_color_blind:
            for answer in participant["answers"]:
                participants_answer = answer["participants_answer"]
                truth = answer["question_info"]["answer"]

                if str(participants_answer).lower() == "yes":
                    participants_answer = "true"
                if str(participants_answer).lower() == "no":
                    participants_answer = "false"

                if str(participants_answer) != "nan":
                    if str(participants_answer).lower() == str(truth).lower():
                        correct_count += 1
                    else:
                        wrong_count += 1
                else:
                    nan_count += 1
            p = {
                "response_id": participant["response_id"],
                "ip": participant["ip"],
                "eng_level": participant["eng_level"],
                "age": participant["age"],
                "is_color_blind": participant["is_color_blind"],
                "correct_count": correct_count,
                "wrong_count": wrong_count,
                "nan_count": nan_count
            }
            ret.append(p)

    total_correct = 0
    total_wrong = 0
    total_nan = 0
    for p in ret:
        total_correct += p["correct_count"]
        total_wrong += p["wrong_count"]
        total_nan += p["nan_count"]

    overall = {
        "num_people_valid": len(ret),
        "total_correct": total_correct,
        "total_wrong": total_wrong,
        "total_nan": total_nan,
        "total_correct_percent":(total_correct / (total_correct + total_wrong)) * 100,
        "all": ret,
    }

    return overall


if __name__ == '__main__':
    participants = FileIO.read_default_json("participants.json")

    analysis = calculate(participants,
                         lambda participant: float(participant["qualtrics_progress"]) >= 75,
                         lambda participant: True,
                         "No")

    FileIO.write_default_json(analysis, "analysis_p75.json")