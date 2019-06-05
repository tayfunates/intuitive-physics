import torch
import torch.nn as nn
from model.common import FullyConnectedLayer


class Physics(torch.nn.Module):
    """ Neural network for physics module of O2P2
    """

    def __init__(self):
        super(Physics, self).__init__()

        self.trans_hid1 = FullyConnectedLayer(256, 512)
        self.trans_hid2 = FullyConnectedLayer(512, 512)
        self.trans_out = FullyConnectedLayer(512, 256)
        self.trans = nn.Sequential(self.trans_hid1, self.trans_hid2, self.trans_out)

        self.interact_hid1 = FullyConnectedLayer(512, 512)
        self.interact_hid2 = FullyConnectedLayer(512, 512)
        self.interact_out = FullyConnectedLayer(512, 256)
        self.interact = nn.Sequential(self.interact_hid1, self.interact_hid2, self.interact_out)

    def forward(self, objs):
        new_objs = []
        for i, obj in enumerate(objs):
            obj_trans = self.trans(obj)
            obj_interact = torch.zeros_like(obj)
            for j, other_obj in enumerate(objs):
                if i == j:
                    continue
                obj_cat = torch.cat((obj, other_obj), 1)
                obj_interact += self.interact(obj_cat)
            obj_new = obj_trans + obj_interact + obj
            new_objs.append(obj_new)
        output = torch.stack(new_objs)
        return output
