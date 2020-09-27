import glob
import json
from typing import List

import orjson
import os

import ujson

from multiprocessing import Process


class DictUtils:

    @staticmethod
    def scrub(obj, key_to_be_removed):
        if isinstance(obj, dict):
            # the call to `list` is useless for py2 but makes
            # the code py2/py3 compatible
            for key in list(obj.keys()):
                if key == key_to_be_removed:
                    obj.pop(key, None)
                else:
                    DictUtils.scrub(obj[key], key_to_be_removed)
        elif isinstance(obj, list):
            for i in reversed(range(len(obj))):
                if obj[i] == key_to_be_removed:
                    del obj[i]
                else:
                    DictUtils.scrub(obj[i], key_to_be_removed)

        else:
            # neither a dict nor a list, do nothing
            pass


class FileIO:

    @staticmethod
    def write_to_file(file_path, content):
        with open(file_path, "w") as f:
            f.write(content)
            f.close()

    @staticmethod
    def read_json(file_path):
        with open(file_path, "rb") as f:
            json_obj = ujson.load(f)
            f.close()
        return json_obj

    @staticmethod
    def write_json(json_obj, file_path):
        with open(file_path, "w") as f:
            ujson.dump(json_obj, f, escape_forward_slashes=False)
            f.close()

    @staticmethod
    def delete_files(folder_path, *wildcards):
        files_to_be_removed = []
        for w in wildcards:
            files_to_be_removed.extend([os.path.abspath(c) for c in glob.glob(f"{folder_path}/{w}")])

        for path in files_to_be_removed:
            os.remove(path) if os.path.exists(path) else None


class Funnel:
    def __init__(self, lst: list):
        self.__list = list(lst)

    def get_result(self) -> list:
        return self.__list

    def filter(self, predicate):
        self.__list = list(filter(predicate, self.__list))
        return self


class ParallelProcessor(object):
    """
    To process the functions in parallel
    """

    def __init__(self, jobs: list, args: list):
        """
        """
        self.jobs = jobs
        self.args = args
        self.processes: List[Process] = []

    def fork_processes(self):
        """
        Creates the process objects for given function delegates
        """
        for i in range(len(self.jobs)):
            job = self.jobs[i]
            job_args = self.args[i]
            proc = Process(target=job, args=job_args)
            self.processes.append(proc)

    def start_all(self):
        """
        Starts the functions process all together.
        """
        for proc in self.processes:
            proc.start()

    def join_all(self):
        """
        Waits untill all the functions executed.
        """
        for proc in self.processes:
            proc.join()

