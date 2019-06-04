import os.path as osp
from util.filesystem import mkdir


class Logger(object):
    def __init__(self, fpath=None):
        self.path = fpath
        mkdir(osp.dirname(fpath))

    def log(self, message):
        print(message)
        with open(self.path,"a") as f:
            f.write(message + '\n')
