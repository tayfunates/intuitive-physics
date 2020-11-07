import json
from collections import defaultdict
from pathlib import Path

from loguru import logger

from framework.simulation import SimulationRunner, SimulationInstance
from framework.utils import FileIO, ParallelProcessor
from converter import Converter

conv = Converter()


def resimulate_and_convert_to_mp4(sid, video_index, video_file_path, output_file_path):
    video_file_path = Path(video_file_path).absolute().as_posix()

    executable_path = "/Users/msa/Repos/intuitive-physics/simulation/2d/SVQA-Box2D/Build/bin/x86_64/Release/Testbed"
    simulation_runner = SimulationRunner(executable_path)

    controller_file_path = Path(f"./temp/{int(video_index):06d}_controller.json").absolute().as_posix()

    with open(controller_file_path, 'w') as controller_file:
        json.dump(
            json.loads(
                f"""{{
                                "simulationID": {sid},
                                "offline": true,
                                "outputVideoPath": "{video_file_path}",
                                "outputJSONPath": "ignored.json",
                                "width": 256,
                                "height": 256,
                                "inputScenePath": "{Path(f"./human_eval/intermediates/{int(video_index):06d}.json").absolute().as_posix()}",
                                "stepCount": 600
                            }}"""),
            controller_file,
            indent=2
        )

    logger.info(f"Re-simulating {video_index}...")
    simulation_runner.run_simulation(controller_file_path)
    logger.info(f"Re-simulation done: {video_index}")

    info = conv.probe(video_file_path)

    convert = conv.convert(video_file_path, output_file_path, {
        'format': 'mp4',
        'video': {
            'codec': 'h264',
            'width': 720,
            'height': 720,
            'fps': 60
        }
    })

    for timecode in convert:
        pass

    logger.info(f"Converted: {video_index} --> mp4")


if __name__ == '__main__':
    vq = FileIO.read_json("./human_eval/questions_per_video.json")

    i = 0
    video_index_question_tuples = []
    for video_index, questions in vq.items():
        video_index_question_tuples.append((video_index, questions))

    concurrent_process_count = 8
    for i in range(0, len(video_index_question_tuples), concurrent_process_count):
        jobs = []
        args = []
        start = i
        for j in range(start, start + concurrent_process_count):
            if j >= len(video_index_question_tuples):
                continue
            video_index = video_index_question_tuples[j][0]
            simulation_id = vq[video_index][0]['simulation_id']
            video_file_path = f"/Users/msa/Research/CRAFT/Dataset_3000_230920/videos/sid_{simulation_id}/{int(video_index):06d}.mpg"
            output_file_path = f"./human_eval/videos/{int(video_index):06d}.mp4"
            jobs.append(resimulate_and_convert_to_mp4)
            args.append([simulation_id, video_index, video_file_path, output_file_path])

        parallel_processes = ParallelProcessor(jobs, args)

        logger.info(f"Forking simulation processes into parallel")
        parallel_processes.fork_processes()
        logger.info(f"Starting parallel processes for simulations from {i} to {i + concurrent_process_count}")
        parallel_processes.start_all()
        logger.info(f"Waiting for parallel processes to finish")
        parallel_processes.join_all()
        logger.info(f"Joined all parallel processes into main thread")

        logger.info(f"{concurrent_process_count} videos has been converted to MP4 format. "
                    f"({i + concurrent_process_count}/{len(vq.keys())}: %{(i + concurrent_process_count) / len(vq.keys()) * 100})")
