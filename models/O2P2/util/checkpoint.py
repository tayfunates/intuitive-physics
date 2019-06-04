import shutil
import os.path as osp
import torch
from util.filesystem import mkdir


def save_checkpoint(state, is_best, fpath='checkpoint.pth.tar'):
    mkdir(osp.dirname(fpath))
    torch.save(state, fpath)
    if is_best:
        shutil.copy(fpath, osp.join(osp.dirname(fpath), 'best_model.pth.tar'))
