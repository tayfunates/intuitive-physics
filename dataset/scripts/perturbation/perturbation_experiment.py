import copy
import json
import os
from datetime import datetime
from pathlib import Path

from loguru import logger

from framework.dataset import SVQADataset
from framework.simulation import SimulationRunner, SimulationInstance
from framework.utils import FileIO, Funnel, ParallelWorker
from svqa.causal_graph import CausalGraph

from svqa import generate_questions as QuestionGeneratorScript

NOISE_AMOUNT = 0.02


def run_simulation_instance(output_json_path, controller_file_path, scene_id: int, id: int):
    logger.info(f"Running a perturbation of {id:06d}")
    new_output_json_path = Path(f"./perturbed_outputs/{id:06d}.json").absolute().as_posix()
    new_output_video_path = Path(f"./perturbed_outputs/{id:06d}.mpg").absolute().as_posix()
    new_controller_file_path = Path(
        f"./perturbed_controllers/controller_{scene_id}_{id:06d}.json").absolute().as_posix()
    new_variations_file_path = Path(f"./perturbed_outputs/variations_{scene_id}_{id:06d}.json").absolute().as_posix()
    new_questions_file_path = Path(f"./perturbed_outputs/questions_{scene_id}_{id:06d}.json").absolute().as_posix()
    new_debug_file_path = Path(f"./perturbed_outputs/debug_{scene_id}_{id:06d}.txt").absolute().as_posix()

    controller = FileIO.read_json(controller_file_path)

    with open(new_controller_file_path, 'w') as controller_file:
        json.dump(
            json.loads(
                f"""{{
                        "simulationID": {scene_id},
                        "offline": true,
                        "outputVideoPath": "{new_output_video_path}",
                        "outputJSONPath": "{new_output_json_path}",
                        "width": {controller["width"]},
                        "height": {controller["height"]},
                        "inputScenePath": "{output_json_path}",
                        "stepCount": {controller["stepCount"]},
                        "noiseAmount": {NOISE_AMOUNT}
                    }}"""),
            controller_file,
            indent=2
        )

    # Executable of the submodule at the branch new-dataset-with-noise must be built before running.
    exec_path = Path("../../../simulation/2d/SVQA-Box2D/Build/bin/x86_64/Release/Testbed").absolute().as_posix()
    working_dir = Path("../../../simulation/2d/SVQA-Box2D/Testbed").absolute().as_posix()

    runner = SimulationRunner(exec_path, working_directory=working_dir)

    instance = SimulationInstance(id, new_controller_file_path, new_variations_file_path, new_questions_file_path,
                                  runner)

    instance.run_simulation(debug_output_path=new_debug_file_path)
    instance.run_variations()


def measure_similarity(questions_original, questions_perturbed):
    correct = 0
    found_count = 0

    wrong_answers = []
    correct_answers = []
    not_found = []

    for original in questions_original:
        perturbed = None
        for question in questions_perturbed:
            if (original["question"] == question["question"]) and (
                    str(original["video_index"]) == str(question["video_index"])):
                perturbed = question

        if perturbed is None:
            not_found.append(original)
            continue
        else:
            found_count += 1
            if str(original["answer"]) == str(perturbed["answer"]):
                correct += 1
                correct_answers.append(original)
            else:
                wrong_answers.append({"original": original, "perturbed": perturbed})

    data = {"correct": correct_answers, "wrong": wrong_answers, "not_found_in_perturbed_questions": not_found}
    return data, len(questions_original), found_count, correct / found_count if found_count != 0 else 0

# Obsolete
def regenerate_questions(new_variations_output_file_path, new_perturbed_qa_file_path, simulation_id, video_index):
    logger.info(f"Regenerating questions for {video_index:06d}")
    instance = SimulationInstance(video_index, None, new_variations_output_file_path, new_perturbed_qa_file_path, None)
    instance.generate_questions(None, output_file_path=None, instances_per_template=100,
                                metadata_file_path="../../svqa/metadata.json",
                                synonyms_file_path="../../svqa/synonyms.json",
                                templates_dir="../../svqa/SVQA_1.0_templates")


def regenerate_answers(original_variations_output_file_path,
                       perturbed_variations_output_path,
                       original_questions_path,
                       new_perturbed_qa_file_path,
                       simulation_id,
                       video_index):
    logger.info(f"Regenerating answers for {video_index:06d}")
    variations_output = FileIO.read_json(perturbed_variations_output_path)
    metadata = FileIO.read_json("../../svqa/metadata.json")

    original_questions = FileIO.read_json(original_questions_path)

    original_variations_output = FileIO.read_json(original_variations_output_file_path)

    new_answers = {"questions": []}

    for qa in original_questions["questions"]:
        program = qa["program"]

        scene_structs = original_variations_output["original_video_output"]["scene_states"]
        causal_graph = CausalGraph(original_variations_output["original_video_output"]["causal_graph"])
        start_scene_struct = [scene['scene'] for scene in scene_structs if scene['step'] == 0][0]
        end_scene_struct = [scene['scene'] for scene in scene_structs if scene['step'] != 0][0]
        scene_structs_array = [start_scene_struct, end_scene_struct]

        answer = None
        try:
            answer = QuestionGeneratorScript.answer_question_offline(variations_output,
                                                                     scene_structs_array,
                                                                     causal_graph,
                                                                     program, metadata)
        except Exception as e:
            logger.error(f"Answer could not be generated: {str(e)}")

        new_qa = copy.deepcopy(qa)

        new_qa["answer"] = answer

        new_answers["questions"].append(new_qa)

    # Because of parallelization, we need to write to file, to not make things more complex with process-safety
    FileIO.write_json(new_answers, new_perturbed_qa_file_path)


def start_experiment(dataset: SVQADataset):
    logger.info(f"Starting experiment with noise amount %{NOISE_AMOUNT * 100}")

    os.makedirs("./perturbed_outputs", exist_ok=True)
    os.makedirs("./perturbed_controllers", exist_ok=True)

    video_sid_set = set()
    for question in dataset.questions:
        video_index = question["video_index"]
        simulation_id = question["simulation_id"]
        video_sid_set.add((video_index, simulation_id))

    simulation_jobs = []
    simulation_args = []

    video_sid_set = list(video_sid_set)
    video_sid_set.sort(key=lambda x: x[0])

    # Perturbation of videos
    original_questions = []
    outputs = []
    for video_sid in video_sid_set:  # Test with only 10 videos for now
        video_index = video_sid[0]
        simulation_id = video_sid[1]
        original_variations_output_file_path = f"{dataset.intermediates_folder_path}/sid_{simulation_id}/{video_index:06d}.json"
        original_questions_file_path = f"{dataset.intermediates_folder_path}/sid_{simulation_id}/qa_{video_index:06d}.json"
        old_controller_file_path = f"{dataset.intermediates_folder_path}/sid_{simulation_id}/debug/controller_{video_index:06d}.json"
        simulation_jobs.append(run_simulation_instance)
        simulation_args.append([original_variations_output_file_path, old_controller_file_path, simulation_id, video_index])
        new_variations_output_file_path = f"./perturbed_outputs/variations_{simulation_id}_{video_index:06d}.json"
        outputs.append((video_index, simulation_id, new_variations_output_file_path, original_questions_file_path, original_variations_output_file_path))
        original_questions.extend(dataset.get_questions_for_video(video_index))

    logger.info(f"{len(simulation_jobs)} simulations will be perturbed")
    parallel_worker = ParallelWorker(simulation_jobs, simulation_args, 4)
    parallel_worker.execute_all()

    question_ask_jobs = []
    question_ask_args = []

    # Regenerate answers for perturbed simulations
    qa_outputs = []
    for output in outputs:
        video_index = output[0]
        simulation_id = output[1]
        new_variations_output_file_path = output[2]
        original_questions_file_path = output[3]
        original_variations_output_file_path = output[4]
        new_perturbed_qa_file_path = f"./perturbed_outputs/qa_{video_index:06d}.json"
        question_ask_jobs.append(regenerate_answers)
        question_ask_args.append(
            [original_variations_output_file_path, new_variations_output_file_path, original_questions_file_path, new_perturbed_qa_file_path, simulation_id, video_index])
        qa_outputs.append((video_index, simulation_id, new_perturbed_qa_file_path))

    logger.info(f"Asking questions for perturbed simulations")
    parallel_worker = ParallelWorker(question_ask_jobs, question_ask_args, 8)
    parallel_worker.execute_all()

    questions_perturbed = []
    for qa in qa_outputs:
        video_index = qa[0]
        simulation_id = qa[1]
        qa_file_path = qa[2]
        qa_file = FileIO.read_json(qa_file_path)
        questions_perturbed.extend(qa_file["questions"])

    logger.info(f"Measuring similarity, this might take a while...")
    data, orig_size, found, ratio = measure_similarity(original_questions, questions_perturbed)
    logger.info(f"Number of questions from original simulations: {orig_size}")
    logger.info(f"Number of questions from perturbed simulations: {len(questions_perturbed)}")
    logger.info(f"Number of perturbed counterparts: {found}")
    logger.info(f"Match ratio: {found / orig_size}")
    logger.info(f"Correctness: {ratio}")
    logger.info(f"Dumping analysis data...")
    FileIO.write_json(data, f"analysis_data_{datetime.now().strftime('%m%d%Y_%H%M')}.json")


if __name__ == '__main__':
    logger.add(f"perturbation_{datetime.now().strftime('%m%d%Y_%H%M')}.log")

    metadata = FileIO.read_json("../../svqa/metadata.json")

    logger.info(f"Reading the dataset...")
    dataset = SVQADataset("D:\Library\Research\datasets\Dataset_3000_230920cpy\dataset.json", metadata)

    logger.info(f"{len(dataset.questions)} questions have been loaded into memory")

    start_experiment(dataset)
