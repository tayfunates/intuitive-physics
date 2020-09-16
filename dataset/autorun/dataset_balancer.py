import copy
import os
from abc import ABC, abstractmethod
from typing import Tuple, List, Dict

from autorun.dataset import SVQADataset
from autorun.dataset_statistics import DatasetStatistics, DatasetInspector
from autorun.simulation_runner import SimulationRunner
from deepdiff import DeepDiff


class DatasetBalancer:
    """
    Balances the dataset by regenerating questions and videos.
    """
    def __init__(self, dataset: SVQADataset):
        """
        1. Generate statistics.
        2. Determine the weak answers in a sid-tid pair.
        3. Run simulation and its variations.
        4. Generate questions until it favors the balance.
        5. If not, regenerate video, and ask questions.
        6. Return to 1 for this particular video.
        """
        self.dataset = dataset
        self.stats = DatasetStatistics(dataset)
        self.inspector = DatasetInspector(self.stats)


    def determine_answers_needed(self) -> dict:
        self.inspector.stats.generate_stat__answer_per_tid_and_sid()
        return self.inspector.inspect_tid_and_sid_versus_answer_balance()

    def start_balancing(self,
                        video_generation_max_try: int = 30):
        answers_needed = self.determine_answers_needed()
        prev_answers_needed = copy.deepcopy(answers_needed)

        number_of_video_tries = 0

        for sid in answers_needed:
            while True:
                new_answers_needed = self.dataset.generate_new_restricted_sample(sid, copy.deepcopy(prev_answers_needed))

                diff = DeepDiff(new_answers_needed, prev_answers_needed, ignore_order=True)

                if prev_answers_needed == new_answers_needed:
                    number_of_video_tries += 1
                else:
                    number_of_video_tries = 0

                prev_answers_needed = copy.deepcopy(new_answers_needed)

                if number_of_video_tries >= video_generation_max_try:
                    break

