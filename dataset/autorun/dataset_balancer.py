from abc import ABC, abstractmethod
from typing import Tuple, List

from autorun.dataset import SVQADataset
from autorun.dataset_statistics import DatasetStatistics


class DatasetInspector:

    def __init__(self, stats: DatasetStatistics):
        self.stats = stats
        self.dataset = stats.dataset

    def inspect_tid_sid_v_answer_balance(self):
        for tid, sid, answer, answer_type, count in self.stats.answer_freq_per_tid_and_sid.items():
            pass




class DatasetBalancer:
    """
    Balances the dataset by regenerating questions and videos.
    """
    def __init__(self, dataset: SVQADataset, output_folder_path: str):
        pass
        """
        1. Generate statistics.
        2. Determine the weak answers in a sid-tid pair.
        3. Regenerate questions until it favors the balance.
        4. If not, regenerate video, and ask questions.
        5. Return to 1 for this particular video.
        """
