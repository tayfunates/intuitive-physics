import sys
from collections import defaultdict

import numpy as np
import pandas as pd
import pylab

from framework.utils import FileIO


def by(data, field):
    question_counts = defaultdict(int)

    correct_count = defaultdict(int)
    wrong_count = defaultdict(int)

    for correct in data["correct"]:
        question_counts[correct[field]] += 1
        correct_count[correct[field]] += 1

    for wrong in data["wrong"]:
        question_counts[wrong["original"][field]] += 1
        wrong_count[wrong["original"][field]] += 1

    percentages = {}
    for key, value in question_counts.items():
        percentages[key] = wrong_count[key] / value

    combined = {field: [],
                "total": [],
                "correct": [],
                "wrong": [],
                "ratio": []}

    for key in question_counts:
        combined[field].append(key)
        combined["total"].append(question_counts[key])
        combined["correct"].append(correct_count[key])
        combined["wrong"].append(wrong_count[key])
        combined["ratio"].append(percentages[key])

    return combined


def analyse(filename, perturbation_results_path):
    data = FileIO.read_json(filename)
    by_template_id = by(data, "template_id")
    df = pd.DataFrame(by_template_id)
    df.to_csv(f"{perturbation_results_path}/perturbation_by_template_id.csv")

    by_sid = by(data, "simulation_id")
    df = pd.DataFrame(by_sid)
    df.to_csv(f"{perturbation_results_path}/perturbation_by_sid.csv")

    by_video_index = by(data, "video_index")
    df = pd.DataFrame(by_video_index)
    df.to_csv(f"{perturbation_results_path}/perturbation_by_video_index.csv")


def correlation_analysis_video_index(perturbation_results_path):
    perturb_by_video_index = pd.read_csv(f"{perturbation_results_path}/perturbation_by_video_index.csv")
    df_p = pd.DataFrame(perturb_by_video_index, columns=["video_index", "ratio"])
    df_p = df_p.rename(columns={"ratio": "perturbation_error_rate"})
    human_by_template_id = pd.read_csv(f"{perturbation_results_path}/human_eval_by_video_index.csv")
    df_h = pd.DataFrame(human_by_template_id, columns=["video_index", "ratio"])
    df_h = df_h.rename(columns={"ratio": "human_error_rate"})
    df_combined = pd.merge(df_p, df_h)

    x = df_combined["human_error_rate"]
    y = df_combined["perturbation_error_rate"]
    pylab.scatter(x, y)

    pylab.title("Error rates by video index")
    pylab.xlabel("Human error rate")
    pylab.ylabel("Perturbation error rate")

    coef = np.polyfit(x, y, 1)
    poly1d_fn = np.poly1d(coef)

    pylab.plot(x, y, 'yo', x, poly1d_fn(x), '--k')
    pylab.show()


def correlation_analysis_template_id(perturbation_results_path):
    perturb_by_template_id = pd.read_csv(f"{perturbation_results_path}/perturbation_by_template_id.csv")
    df_p = pd.DataFrame(perturb_by_template_id, columns=["template_id", "ratio"])
    df_p = df_p.rename(columns={"ratio": "perturbation_error_rate"})
    human_by_template_id = pd.read_csv(f"{perturbation_results_path}/human_eval_by_template_id.csv")
    df_h = pd.DataFrame(human_by_template_id, columns=["template_id", "ratio"])
    df_h = df_h.rename(columns={"ratio": "human_error_rate"})
    df_combined = pd.merge(df_p, df_h)

    x = df_combined["human_error_rate"]
    y = df_combined["perturbation_error_rate"]
    pylab.scatter(x, y)

    pylab.title("Question template error rates")
    pylab.xlabel("Human error rate")
    pylab.ylabel("Perturbation error rate")

    coef = np.polyfit(x, y, 1)
    poly1d_fn = np.poly1d(coef)

    pylab.plot(x, y, 'yo', x, poly1d_fn(x), '--k')
    pylab.show()


if __name__ == '__main__':
    perturbation_results_path = sys.argv[1]
    analysis_filename = sys.argv[2]
    analyse(f"{perturbation_results_path}/{analysis_filename}")
    correlation_analysis_video_index()
