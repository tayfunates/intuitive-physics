from abc import ABC, abstractmethod
from typing import Tuple, List, Dict

from autorun.dataset import SVQADataset


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
