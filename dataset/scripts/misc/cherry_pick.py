from framework.dataset import CRAFTDataset
from framework.utils import FileIO

#{'Descriptive', 'Prevent', 'Counterfactual', 'Enable', 'Cause'}
def get_videos_by_number_of_question(dataset, q_type, min_count):

    result = []

    for video_index in dataset.video_index_to_questions_map.keys():
        questions = dataset.get_questions_for_video(video_index)

        counter = 0
        for q in questions:
            if q["question_type"] == q_type:
                counter += 1

        if counter >= min_count:
            result.append((questions[0]["simulation_id"], video_index))


    print(len(result), "videos includes at least", min_count, "question with type", q_type, "(sim_id, video_idx):",  result)

def get_videos_with_min_num_of_q_type(dataset):
    result = []
    for video_index in dataset.video_index_to_questions_map.keys():
        questions = dataset.get_questions_for_video(video_index)

        counts = [0, 0, 0, 0, 0] ##{'Descriptive', 'Prevent', 'Counterfactual', 'Enable', 'Cause'}
        for q in questions:
            if q["question_type"] == "Descriptive":
                counts[0] += 1
            if q["question_type"] == "Prevent":
                counts[1] += 1
            if q["question_type"] == "Counterfactual":
                counts[2] += 1
            if q["question_type"] == "Enable":
                counts[3] += 1
            if q["question_type"] == "Cause":
                counts[4] += 1

        if min(counts) >= 2:
            result.append((questions[0]["simulation_id"],video_index))
            print(counts)

    return result

def main():
    dataset_folder_path = "../human_eval/data"
    metadata = FileIO.read_json("../../svqa/metadata.json")
    dataset = CRAFTDataset(dataset_folder_path, metadata)

    #get_videos_by_number_of_question(dataset, "Descriptive", 10)
    #get_videos_by_number_of_question(dataset, "Prevent", 3)
    #get_videos_by_number_of_question(dataset, "Counterfactual", 6)
    #get_videos_by_number_of_question(dataset, "Enable", 3)
    get_videos_by_number_of_question(dataset, "Cause", 3)


if __name__ == '__main__':
    main()