import torch
import torch.nn as nn
from model.common import ConvLayer
from model.common import FullyConnectedLayer


class Percept(torch.nn.Module):
    """ Neural network for perception module of O2P2
    """

    def __init__(self):
        super(Percept, self).__init__()

        w = 224
        h = 224
        c = 3

        num_chn = [32, 64, 128, 256]

        self.conv1 = ConvLayer(cin=c,  cout=num_chn[0], kernel_size=4, stride=2, padding=1)
        w = self.conv1.output_size(w)

        self.conv2 = ConvLayer(cin=num_chn[0],  cout=num_chn[1], kernel_size=4, stride=2, padding=1)
        w = self.conv2.output_size(w)

        self.conv3 = ConvLayer(cin=num_chn[1],  cout=num_chn[2], kernel_size=4, stride=2, padding=1)
        w = self.conv3.output_size(w)

        self.conv4 = ConvLayer(cin=num_chn[2],  cout=num_chn[3], kernel_size=4, stride=2, padding=1)
        w = self.conv4.output_size(w)

        self.fc_input_size = w * w * num_chn[3]

        self.fcnet = FullyConnectedLayer(self.fc_input_size, 256, act=True)

        self.convnet = nn.Sequential(self.conv1, self.conv2, self.conv3, self.conv4)

    def forward(self, seg):
        output = self.convnet(seg)
        output = output.view(-1, self.fc_input_size)
        output = self.fcnet(output)
        return output
