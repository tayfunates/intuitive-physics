import glob
import os


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


class FileUtils:

    @staticmethod
    def write_to_file(file_path, content):
        with open(file_path, "w") as f:
            f.write(content)
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